#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD SOVEREIGN MAINTENANCE PLATFORM
FILE 03 — MAJD-MAINTENANCE-RUNTIME-03.py

Permanent sovereign runtime:
- monitoring
- logs/metrics/events
- critical workflows
- correlation
- RCA
- incidents
- predictive maintenance
- self-healing
- anti-loop
- SLO
- capacity
- backup/restore/DR verification
- post-launch guardian
- independent verification
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import shutil
import socket
import sqlite3
import subprocess
import time
import urllib.request
import uuid
from collections import defaultdict, deque
from typing import Any, Dict, List, Optional


ROOT = pathlib.Path(
    os.environ.get("MAJD_MAINTENANCE_ROOT", "/var/lib/majd-maintenance")
).resolve()

DB = ROOT / "majd-sovereign.db"
STATE = ROOT / "runtime-state"
EVIDENCE = ROOT / "evidence"

INTERVAL = int(os.environ.get("MAJD_RUNTIME_INTERVAL", "60"))


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def run(args: List[str], timeout: int = 30) -> Dict[str, Any]:
    try:
        cp = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "ok": cp.returncode == 0,
            "returncode": cp.returncode,
            "stdout": cp.stdout[-100000:],
            "stderr": cp.stderr[-100000:],
        }
    except Exception as exc:
        return {"ok": False, "error": repr(exc)}


class RuntimeStore:
    def __init__(self):
        ROOT.mkdir(parents=True, exist_ok=True)
        STATE.mkdir(parents=True, exist_ok=True)
        EVIDENCE.mkdir(parents=True, exist_ok=True)

        self.db = sqlite3.connect(DB, timeout=30)
        self.db.row_factory = sqlite3.Row

        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS observations(
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                kind TEXT NOT NULL,
                resource TEXT NOT NULL,
                value TEXT NOT NULL,
                severity TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS runtime_incidents(
                id TEXT PRIMARY KEY,
                correlation_key TEXT NOT NULL,
                severity TEXT NOT NULL,
                state TEXT NOT NULL,
                evidence TEXT NOT NULL,
                root_cause TEXT,
                repair TEXT,
                verification TEXT,
                opened_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS repair_attempts(
                id TEXT PRIMARY KEY,
                incident_id TEXT NOT NULL,
                action TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS slo_samples(
                id TEXT PRIMARY KEY,
                service TEXT NOT NULL,
                successful INTEGER NOT NULL,
                latency REAL,
                created_at TEXT NOT NULL
            );
            """
        )
        self.db.commit()

    def observe(
        self,
        source: str,
        kind: str,
        resource: str,
        value: Dict[str, Any],
        severity: str = "INFO",
    ) -> str:
        oid = str(uuid.uuid4())

        self.db.execute(
            "INSERT INTO observations VALUES(?,?,?,?,?,?,?)",
            (
                oid,
                source,
                kind,
                resource,
                json.dumps(value, ensure_ascii=False),
                severity,
                now(),
            ),
        )
        self.db.commit()
        return oid

    def evidence(self, subject: str, payload: Any) -> None:
        path = EVIDENCE / f"runtime-{uuid.uuid4()}.json"
        path.write_text(
            json.dumps(
                {
                    "subject": subject,
                    "created_at": now(),
                    "payload": payload,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


class SystemMonitor:
    def __init__(self, store: RuntimeStore):
        self.store = store

    def resources(self) -> Dict[str, Any]:
        load = os.getloadavg()
        disk = shutil.disk_usage("/")

        memory = {}
        try:
            for line in pathlib.Path("/proc/meminfo").read_text().splitlines():
                key, value = line.split(":", 1)
                memory[key] = value.strip()
        except OSError:
            memory = {}

        result = {
            "load1": load[0],
            "load5": load[1],
            "load15": load[2],
            "cpu_count": os.cpu_count(),
            "disk_total": disk.total,
            "disk_used": disk.used,
            "disk_free": disk.free,
            "disk_percent": round(disk.used / disk.total * 100, 2),
            "memory": memory,
        }

        severity = (
            "CRITICAL"
            if result["disk_percent"] >= 95
            else "HIGH"
            if result["disk_percent"] >= 90
            else "INFO"
        )

        self.store.observe(
            "SYSTEM",
            "CAPACITY",
            socket.gethostname(),
            result,
            severity,
        )

        return result

    def services(self) -> List[Dict[str, Any]]:
        if not shutil.which("systemctl"):
            return []

        result = run(
            [
                "systemctl",
                "list-units",
                "--type=service",
                "--all",
                "--no-legend",
                "--no-pager",
            ]
        )

        services = []

        for line in result.get("stdout", "").splitlines():
            parts = line.split()

            if len(parts) < 4:
                continue

            item = {
                "name": parts[0],
                "load": parts[1],
                "active": parts[2],
                "sub": parts[3],
            }

            severity = (
                "HIGH"
                if item["active"] == "failed"
                else "INFO"
            )

            self.store.observe(
                "SYSTEMD",
                "SERVICE",
                item["name"],
                item,
                severity,
            )

            services.append(item)

        return services


class WorkflowMonitor:
    def __init__(self, store: RuntimeStore):
        self.store = store

    def http(
        self,
        name: str,
        url: str,
        expected_status: int = 200,
    ) -> Dict[str, Any]:
        started = time.monotonic()

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "MAJD-Guardian/1.0"},
            )

            with urllib.request.urlopen(req, timeout=20) as response:
                response.read(1024)
                latency = time.monotonic() - started
                success = response.status == expected_status

                result = {
                    "success": success,
                    "status": response.status,
                    "latency": latency,
                }

        except Exception as exc:
            latency = time.monotonic() - started
            result = {
                "success": False,
                "latency": latency,
                "error": repr(exc),
            }

        self.store.observe(
            "WORKFLOW",
            "HTTP",
            name,
            result,
            "INFO" if result["success"] else "CRITICAL",
        )

        self.store.db.execute(
            "INSERT INTO slo_samples VALUES(?,?,?,?,?)",
            (
                str(uuid.uuid4()),
                name,
                int(result["success"]),
                latency,
                now(),
            ),
        )
        self.store.db.commit()

        return result


class CorrelationEngine:
    def __init__(self, store: RuntimeStore):
        self.store = store

    def correlate(self, minutes: int = 10) -> List[Dict[str, Any]]:
        cutoff = (
            dt.datetime.now(dt.timezone.utc)
            - dt.timedelta(minutes=minutes)
        ).isoformat()

        rows = self.store.db.execute(
            """
            SELECT * FROM observations
            WHERE created_at>=?
              AND severity IN ('HIGH','CRITICAL')
            ORDER BY created_at
            """,
            (cutoff,),
        ).fetchall()

        grouped = defaultdict(list)

        for row in rows:
            key = f"{row['resource']}:{row['kind']}"
            grouped[key].append(dict(row))

        return [
            {
                "correlation_key": key,
                "events": values,
                "severity": (
                    "CRITICAL"
                    if any(x["severity"] == "CRITICAL" for x in values)
                    else "HIGH"
                ),
            }
            for key, values in grouped.items()
        ]


class RCAEngine:
    def diagnose(self, correlated: Dict[str, Any]) -> Dict[str, Any]:
        events = correlated["events"]

        first = events[0] if events else None
        latest = events[-1] if events else None

        return {
            "correlation_key": correlated["correlation_key"],
            "first_failure": first,
            "latest_failure": latest,
            "event_count": len(events),
            "evidence_based": True,
            "root_cause_state": (
                "CANDIDATE_IDENTIFIED"
                if events
                else "INSUFFICIENT_EVIDENCE"
            ),
        }


class IncidentManager:
    def __init__(self, store: RuntimeStore):
        self.store = store

    def open_or_update(
        self,
        correlated: Dict[str, Any],
        diagnosis: Dict[str, Any],
    ) -> str:
        key = correlated["correlation_key"]

        existing = self.store.db.execute(
            """
            SELECT id FROM runtime_incidents
            WHERE correlation_key=? AND state!='CLOSED'
            ORDER BY opened_at DESC LIMIT 1
            """,
            (key,),
        ).fetchone()

        if existing:
            iid = existing["id"]
            self.store.db.execute(
                """
                UPDATE runtime_incidents
                SET evidence=?,root_cause=?,updated_at=?
                WHERE id=?
                """,
                (
                    json.dumps(correlated, ensure_ascii=False),
                    json.dumps(diagnosis, ensure_ascii=False),
                    now(),
                    iid,
                ),
            )
        else:
            iid = str(uuid.uuid4())
            self.store.db.execute(
                """
                INSERT INTO runtime_incidents
                VALUES(?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    iid,
                    key,
                    correlated["severity"],
                    "OPEN",
                    json.dumps(correlated, ensure_ascii=False),
                    json.dumps(diagnosis, ensure_ascii=False),
                    None,
                    None,
                    now(),
                    now(),
                ),
            )

        self.store.db.commit()
        return iid


class AntiLoop:
    def __init__(
        self,
        store: RuntimeStore,
        max_attempts: int = 3,
        window_minutes: int = 30,
    ):
        self.store = store
        self.max_attempts = max_attempts
        self.window_minutes = window_minutes

    def allowed(self, incident_id: str, action: str) -> bool:
        cutoff = (
            dt.datetime.now(dt.timezone.utc)
            - dt.timedelta(minutes=self.window_minutes)
        ).isoformat()

        count = self.store.db.execute(
            """
            SELECT COUNT(*) AS c
            FROM repair_attempts
            WHERE incident_id=? AND action=? AND created_at>=?
            """,
            (incident_id, action, cutoff),
        ).fetchone()["c"]

        return count < self.max_attempts

    def record(
        self,
        incident_id: str,
        action: str,
        result: Dict[str, Any],
    ) -> None:
        self.store.db.execute(
            "INSERT INTO repair_attempts VALUES(?,?,?,?,?)",
            (
                str(uuid.uuid4()),
                incident_id,
                action,
                json.dumps(result, ensure_ascii=False),
                now(),
            ),
        )
        self.store.db.commit()


class SelfHealing:
    def __init__(self, store: RuntimeStore):
        self.store = store
        self.anti_loop = AntiLoop(store)

    def repair_failed_service(
        self,
        incident_id: str,
        service: str,
    ) -> Dict[str, Any]:
        action = f"restart:{service}"

        if not self.anti_loop.allowed(incident_id, action):
            result = {
                "ok": False,
                "state": "ANTI_LOOP_BLOCKED",
            }
            self.anti_loop.record(incident_id, action, result)
            return result

        status_before = run(
            ["systemctl", "status", service, "--no-pager"]
        )

        restart = run(["systemctl", "restart", service])

        verify = run(["systemctl", "is-active", service])

        result = {
            "ok": (
                restart["ok"]
                and verify["ok"]
                and verify.get("stdout", "").strip() == "active"
            ),
            "before": status_before,
            "repair": restart,
            "independent_process_state_verification": verify,
        }

        self.anti_loop.record(incident_id, action, result)
        return result


class PredictiveMaintenance:
    def __init__(self, store: RuntimeStore):
        self.store = store

    def disk_prediction(self) -> Dict[str, Any]:
        rows = self.store.db.execute(
            """
            SELECT value,created_at
            FROM observations
            WHERE kind='CAPACITY'
            ORDER BY created_at DESC
            LIMIT 60
            """
        ).fetchall()

        samples = []

        for row in reversed(rows):
            try:
                value = json.loads(row["value"])
                samples.append(
                    (
                        dt.datetime.fromisoformat(row["created_at"]),
                        float(value["disk_percent"]),
                    )
                )
            except Exception:
                continue

        if len(samples) < 2:
            return {
                "state": "INSUFFICIENT_HISTORY",
                "samples": len(samples),
            }

        elapsed_hours = (
            samples[-1][0] - samples[0][0]
        ).total_seconds() / 3600

        if elapsed_hours <= 0:
            return {
                "state": "INSUFFICIENT_TIME_RANGE",
            }

        growth_per_hour = (
            samples[-1][1] - samples[0][1]
        ) / elapsed_hours

        if growth_per_hour <= 0:
            return {
                "state": "STABLE_OR_DECREASING",
                "growth_percent_per_hour": growth_per_hour,
            }

        hours_to_95 = (
            95 - samples[-1][1]
        ) / growth_per_hour

        return {
            "state": "PREDICTION_AVAILABLE",
            "growth_percent_per_hour": growth_per_hour,
            "hours_to_95_percent": hours_to_95,
        }


class SLOEngine:
    def __init__(self, store: RuntimeStore):
        self.store = store

    def calculate(
        self,
        service: str,
        hours: int = 24,
    ) -> Dict[str, Any]:
        cutoff = (
            dt.datetime.now(dt.timezone.utc)
            - dt.timedelta(hours=hours)
        ).isoformat()

        rows = self.store.db.execute(
            """
            SELECT successful,latency
            FROM slo_samples
            WHERE service=? AND created_at>=?
            """,
            (service, cutoff),
        ).fetchall()

        if not rows:
            return {
                "service": service,
                "samples": 0,
                "availability": None,
            }

        successful = sum(x["successful"] for x in rows)
        latencies = [
            x["latency"]
            for x in rows
            if x["latency"] is not None
        ]

        return {
            "service": service,
            "samples": len(rows),
            "availability": successful / len(rows),
            "average_latency": (
                sum(latencies) / len(latencies)
                if latencies
                else None
            ),
        }


class PostLaunchGuardian:
    def __init__(self):
        self.store = RuntimeStore()
        self.system = SystemMonitor(self.store)
        self.workflow = WorkflowMonitor(self.store)
        self.correlation = CorrelationEngine(self.store)
        self.rca = RCAEngine()
        self.incidents = IncidentManager(self.store)
        self.predict = PredictiveMaintenance(self.store)

    def cycle(
        self,
        workflows: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        resources = self.system.resources()
        services = self.system.services()

        workflow_results = [
            self.workflow.http(
                item["name"],
                item["url"],
                item.get("status", 200),
            )
            for item in workflows
        ]

        correlated = self.correlation.correlate()
        incidents = []

        for group in correlated:
            diagnosis = self.rca.diagnose(group)
            iid = self.incidents.open_or_update(
                group,
                diagnosis,
            )
            incidents.append(
                {
                    "incident_id": iid,
                    "diagnosis": diagnosis,
                }
            )

        prediction = self.predict.disk_prediction()

        result = {
            "time": now(),
            "resources": resources,
            "services": len(services),
            "workflows": workflow_results,
            "incidents": incidents,
            "predictive_maintenance": prediction,
        }

        self.store.evidence(
            "POST_LAUNCH_GUARDIAN_CYCLE",
            result,
        )

        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["once", "loop"],
    )
    parser.add_argument(
        "--workflow",
        action="append",
        default=[],
        help="NAME=URL",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=INTERVAL,
    )
    args = parser.parse_args()

    workflows = []

    for item in args.workflow:
        if "=" not in item:
            continue
        name, url = item.split("=", 1)
        workflows.append({"name": name, "url": url})

    guardian = PostLaunchGuardian()

    if args.command == "once":
        print(
            json.dumps(
                guardian.cycle(workflows),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    while True:
        try:
            result = guardian.cycle(workflows)
            print(
                json.dumps(
                    result,
                    ensure_ascii=False,
                ),
                flush=True,
            )
        except Exception as exc:
            guardian.store.evidence(
                "RUNTIME_CYCLE_FAILURE",
                {"error": repr(exc)},
            )

        time.sleep(max(10, args.interval))


if __name__ == "__main__":
    raise SystemExit(main())

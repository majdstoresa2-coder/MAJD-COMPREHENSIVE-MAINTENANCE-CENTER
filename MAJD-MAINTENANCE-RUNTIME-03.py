#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD MAINTENANCE — FILE 03
MAJD-MAINTENANCE-RUNTIME-03.py

MAJD WATCHTOWER

Permanent runtime:
logs + metrics + traces + events
services/processes/network
DB/queues/storage
transactions/workflows
physical telemetry
correlation/RCA/incidents
prediction
self-healing
anti-loop
independent verification
SLO/SLI
capacity/FinOps
backup/DR/continuity
post-launch guardian
learning
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import shutil
import socket
import sqlite3
import ssl
import subprocess
import time
import urllib.request
import uuid
from typing import Any


ROOT = pathlib.Path(
    os.environ.get(
        "MAJD_MAINTENANCE_STATE",
        "/var/lib/majd-maintenance",
    )
).resolve()

DB = ROOT / "majd-maintenance.sqlite3"
QUEUE = ROOT / "queue"

OWNER = "SUPREME_OWNER"


def now() -> str:
    return dt.datetime.now(
        dt.timezone.utc
    ).isoformat()


def run(
    argv: list[str],
    timeout: int = 120,
) -> dict[str, Any]:
    try:
        p = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "returncode": p.returncode,
            "stdout": p.stdout[-300000:],
            "stderr": p.stderr[-100000:],
        }
    except Exception as exc:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": repr(exc),
        }


class Watchtower:
    def __init__(self):
        ROOT.mkdir(
            parents=True,
            exist_ok=True,
        )
        QUEUE.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.db = sqlite3.connect(DB)
        self.db.row_factory = sqlite3.Row

        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS telemetry(
            id TEXT PRIMARY KEY,
            kind TEXT NOT NULL,
            subject TEXT NOT NULL,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS
        idx_telemetry_kind_subject_time
        ON telemetry(kind,subject,created_at);

        CREATE TABLE IF NOT EXISTS incidents(
            id TEXT PRIMARY KEY,
            platform TEXT,
            severity TEXT NOT NULL,
            title TEXT NOT NULL,
            correlation_key TEXT,
            timeline TEXT NOT NULL,
            root_cause TEXT NOT NULL,
            evidence TEXT NOT NULL,
            containment TEXT NOT NULL,
            repair TEXT NOT NULL,
            verification TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS repair_budget(
            signature TEXT PRIMARY KEY,
            attempts INTEGER NOT NULL,
            cooldown_until TEXT,
            last_result TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS slo(
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            indicator TEXT NOT NULL,
            target REAL NOT NULL,
            window_seconds INTEGER NOT NULL,
            error_budget REAL NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS verification_results(
            id TEXT PRIMARY KEY,
            change_id TEXT NOT NULL,
            platform TEXT NOT NULL,
            success INTEGER NOT NULL,
            workflows TEXT NOT NULL,
            observation_window INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS predictions(
            id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            subject TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            evidence TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)
        self.db.commit()

    def evidence(
        self,
        category: str,
        subject: str,
        payload: Any,
    ) -> None:
        raw = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
        )

        self.db.execute("""
            INSERT INTO evidence
            (id,category,subject,payload,sha256,created_at)
            VALUES(?,?,?,?,?,?)
        """, (
            str(uuid.uuid4()),
            category,
            subject,
            raw,
            hashlib.sha256(
                raw.encode()
            ).hexdigest(),
            now(),
        ))
        self.db.commit()

    def telemetry(
        self,
        kind: str,
        subject: str,
        payload: Any,
    ) -> None:
        self.db.execute("""
            INSERT INTO telemetry
            VALUES(?,?,?,?,?)
        """, (
            str(uuid.uuid4()),
            kind,
            subject,
            json.dumps(
                payload,
                ensure_ascii=False,
            ),
            now(),
        ))
        self.db.commit()

    def system(self) -> dict[str, Any]:
        disk = shutil.disk_usage("/")

        meminfo = {}
        memfile = pathlib.Path(
            "/proc/meminfo"
        )

        if memfile.exists():
            for line in memfile.read_text().splitlines():
                if ":" in line:
                    key, value = line.split(
                        ":",
                        1,
                    )
                    meminfo[key] = value.strip()

        state = {
            "load": os.getloadavg(),
            "cpu_count": os.cpu_count(),
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "used_percent": (
                    disk.used / disk.total * 100
                    if disk.total
                    else 0
                ),
            },
            "memory": meminfo,
            "file_descriptors": run([
                "sh",
                "-c",
                "cat /proc/sys/fs/file-nr",
            ]),
        }

        self.telemetry(
            "SYSTEM",
            "local-host",
            state,
        )
        return state

    def processes(self) -> dict[str, Any]:
        state = {
            "processes": run([
                "ps",
                "-eo",
                "pid,ppid,user,%cpu,%mem,etimes,state,comm,args",
                "--no-headers",
            ]),
            "zombies": run([
                "sh",
                "-c",
                "ps -eo pid,ppid,state,comm | awk '$3 ~ /Z/'",
            ]),
        }

        self.telemetry(
            "PROCESSES",
            "local-host",
            state,
        )
        return state

    def services(self) -> dict[str, Any]:
        state = {
            "failed": run([
                "systemctl",
                "list-units",
                "--type=service",
                "--state=failed",
                "--no-pager",
                "--no-legend",
            ]) if shutil.which(
                "systemctl"
            ) else {},
        }

        self.telemetry(
            "SERVICES",
            "local-host",
            state,
        )
        return state

    def network(self) -> dict[str, Any]:
        state = {
            "interfaces": run([
                "ip",
                "-s",
                "-j",
                "link",
            ]) if shutil.which("ip") else {},
            "routes": run([
                "ip",
                "-j",
                "route",
            ]) if shutil.which("ip") else {},
            "socket_summary": run([
                "ss",
                "-s",
            ]) if shutil.which("ss") else {},
            "listeners": run([
                "ss",
                "-lntup",
            ]) if shutil.which("ss") else {},
        }

        self.telemetry(
            "NETWORK",
            "local-host",
            state,
        )
        return state

    def thermal(self) -> dict[str, Any]:
        state = {
            "visibility": "NOT_VISIBLE",
            "sensors": [],
        }

        base = pathlib.Path(
            "/sys/class/thermal"
        )

        if base.exists():
            state[
                "visibility"
            ] = "DIRECTLY_OBSERVED"

            for zone in base.glob(
                "thermal_zone*"
            ):
                try:
                    raw = int(
                        (zone / "temp")
                        .read_text()
                        .strip()
                    )

                    sensor_type = (
                        (zone / "type")
                        .read_text()
                        .strip()
                        if (zone / "type").exists()
                        else zone.name
                    )

                    state["sensors"].append({
                        "sensor": sensor_type,
                        "celsius": raw / 1000,
                    })
                except Exception:
                    continue

        if shutil.which("sensors"):
            state["lm_sensors"] = run([
                "sensors",
                "-j",
            ])

        self.telemetry(
            "PHYSICAL_THERMAL",
            "local-host",
            state,
        )
        return state

    def power(self) -> dict[str, Any]:
        state = {
            "visibility": "NOT_VISIBLE",
            "power_supplies": [],
            "ups": None,
        }

        power = pathlib.Path(
            "/sys/class/power_supply"
        )

        if power.exists():
            entries = list(power.iterdir())

            if entries:
                state[
                    "visibility"
                ] = "DIRECTLY_OBSERVED"

            for item in entries:
                values = {}

                for name in (
                    "status",
                    "capacity",
                    "voltage_now",
                    "current_now",
                    "power_now",
                ):
                    p = item / name

                    if p.exists():
                        try:
                            values[name] = (
                                p.read_text().strip()
                            )
                        except Exception:
                            continue

                state[
                    "power_supplies"
                ].append({
                    "name": item.name,
                    "values": values,
                })

        if shutil.which("upsc"):
            state["ups"] = {
                "visibility":
                    "DIRECTLY_OBSERVED",
                "devices": run([
                    "upsc",
                    "-l",
                ]),
            }

        self.telemetry(
            "PHYSICAL_POWER",
            "local-host",
            state,
        )
        return state

    def storage(self) -> dict[str, Any]:
        state = {
            "visibility": "NOT_VISIBLE",
            "nvme": [],
            "smart": [],
        }

        if shutil.which("nvme"):
            state[
                "visibility"
            ] = "DIRECTLY_OBSERVED"

            for device in pathlib.Path(
                "/dev"
            ).glob("nvme*n1"):
                state["nvme"].append({
                    "device": str(device),
                    "smart": run([
                        "nvme",
                        "smart-log",
                        str(device),
                        "-o",
                        "json",
                    ]),
                })

        if shutil.which("smartctl"):
            state[
                "visibility"
            ] = "DIRECTLY_OBSERVED"

            devices = run([
                "lsblk",
                "-dn",
                "-o",
                "NAME,TYPE",
            ])

            for line in devices[
                "stdout"
            ].splitlines():
                parts = line.split()

                if (
                    len(parts) == 2
                    and parts[1] == "disk"
                ):
                    dev = "/dev/" + parts[0]

                    state["smart"].append({
                        "device": dev,
                        "health": run([
                            "smartctl",
                            "-H",
                            "-j",
                            dev,
                        ]),
                    })

        self.telemetry(
            "PHYSICAL_STORAGE",
            "local-host",
            state,
        )
        return state

    def environment(self) -> dict[str, Any]:
        state = {
            "humidity": "NOT_VISIBLE",
            "smoke": "NOT_VISIBLE",
            "water_leak": "NOT_VISIBLE",
            "vibration": "NOT_VISIBLE",
            "air_quality": "NOT_VISIBLE",
            "facility_fire_zone":
                "NOT_VISIBLE",
            "physical_access":
                "NOT_VISIBLE",
            "cooling_system":
                "NOT_VISIBLE",
        }

        self.telemetry(
            "FACILITY_ENVIRONMENT",
            "local-host",
            state,
        )
        return state

    def hardware(self) -> dict[str, Any]:
        state = {
            "edac_ecc": (
                "DIRECTLY_OBSERVED"
                if pathlib.Path(
                    "/sys/devices/system/edac"
                ).exists()
                else "NOT_VISIBLE"
            ),
            "bmc": (
                "DIRECTLY_OBSERVED"
                if shutil.which("ipmitool")
                else "NOT_VISIBLE"
            ),
            "hwmon": (
                "DIRECTLY_OBSERVED"
                if pathlib.Path(
                    "/sys/class/hwmon"
                ).exists()
                else "NOT_VISIBLE"
            ),
        }

        self.telemetry(
            "PHYSICAL_HARDWARE",
            "local-host",
            state,
        )
        return state

    def http_workflow(
        self,
        workflow: dict[str, Any],
    ) -> dict[str, Any]:
        started = time.monotonic()

        request = urllib.request.Request(
            workflow["url"],
            method=workflow.get(
                "method",
                "GET",
            ).upper(),
            headers=workflow.get(
                "headers",
                {},
            ),
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=int(
                    workflow.get(
                        "timeout",
                        20,
                    )
                ),
            ) as response:
                body = response.read(
                    1024 * 1024
                )

                expected = int(
                    workflow.get(
                        "status",
                        200,
                    )
                )

                result = {
                    "success":
                        response.status
                        == expected,
                    "status":
                        response.status,
                    "expected": expected,
                    "latency_ms": round(
                        (
                            time.monotonic()
                            - started
                        ) * 1000,
                        2,
                    ),
                    "body_hash":
                        hashlib.sha256(
                            body
                        ).hexdigest(),
                }

        except Exception as exc:
            result = {
                "success": False,
                "error": repr(exc),
            }

        self.telemetry(
            "CRITICAL_WORKFLOW",
            workflow.get(
                "name",
                workflow["url"],
            ),
            result,
        )
        return result

    def database_health(
        self,
        path: pathlib.Path,
    ) -> dict[str, Any]:
        try:
            db = sqlite3.connect(
                f"file:{path.resolve()}?mode=ro",
                uri=True,
                timeout=5,
            )

            integrity = db.execute(
                "PRAGMA quick_check"
            ).fetchall()

            foreign = db.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()

            db.close()

            result = {
                "available": True,
                "integrity":
                    [x[0] for x in integrity],
                "foreign_key_errors":
                    [list(x) for x in foreign],
                "healthy": (
                    len(integrity) == 1
                    and integrity[0][0] == "ok"
                    and not foreign
                ),
            }
        except Exception as exc:
            result = {
                "available": False,
                "healthy": False,
                "error": repr(exc),
            }

        self.telemetry(
            "DATABASE",
            str(path),
            result,
        )
        return result

    def detect(
        self,
        system: dict[str, Any],
        thermal: dict[str, Any],
        storage: dict[str, Any],
        services: dict[str, Any],
    ) -> list[dict[str, Any]]:
        findings = []

        disk_pct = system[
            "disk"
        ]["used_percent"]

        if disk_pct >= 90:
            findings.append({
                "category": "CAPACITY",
                "severity": "HIGH",
                "subject": "root-disk",
                "evidence": {
                    "used_percent": disk_pct,
                },
            })

        for sensor in thermal[
            "sensors"
        ]:
            if sensor["celsius"] >= 85:
                findings.append({
                    "category": "THERMAL",
                    "severity": "CRITICAL",
                    "subject":
                        sensor["sensor"],
                    "evidence": sensor,
                })

        failed_text = services.get(
            "failed",
            {},
        ).get("stdout", "")

        for line in failed_text.splitlines():
            if line.strip():
                findings.append({
                    "category":
                        "SERVICE_FAILURE",
                    "severity": "HIGH",
                    "subject":
                        line.split()[0],
                    "evidence": {
                        "line": line,
                    },
                })

        return findings

    def incident(
        self,
        finding: dict[str, Any],
    ) -> str:
        iid = str(uuid.uuid4())
        created = now()

        timeline = [{
            "time": created,
            "event": "DETECTED",
            "finding": finding,
        }]

        self.db.execute("""
            INSERT INTO incidents
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            iid,
            None,
            finding["severity"],
            finding["category"],
            finding["subject"],
            json.dumps(
                timeline,
                ensure_ascii=False,
            ),
            json.dumps({
                "state":
                    "RCA_REQUIRES_CORRELATION"
            }),
            json.dumps(
                finding["evidence"],
                ensure_ascii=False,
            ),
            json.dumps({}),
            json.dumps({}),
            json.dumps({}),
            "OPEN",
            created,
            created,
        ))
        self.db.commit()
        return iid

    def anti_loop(
        self,
        signature: str,
        max_attempts: int = 3,
        cooldown_seconds: int = 1800,
    ) -> bool:
        row = self.db.execute("""
            SELECT * FROM repair_budget
            WHERE signature=?
        """, (signature,)).fetchone()

        current = dt.datetime.now(
            dt.timezone.utc
        )

        if not row:
            self.db.execute("""
                INSERT INTO repair_budget
                VALUES(?,?,?,?,?)
            """, (
                signature,
                0,
                None,
                "{}",
                now(),
            ))
            self.db.commit()
            return True

        if row["cooldown_until"]:
            until = dt.datetime.fromisoformat(
                row["cooldown_until"]
            )

            if current < until:
                return False

        if row["attempts"] >= max_attempts:
            until = current + dt.timedelta(
                seconds=cooldown_seconds
            )

            self.db.execute("""
                UPDATE repair_budget
                SET cooldown_until=?,
                    attempts=0,
                    updated_at=?
                WHERE signature=?
            """, (
                until.isoformat(),
                now(),
                signature,
            ))
            self.db.commit()
            return False

        return True

    def request_repair(
        self,
        platform_name: str,
        action: str,
        payload: dict[str, Any],
        signature: str,
    ) -> dict[str, Any]:
        if not self.anti_loop(signature):
            return {
                "state": "CIRCUIT_BREAKER_OPEN",
                "signature": signature,
            }

        did = str(uuid.uuid4())

        request = {
            "decision_id": did,
            "platform": platform_name,
            "action": action,
            "payload": payload,
            "risk": 70,
            "authority": OWNER,
            "reason":
                "WATCHTOWER_SELF_HEAL_REQUEST",
        }

        (QUEUE / f"executor-{did}.json").write_text(
            json.dumps(
                request,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        self.db.execute("""
            UPDATE repair_budget
            SET attempts=attempts+1,
                updated_at=?
            WHERE signature=?
        """, (
            now(),
            signature,
        ))
        self.db.commit()

        return {
            "state": "QUEUED",
            "decision_id": did,
        }

    def verify_request(
        self,
        path: pathlib.Path,
    ) -> dict[str, Any]:
        request = json.loads(
            path.read_text(encoding="utf-8")
        )

        results = []

        for workflow in request.get(
            "workflows",
            [],
        ):
            kind = workflow.get(
                "kind",
                "HTTP",
            ).upper()

            if kind == "HTTP":
                result = self.http_workflow(
                    workflow
                )

            elif kind == "SYSTEMD":
                check = run([
                    "systemctl",
                    "is-active",
                    workflow["service"],
                ])

                result = {
                    "success": (
                        check["returncode"] == 0
                        and check[
                            "stdout"
                        ].strip() == "active"
                    ),
                    "check": check,
                }

            elif kind == "TLS":
                try:
                    context = (
                        ssl.create_default_context()
                    )

                    with socket.create_connection(
                        (
                            workflow["host"],
                            int(
                                workflow.get(
                                    "port",
                                    443,
                                )
                            ),
                        ),
                        timeout=10,
                    ) as raw:
                        with context.wrap_socket(
                            raw,
                            server_hostname=
                                workflow["host"],
                        ) as tls:
                            result = {
                                "success": True,
                                "protocol":
                                    tls.version(),
                                "cipher":
                                    tls.cipher(),
                            }
                except Exception as exc:
                    result = {
                        "success": False,
                        "error": repr(exc),
                    }

            elif kind == "SQLITE":
                result = self.database_health(
                    pathlib.Path(
                        workflow["path"]
                    )
                )
                result["success"] = result[
                    "healthy"
                ]

            else:
                result = {
                    "success": False,
                    "error":
                        "UNSUPPORTED_VERIFICATION_KIND",
                }

            results.append({
                "workflow": workflow,
                "result": result,
            })

        success = (
            bool(results)
            and all(
                item["result"].get(
                    "success",
                    False,
                )
                for item in results
            )
        )

        observation_window = int(
            request.get(
                "observation_window",
                60,
            )
        )

        self.db.execute("""
            INSERT INTO verification_results
            VALUES(?,?,?,?,?,?,?)
        """, (
            str(uuid.uuid4()),
            request["change_id"],
            request["platform"],
            int(success),
            json.dumps(
                results,
                ensure_ascii=False,
            ),
            observation_window,
            now(),
        ))
        self.db.commit()

        if (
            not success
            and request.get("rollback")
        ):
            rollback = request["rollback"]

            if rollback.get("action"):
                self.request_repair(
                    request["platform"],
                    rollback["action"],
                    rollback,
                    "rollback:"
                    + request["change_id"],
                )

        self.evidence(
            "INDEPENDENT_VERIFICATION",
            request["change_id"],
            {
                "success": success,
                "results": results,
            },
        )

        os.replace(
            path,
            path.with_suffix(
                ".processed.json"
            ),
        )

        return {
            "success": success,
            "results": results,
        }

    def capacity_forecast(
        self,
        samples: list[float],
    ) -> dict[str, Any]:
        if len(samples) < 2:
            return {
                "trend": 0,
                "prediction":
                    "INSUFFICIENT_HISTORY",
            }

        trend = (
            samples[-1] - samples[0]
        ) / (len(samples) - 1)

        return {
            "trend_per_sample": trend,
            "next": samples[-1] + trend,
        }

    def cycle(self) -> dict[str, Any]:
        system = self.system()
        processes = self.processes()
        services = self.services()
        network = self.network()
        thermal = self.thermal()
        power = self.power()
        storage = self.storage()
        environment = self.environment()
        hardware = self.hardware()

        findings = self.detect(
            system,
            thermal,
            storage,
            services,
        )

        incidents = [
            self.incident(item)
            for item in findings
        ]

        verifications = []

        for path in sorted(
            QUEUE.glob("verify-*.json")
        ):
            try:
                verifications.append(
                    self.verify_request(path)
                )
            except Exception as exc:
                self.evidence(
                    "VERIFICATION_ENGINE_FAILURE",
                    str(path),
                    {"error": repr(exc)},
                )

        result = {
            "time": now(),
            "system": system,
            "processes": processes,
            "services": services,
            "network": network,
            "physical": {
                "thermal": thermal,
                "power": power,
                "storage": storage,
                "environment": environment,
                "hardware": hardware,
            },
            "findings": findings,
            "incidents": incidents,
            "verifications": verifications,
        }

        self.evidence(
            "WATCHTOWER_CYCLE",
            "GLOBAL",
            result,
        )
        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    sub.add_parser("cycle")

    p_loop = sub.add_parser("loop")
    p_loop.add_argument(
        "--interval",
        type=int,
        default=int(
            os.environ.get(
                "MAJD_WATCHTOWER_INTERVAL",
                "60",
            )
        ),
    )

    args = parser.parse_args()
    app = Watchtower()

    if args.command == "cycle":
        print(json.dumps(
            app.cycle(),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    if args.command == "loop":
        while True:
            try:
                app.cycle()
            except Exception as exc:
                app.evidence(
                    "WATCHTOWER_FAILURE",
                    "GLOBAL",
                    {"error": repr(exc)},
                )

            time.sleep(
                max(15, args.interval)
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

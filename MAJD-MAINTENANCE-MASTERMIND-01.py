#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD MAINTENANCE — FILE 01
MAJD-MAINTENANCE-MASTERMIND-01.py

SOVEREIGN GLOBAL MASTERMIND
ABSOLUTE AUTHORITY: SUPREME_OWNER

This is the governing intelligence plane for MAJD Maintenance.

Permanent cycle:
WORLD
→ DISCOVER
→ VERIFY OFFICIAL SOURCE
→ APPLICABILITY
→ IMPACT / RISK
→ BACKUP PLAN
→ BUILD / REBUILD PLAN
→ SECURITY / COMPATIBILITY GATE
→ EXECUTOR 02
→ INDEPENDENT VERIFIER 03
→ DEFENSE 04
→ PRODUCTION OBSERVATION
→ ROLLBACK / SELF-HEAL
→ LEARN
→ IMPROVE
→ REPEAT

NO FILE 05.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import platform
import shutil
import socket
import sqlite3
import subprocess
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass, asdict
from typing import Any, Optional


VERSION = "6.0.0"
OWNER = "SUPREME_OWNER"

ROOT = pathlib.Path(
    os.environ.get("MAJD_MAINTENANCE_STATE", "/var/lib/majd-maintenance")
).resolve()

DB = ROOT / "majd-maintenance.sqlite3"
EVIDENCE = ROOT / "evidence"
QUEUE = ROOT / "queue"
REGULATORY = ROOT / "regulatory"
STATE = ROOT / "state"

PRIMARY_FILES = (
    "MAJD-MAINTENANCE-MASTERMIND-01.py",
    "MAJD-MAINTENANCE-EXECUTOR-02.py",
    "MAJD-MAINTENANCE-RUNTIME-03.py",
    "MAJD-SOVEREIGN-CYBER-DEFENSE-04.py",
)

VISIBILITY = (
    "DIRECTLY_CONTROLLED",
    "DIRECTLY_OBSERVED",
    "PROVIDER_REPORTED",
    "CONTRACTUALLY_ASSURED",
    "NOT_VISIBLE",
    "NOT_APPLICABLE",
)

SECTOR_OVERLAYS = (
    "HEALTH",
    "FINANCE",
    "CHILDREN",
    "MEDIA",
    "COMMERCE",
    "HOSTING_CLOUD",
    "EMAIL_COMMUNICATIONS",
    "AI",
    "MARKETPLACE",
    "GAMING",
)

PHYSICAL_CHAIN = (
    "PHYSICAL_WORLD",
    "FACILITY",
    "POWER",
    "COOLING",
    "RACK",
    "HARDWARE",
    "NETWORK",
    "OS",
    "SOFTWARE",
    "DATA",
    "AI",
    "PLATFORM",
    "BUSINESS",
    "USER",
    "LAW",
)

LIFECYCLE = (
    "OBSERVE",
    "PREDICT_PREVENT",
    "DETECT",
    "CORRELATE",
    "DIAGNOSE",
    "DECIDE",
    "BACKUP",
    "REPAIR_WRITE_REAL_CODE",
    "BUILD_CONFIGURE",
    "REAL_EXECUTION",
    "INDEPENDENT_VERIFY",
    "DEPLOY_LAUNCH",
    "MONITOR",
    "PROTECT",
    "LEARN",
    "IMPROVE",
    "REPEAT",
)


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def stable_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def digest(value: Any) -> str:
    if not isinstance(value, (bytes, bytearray)):
        value = stable_json(value).encode()
    return hashlib.sha256(value).hexdigest()


def cmd(argv: list[str], timeout: int = 60) -> dict[str, Any]:
    try:
        p = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "argv": argv,
            "returncode": p.returncode,
            "stdout": p.stdout[-250000:],
            "stderr": p.stderr[-100000:],
        }
    except Exception as exc:
        return {
            "argv": argv,
            "returncode": -1,
            "stdout": "",
            "stderr": repr(exc),
        }


class Database:
    def __init__(self) -> None:
        for directory in (ROOT, EVIDENCE, QUEUE, REGULATORY, STATE):
            directory.mkdir(parents=True, exist_ok=True)

        self.db = sqlite3.connect(DB)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA synchronous=FULL")
        self.schema()

    def schema(self) -> None:
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS evidence(
            id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            subject TEXT NOT NULL,
            payload TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS resources(
            id TEXT PRIMARY KEY,
            kind TEXT NOT NULL,
            name TEXT NOT NULL,
            platform TEXT,
            location TEXT,
            criticality INTEGER NOT NULL DEFAULT 0,
            visibility TEXT NOT NULL,
            desired_state TEXT NOT NULL,
            observed_state TEXT NOT NULL,
            metadata TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(kind,name,location)
        );

        CREATE TABLE IF NOT EXISTS relationships(
            source_id TEXT NOT NULL,
            relation TEXT NOT NULL,
            target_id TEXT NOT NULL,
            metadata TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY(source_id,relation,target_id)
        );

        CREATE TABLE IF NOT EXISTS platforms(
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            countries TEXT NOT NULL,
            sectors TEXT NOT NULL,
            users TEXT NOT NULL,
            data_profile TEXT NOT NULL,
            ai_profile TEXT NOT NULL,
            payments_profile TEXT NOT NULL,
            email_profile TEXT NOT NULL,
            infrastructure_profile TEXT NOT NULL,
            product_profile TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS constitutions(
            id TEXT PRIMARY KEY,
            scope TEXT NOT NULL,
            platform TEXT,
            version INTEGER NOT NULL,
            body TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            active INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS policies(
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            scope TEXT NOT NULL,
            body TEXT NOT NULL,
            version INTEGER NOT NULL,
            active INTEGER NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS policy_results(
            id TEXT PRIMARY KEY,
            policy TEXT NOT NULL,
            subject TEXT NOT NULL,
            result TEXT NOT NULL,
            reasons TEXT NOT NULL,
            evidence TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS official_sources(
            id TEXT PRIMARY KEY,
            jurisdiction TEXT NOT NULL,
            authority TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            source_type TEXT NOT NULL,
            official_domains TEXT NOT NULL,
            last_hash TEXT,
            last_checked TEXT
        );

        CREATE TABLE IF NOT EXISTS source_snapshots(
            id TEXT PRIMARY KEY,
            source_id TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            body_path TEXT NOT NULL,
            headers TEXT NOT NULL,
            official_verified INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS regulatory_changes(
            id TEXT PRIMARY KEY,
            source_id TEXT NOT NULL,
            old_hash TEXT,
            new_hash TEXT NOT NULL,
            official_verified INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS applicability(
            id TEXT PRIMARY KEY,
            source_id TEXT NOT NULL,
            platform TEXT NOT NULL,
            result TEXT NOT NULL,
            reasons TEXT NOT NULL,
            impact TEXT NOT NULL,
            risk TEXT NOT NULL,
            review_status TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS regulatory_deadlines(
            id TEXT PRIMARY KEY,
            source_id TEXT NOT NULL,
            platform TEXT,
            deadline TEXT NOT NULL,
            requirement TEXT NOT NULL,
            state TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS data_assets(
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            name TEXT NOT NULL,
            classification TEXT NOT NULL,
            owner TEXT,
            purpose TEXT,
            lawful_basis TEXT,
            consent_model TEXT,
            residency TEXT,
            transfer_basis TEXT,
            retention TEXT,
            deletion_rule TEXT,
            source_of_truth TEXT,
            lineage TEXT NOT NULL,
            quality TEXT NOT NULL,
            processors TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ai_assets(
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            kind TEXT NOT NULL,
            name TEXT NOT NULL,
            provider TEXT,
            model TEXT,
            provenance TEXT NOT NULL,
            permissions TEXT NOT NULL,
            tools TEXT NOT NULL,
            evaluations TEXT NOT NULL,
            security TEXT NOT NULL,
            drift_state TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dependencies(
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            ecosystem TEXT NOT NULL,
            name TEXT NOT NULL,
            version TEXT,
            license TEXT,
            source TEXT,
            provenance TEXT NOT NULL,
            vulnerabilities TEXT NOT NULL,
            eol TEXT,
            compatibility TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS service_catalog(
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            service TEXT NOT NULL,
            owner TEXT,
            criticality INTEGER NOT NULL,
            requirements TEXT NOT NULL,
            dependencies TEXT NOT NULL,
            availability_target REAL,
            latency_target_ms REAL,
            continuity TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS quality_gates(
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            gate TEXT NOT NULL,
            checks TEXT NOT NULL,
            result TEXT NOT NULL,
            evidence TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS customer_journeys(
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            name TEXT NOT NULL,
            steps TEXT NOT NULL,
            critical INTEGER NOT NULL,
            expected_result TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS innovation(
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            idea TEXT NOT NULL,
            value_analysis TEXT NOT NULL,
            risk TEXT NOT NULL,
            compatibility TEXT NOT NULL,
            priority INTEGER NOT NULL,
            state TEXT NOT NULL,
            actual_value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS business_controls(
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            control_name TEXT NOT NULL,
            control_type TEXT NOT NULL,
            rule TEXT NOT NULL,
            evidence TEXT NOT NULL,
            state TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS physical_assets(
            id TEXT PRIMARY KEY,
            platform TEXT,
            asset_type TEXT NOT NULL,
            name TEXT NOT NULL,
            parent_id TEXT,
            visibility TEXT NOT NULL,
            desired_state TEXT NOT NULL,
            observed_state TEXT NOT NULL,
            supplier TEXT,
            model TEXT,
            serial TEXT,
            firmware TEXT,
            warranty TEXT,
            eol TEXT,
            replacement_lead_time TEXT,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS capacity(
            id TEXT PRIMARY KEY,
            platform TEXT,
            resource TEXT NOT NULL,
            capacity TEXT NOT NULL,
            usage TEXT NOT NULL,
            headroom TEXT NOT NULL,
            forecast TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS plans(
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            objective TEXT NOT NULL,
            discovery TEXT NOT NULL,
            applicability TEXT NOT NULL,
            impact TEXT NOT NULL,
            risk TEXT NOT NULL,
            backup TEXT NOT NULL,
            build TEXT NOT NULL,
            security TEXT NOT NULL,
            verification TEXT NOT NULL,
            deployment TEXT NOT NULL,
            rollback TEXT NOT NULL,
            state TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS decisions(
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            action TEXT NOT NULL,
            payload TEXT NOT NULL,
            authority TEXT NOT NULL,
            risk INTEGER NOT NULL,
            owner_required INTEGER NOT NULL,
            state TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS learning(
            id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            signature TEXT UNIQUE NOT NULL,
            knowledge TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """)
        self.db.commit()

    def evidence(
        self,
        category: str,
        subject: str,
        payload: Any,
    ) -> str:
        eid = str(uuid.uuid4())
        h = digest(payload)
        created = now()

        self.db.execute(
            "INSERT INTO evidence VALUES(?,?,?,?,?,?)",
            (eid, category, subject, stable_json(payload), h, created),
        )
        self.db.commit()

        (EVIDENCE / f"{created.replace(':','_')}-{eid}.json").write_text(
            json.dumps({
                "id": eid,
                "category": category,
                "subject": subject,
                "payload": payload,
                "sha256": h,
                "created_at": created,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return eid

    def resource(
        self,
        kind: str,
        name: str,
        location: str,
        observed: Any,
        *,
        platform_name: Optional[str] = None,
        desired: Any = None,
        criticality: int = 0,
        visibility: str = "DIRECTLY_OBSERVED",
        metadata: Any = None,
    ) -> str:
        if visibility not in VISIBILITY:
            raise ValueError("invalid physical/operational visibility")

        rid = digest([kind, name, location])[:32]

        self.db.execute("""
        INSERT INTO resources
        VALUES(?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(kind,name,location) DO UPDATE SET
            platform=excluded.platform,
            criticality=excluded.criticality,
            visibility=excluded.visibility,
            desired_state=excluded.desired_state,
            observed_state=excluded.observed_state,
            metadata=excluded.metadata,
            updated_at=excluded.updated_at
        """, (
            rid, kind, name, platform_name, location, criticality,
            visibility,
            stable_json(desired or {}),
            stable_json(observed),
            stable_json(metadata or {}),
            now(),
        ))
        self.db.commit()
        return rid


class WorldModel:
    def __init__(self, db: Database):
        self.db = db

    def host(self) -> dict[str, Any]:
        disk = shutil.disk_usage("/")
        state = {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "cpu_count": os.cpu_count(),
            "load": os.getloadavg(),
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
            },
        }
        self.db.resource(
            "HOST", socket.gethostname(), "local",
            state, criticality=10
        )
        return state

    def repositories(self) -> list[dict[str, Any]]:
        output = []
        for base in ("/root", "/srv", "/opt", "/var/www"):
            p = pathlib.Path(base)
            if not p.exists():
                continue

            try:
                children = list(p.iterdir())
            except PermissionError:
                continue

            for repo in children:
                if not repo.is_dir() or not (repo / ".git").exists():
                    continue

                state = {
                    "branch": cmd([
                        "git", "-C", str(repo),
                        "branch", "--show-current"
                    ])["stdout"].strip(),
                    "head": cmd([
                        "git", "-C", str(repo),
                        "rev-parse", "HEAD"
                    ])["stdout"].strip(),
                    "status": cmd([
                        "git", "-C", str(repo),
                        "status", "--porcelain"
                    ])["stdout"].splitlines(),
                    "remotes": cmd([
                        "git", "-C", str(repo),
                        "remote", "-v"
                    ])["stdout"].splitlines(),
                    "tags": cmd([
                        "git", "-C", str(repo),
                        "tag", "--list"
                    ])["stdout"].splitlines(),
                }

                self.db.resource(
                    "GIT_REPOSITORY",
                    repo.name,
                    str(repo),
                    state,
                    platform_name=repo.name,
                    criticality=8,
                )
                output.append({"name": repo.name, **state})
        return output

    def services(self) -> list[dict[str, Any]]:
        if not shutil.which("systemctl"):
            return []

        units = cmd([
            "systemctl", "list-units",
            "--type=service", "--all",
            "--no-pager", "--no-legend"
        ])

        result = []
        for line in units["stdout"].splitlines():
            if not line.strip():
                continue

            name = line.split()[0]
            show = cmd([
                "systemctl", "show", name,
                "--property=ActiveState,SubState,UnitFileState,FragmentPath"
            ])

            state = {}
            for item in show["stdout"].splitlines():
                if "=" in item:
                    k, v = item.split("=", 1)
                    state[k] = v

            self.db.resource(
                "SYSTEMD_SERVICE",
                name,
                state.get("FragmentPath", ""),
                state,
                criticality=6,
            )
            result.append({"name": name, **state})

        return result

    def network(self) -> dict[str, Any]:
        state = {
            "addresses": cmd(["ip", "-json", "address"])
            if shutil.which("ip") else {},
            "routes": cmd(["ip", "-json", "route"])
            if shutil.which("ip") else {},
            "listeners": cmd(["ss", "-lntup"])
            if shutil.which("ss") else {},
            "dns": (
                pathlib.Path("/etc/resolv.conf")
                .read_text(errors="replace")
                if pathlib.Path("/etc/resolv.conf").exists()
                else ""
            ),
        }
        self.db.resource(
            "NETWORK", "host-network", "local",
            state, criticality=9
        )
        return state

    def containers(self) -> dict[str, Any]:
        state = {}

        if shutil.which("docker"):
            state["docker"] = cmd([
                "docker", "ps", "-a", "--no-trunc"
            ])

        if shutil.which("podman"):
            state["podman"] = cmd([
                "podman", "ps", "-a", "--no-trunc"
            ])

        self.db.resource(
            "CONTAINERS", "container-runtime", "local",
            state,
            criticality=7,
            visibility=(
                "DIRECTLY_OBSERVED"
                if state else "NOT_VISIBLE"
            ),
        )
        return state

    def databases(self) -> list[dict[str, Any]]:
        found = []

        for base in ("/root", "/srv", "/opt", "/var/lib", "/var/www"):
            p = pathlib.Path(base)
            if not p.exists():
                continue

            try:
                for dbfile in p.glob("**/*.sqlite3"):
                    if len(found) >= 1000:
                        break
                    try:
                        st = dbfile.stat()
                    except Exception:
                        continue

                    state = {
                        "size": st.st_size,
                        "mtime": st.st_mtime,
                    }

                    self.db.resource(
                        "SQLITE",
                        dbfile.name,
                        str(dbfile),
                        state,
                        criticality=8,
                    )
                    found.append({
                        "path": str(dbfile),
                        **state,
                    })
            except (PermissionError, OSError):
                continue

        return found

    def schedulers(self) -> dict[str, Any]:
        state = {
            "crontab": (
                pathlib.Path("/etc/crontab")
                .read_text(errors="replace")
                if pathlib.Path("/etc/crontab").exists()
                else ""
            ),
            "cron_d": [],
            "systemd_timers": cmd([
                "systemctl", "list-timers",
                "--all", "--no-pager"
            ]) if shutil.which("systemctl") else {},
        }

        cron_d = pathlib.Path("/etc/cron.d")
        if cron_d.exists():
            for f in cron_d.iterdir():
                if f.is_file():
                    state["cron_d"].append({
                        "name": f.name,
                        "sha256": digest(f.read_bytes()),
                    })

        self.db.resource(
            "SCHEDULER", "schedulers", "local",
            state, criticality=6
        )
        return state

    def ai(self) -> dict[str, Any]:
        base = os.environ.get(
            "OLLAMA_BASE_URL",
            "http://127.0.0.1:11434"
        ).rstrip("/")

        state = {
            "ollama_base": base,
            "available": False,
            "models": [],
        }

        try:
            with urllib.request.urlopen(
                base + "/api/tags", timeout=3
            ) as r:
                body = json.loads(r.read())
                state["available"] = True
                state["models"] = body.get("models", [])
        except Exception as exc:
            state["error"] = repr(exc)

        self.db.resource(
            "AI_PROVIDER",
            "ollama",
            base,
            state,
            criticality=7,
            visibility=(
                "DIRECTLY_OBSERVED"
                if state["available"]
                else "NOT_VISIBLE"
            ),
        )
        return state

    def physical(self) -> dict[str, Any]:
        capabilities = {
            "thermal": pathlib.Path("/sys/class/thermal").exists(),
            "hwmon": pathlib.Path("/sys/class/hwmon").exists(),
            "power_supply": pathlib.Path("/sys/class/power_supply").exists(),
            "edac_ecc": pathlib.Path("/sys/devices/system/edac").exists(),
            "smart": bool(shutil.which("smartctl")),
            "nvme": bool(shutil.which("nvme")),
            "sensors": bool(shutil.which("sensors")),
            "ipmi": bool(shutil.which("ipmitool")),
            "redfish": bool(os.environ.get("MAJD_REDFISH_ENDPOINT")),
            "ups": bool(shutil.which("upsc")),
        }

        for name, available in capabilities.items():
            self.db.resource(
                "PHYSICAL_CAPABILITY",
                name,
                "local",
                {"available": available},
                visibility=(
                    "DIRECTLY_OBSERVED"
                    if available else "NOT_VISIBLE"
                ),
            )

        return capabilities

    def discover(self) -> dict[str, Any]:
        state = {
            "host": self.host(),
            "repositories": self.repositories(),
            "services": self.services(),
            "network": self.network(),
            "containers": self.containers(),
            "databases": self.databases(),
            "schedulers": self.schedulers(),
            "ai": self.ai(),
            "physical": self.physical(),
        }
        self.db.evidence("WORLD_MODEL", "discovery", state)
        return state


class Constitution:
    def __init__(self, db: Database):
        self.db = db

    def install(self) -> str:
        body = {
            "authority": OWNER,
            "primary_files": PRIMARY_FILES,
            "manual_file_05_forbidden": True,
            "real_execution": True,
            "fake_success_forbidden": True,
            "todo_pass_as_completion_forbidden": True,
            "scan_report_only_forbidden": True,
            "latest_equals_install_forbidden": True,
            "independent_verification_required": True,
            "critical_workflow_verification_required": True,
            "backup_before_mutation": True,
            "restore_verification_required": True,
            "rollback_required": True,
            "legal_uncertainty": "LEGAL_REVIEW_REQUIRED",
            "external_reality":
                "EXTERNAL_DEPENDENCY_REQUIRED",
            "physical_visibility": VISIBILITY,
            "physical_chain": PHYSICAL_CHAIN,
            "sector_overlays": SECTOR_OVERLAYS,
            "lifecycle": LIFECYCLE,
            "hardware_reality_rule": (
                "Never claim a physical capability or healthy "
                "physical state without direct telemetry, provider "
                "evidence or contractual evidence."
            ),
            "cyber_physical_safety": (
                "LLM MAY REASON — SAFETY CONTROLLER "
                "ENFORCES PHYSICAL LIMITS"
            ),
        }

        previous = self.db.db.execute("""
            SELECT MAX(version) FROM constitutions
            WHERE scope='GLOBAL'
        """).fetchone()[0]

        version = int(previous or 0) + 1
        cid = str(uuid.uuid4())

        self.db.db.execute(
            "UPDATE constitutions SET active=0 WHERE scope='GLOBAL'"
        )

        self.db.db.execute("""
            INSERT INTO constitutions
            VALUES(?,?,?,?,?,?,?,?)
        """, (
            cid,
            "GLOBAL",
            None,
            version,
            stable_json(body),
            digest(body),
            1,
            now(),
        ))
        self.db.db.commit()

        self.db.evidence(
            "CONSTITUTION",
            "GLOBAL",
            {"id": cid, "version": version, "body": body},
        )
        return cid

    def platform(
        self,
        platform_name: str,
        body: dict[str, Any],
    ) -> str:
        previous = self.db.db.execute("""
            SELECT MAX(version) FROM constitutions
            WHERE scope='PLATFORM' AND platform=?
        """, (platform_name,)).fetchone()[0]

        version = int(previous or 0) + 1
        cid = str(uuid.uuid4())

        self.db.db.execute("""
            UPDATE constitutions SET active=0
            WHERE scope='PLATFORM' AND platform=?
        """, (platform_name,))

        self.db.db.execute("""
            INSERT INTO constitutions
            VALUES(?,?,?,?,?,?,?,?)
        """, (
            cid,
            "PLATFORM",
            platform_name,
            version,
            stable_json(body),
            digest(body),
            1,
            now(),
        ))
        self.db.db.commit()
        return cid


class PolicyEngine:
    def __init__(self, db: Database):
        self.db = db

    def set(
        self,
        name: str,
        scope: str,
        body: dict[str, Any],
    ) -> None:
        row = self.db.db.execute(
            "SELECT version FROM policies WHERE name=?",
            (name,),
        ).fetchone()

        version = int(row["version"]) + 1 if row else 1
        pid = digest(name)[:32]

        self.db.db.execute("""
        INSERT INTO policies VALUES(?,?,?,?,?,?,?)
        ON CONFLICT(name) DO UPDATE SET
            scope=excluded.scope,
            body=excluded.body,
            version=excluded.version,
            active=1,
            updated_at=excluded.updated_at
        """, (
            pid, name, scope,
            stable_json(body), version, 1, now()
        ))
        self.db.db.commit()

    def evaluate(
        self,
        policy_name: str,
        subject: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        row = self.db.db.execute("""
            SELECT * FROM policies
            WHERE name=? AND active=1
        """, (policy_name,)).fetchone()

        if not row:
            return {
                "result": "DENIED",
                "reasons": ["POLICY_NOT_FOUND"],
            }

        policy = json.loads(row["body"])
        reasons = []
        result = "APPROVED"

        for key, expected in policy.get("required", {}).items():
            if context.get(key) != expected:
                result = "DENIED"
                reasons.append(
                    f"REQUIRED:{key}={expected!r}"
                )

        for key, forbidden in policy.get("forbidden", {}).items():
            if context.get(key) == forbidden:
                result = "DENIED"
                reasons.append(
                    f"FORBIDDEN:{key}={forbidden!r}"
                )

        if context.get("legal_uncertainty"):
            result = "LEGAL_REVIEW_REQUIRED"
            reasons.append("UNRESOLVED_LEGAL_INTERPRETATION")

        if context.get("external_dependency_missing"):
            result = "EXTERNAL_DEPENDENCY_REQUIRED"
            reasons.append("REAL_EXTERNAL_DEPENDENCY_MISSING")

        if context.get("owner_approval_required"):
            result = "OWNER_ACTION_REQUIRED"
            reasons.append("SUPREME_OWNER_APPROVAL_REQUIRED")

        rid = str(uuid.uuid4())

        self.db.db.execute("""
            INSERT INTO policy_results
            VALUES(?,?,?,?,?,?,?)
        """, (
            rid,
            policy_name,
            subject,
            result,
            stable_json(reasons),
            stable_json(context),
            now(),
        ))
        self.db.db.commit()

        return {"result": result, "reasons": reasons}


class RegulatoryBrain:
    def __init__(self, db: Database):
        self.db = db

    def register(
        self,
        jurisdiction: str,
        authority: str,
        title: str,
        url: str,
        source_type: str,
        official_domains: list[str],
    ) -> str:
        sid = digest(url)[:32]

        self.db.db.execute("""
        INSERT INTO official_sources
        VALUES(?,?,?,?,?,?,?,?,?)
        ON CONFLICT(url) DO UPDATE SET
            jurisdiction=excluded.jurisdiction,
            authority=excluded.authority,
            title=excluded.title,
            source_type=excluded.source_type,
            official_domains=excluded.official_domains
        """, (
            sid,
            jurisdiction,
            authority,
            title,
            url,
            source_type,
            stable_json(official_domains),
            None,
            None,
        ))
        self.db.db.commit()
        return sid

    def verify_domain(
        self,
        url: str,
        allowed: list[str],
    ) -> bool:
        parsed = urllib.parse.urlparse(url)
        host = (parsed.hostname or "").lower()

        if parsed.scheme != "https":
            return False

        return any(
            host == domain.lower()
            or host.endswith("." + domain.lower())
            for domain in allowed
        )

    def fetch(self, source_id: str) -> dict[str, Any]:
        row = self.db.db.execute("""
            SELECT * FROM official_sources WHERE id=?
        """, (source_id,)).fetchone()

        if not row:
            raise KeyError(source_id)

        allowed = json.loads(row["official_domains"])
        official = self.verify_domain(row["url"], allowed)

        if not official:
            result = {
                "state": "DENIED",
                "reason": "OFFICIAL_DOMAIN_VERIFICATION_FAILED",
            }
            self.db.evidence(
                "REGULATORY_SOURCE_REJECTED",
                row["title"],
                result,
            )
            return result

        request = urllib.request.Request(
            row["url"],
            headers={
                "User-Agent":
                    f"MAJD-Maintenance-Regulatory/{VERSION}"
            },
        )

        try:
            with urllib.request.urlopen(
                request, timeout=30
            ) as response:
                body = response.read(20 * 1024 * 1024)
                headers = dict(response.headers.items())
        except Exception as exc:
            result = {
                "state": "FETCH_FAILED",
                "error": repr(exc),
            }
            self.db.evidence(
                "REGULATORY_FETCH_FAILURE",
                row["title"],
                result,
            )
            return result

        new_hash = digest(body)
        old_hash = row["last_hash"]
        snapshot_id = str(uuid.uuid4())
        body_path = REGULATORY / f"{snapshot_id}.bin"
        body_path.write_bytes(body)

        self.db.db.execute("""
            INSERT INTO source_snapshots
            VALUES(?,?,?,?,?,?,?)
        """, (
            snapshot_id,
            source_id,
            new_hash,
            str(body_path),
            stable_json(headers),
            1,
            now(),
        ))

        self.db.db.execute("""
            UPDATE official_sources
            SET last_hash=?,last_checked=?
            WHERE id=?
        """, (new_hash, now(), source_id))

        changed = bool(old_hash and old_hash != new_hash)

        if changed:
            self.db.db.execute("""
                INSERT INTO regulatory_changes
                VALUES(?,?,?,?,?,?)
            """, (
                str(uuid.uuid4()),
                source_id,
                old_hash,
                new_hash,
                1,
                now(),
            ))

        self.db.db.commit()

        result = {
            "official_verified": True,
            "changed": changed,
            "old_hash": old_hash,
            "new_hash": new_hash,
            "snapshot": str(body_path),
        }

        self.db.evidence(
            "REGULATORY_FETCH",
            row["title"],
            result,
        )
        return result

    def applicability(
        self,
        source_id: str,
        platform_name: str,
        profile: dict[str, Any],
    ) -> dict[str, Any]:
        source = self.db.db.execute("""
            SELECT * FROM official_sources WHERE id=?
        """, (source_id,)).fetchone()

        if not source:
            raise KeyError(source_id)

        countries = {
            str(x).upper()
            for x in profile.get("countries", [])
        }
        sectors = {
            str(x).upper()
            for x in profile.get("sectors", [])
        }

        jurisdiction = source["jurisdiction"].upper()
        reasons = []

        if jurisdiction in {"GLOBAL", "INTERNATIONAL"}:
            reasons.append("GLOBAL_SOURCE")
        elif jurisdiction in countries:
            reasons.append("JURISDICTION_MATCH")

        title_upper = source["title"].upper()
        matched = [
            sector for sector in sectors
            if sector.replace("_", " ") in title_upper
        ]

        if matched:
            reasons.append(
                "SECTOR_MATCH:" + ",".join(matched)
            )

        impact = {
            "privacy": bool(profile.get("data")),
            "cross_border": bool(
                profile.get("cross_border_data")
            ),
            "ai": bool(profile.get("ai")),
            "payments": bool(profile.get("payments")),
            "children": "CHILDREN" in sectors,
            "commerce": "COMMERCE" in sectors,
            "hosting_cloud": "HOSTING_CLOUD" in sectors,
            "email": "EMAIL_COMMUNICATIONS" in sectors,
        }

        risk_score = min(
            100,
            15
            + 10 * len(reasons)
            + 8 * sum(bool(v) for v in impact.values())
        )

        if not reasons:
            result = "NOT_APPLICABLE"
            review = "COMPLETED"
        elif source["source_type"].upper() in {
            "LAW",
            "REGULATION",
            "CONTROL",
            "STANDARD",
            "OFFICIAL_GUIDANCE",
        }:
            result = "APPLICABILITY_CANDIDATE"
            review = "REQUIRES_REQUIREMENT_EXTRACTION"
        else:
            result = "LEGAL_REVIEW_REQUIRED"
            review = "LEGAL_REVIEW_REQUIRED"

        record = {
            "result": result,
            "reasons": reasons,
            "impact": impact,
            "risk": {"score": risk_score},
            "review_status": review,
        }

        self.db.db.execute("""
            INSERT INTO applicability
            VALUES(?,?,?,?,?,?,?,?,?)
        """, (
            str(uuid.uuid4()),
            source_id,
            platform_name,
            result,
            stable_json(reasons),
            stable_json(impact),
            stable_json({"score": risk_score}),
            review,
            now(),
        ))
        self.db.db.commit()

        return record


class DataGovernance:
    def __init__(self, db: Database):
        self.db = db

    @staticmethod
    def classification(name: str) -> str:
        n = name.lower()

        if any(x in n for x in (
            "password", "secret", "private_key",
            "access_token", "refresh_token"
        )):
            return "SECRET"

        if any(x in n for x in (
            "card", "payment", "invoice",
            "transaction", "bank"
        )):
            return "FINANCIAL"

        if any(x in n for x in (
            "email", "phone", "address",
            "location", "birth", "name",
            "device_id", "ip_address"
        )):
            return "PERSONAL"

        return "INTERNAL"

    def inspect_sqlite(
        self,
        platform_name: str,
        path: pathlib.Path,
    ) -> list[dict[str, Any]]:
        if not path.exists():
            return []

        db = sqlite3.connect(
            f"file:{path}?mode=ro",
            uri=True,
        )

        tables = [
            row[0]
            for row in db.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table'
            """)
        ]

        result = []

        for table in tables:
            safe = table.replace('"', '""')
            columns = db.execute(
                f'PRAGMA table_info("{safe}")'
            ).fetchall()

            column_data = [{
                "name": c[1],
                "type": c[2],
                "classification":
                    self.classification(c[1]),
            } for c in columns]

            classes = {
                x["classification"]
                for x in column_data
            }

            overall = (
                "SECRET" if "SECRET" in classes
                else "FINANCIAL" if "FINANCIAL" in classes
                else "PERSONAL" if "PERSONAL" in classes
                else "INTERNAL"
            )

            quality = {
                "accuracy": "REQUIRES_DOMAIN_RULES",
                "completeness": "MEASURABLE",
                "consistency": "MEASURABLE",
                "freshness": "MEASURABLE",
                "uniqueness": "MEASURABLE",
                "traceability": True,
                "source_of_truth_required": True,
                "reconciliation_required": (
                    overall == "FINANCIAL"
                ),
            }

            asset_id = str(uuid.uuid4())

            self.db.db.execute("""
                INSERT INTO data_assets
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                asset_id,
                platform_name,
                f"{path.name}:{table}",
                overall,
                OWNER,
                "PLATFORM_CONSTITUTION_REQUIRED",
                None,
                "PLATFORM_CONSTITUTION_REQUIRED",
                "DISCOVERED_LOCATION",
                (
                    "TRANSFER_BASIS_REGISTRY_REQUIRED"
                    if overall in {"PERSONAL", "FINANCIAL"}
                    else "NOT_APPLICABLE"
                ),
                "RETENTION_POLICY_REQUIRED",
                "DELETION_PROPAGATION_REQUIRED",
                str(path),
                stable_json({"columns": column_data}),
                stable_json(quality),
                stable_json([]),
                now(),
            ))

            result.append({
                "table": table,
                "classification": overall,
                "columns": column_data,
                "quality": quality,
            })

        db.close()
        self.db.db.commit()
        return result


class AIGovernance:
    def __init__(self, db: Database):
        self.db = db

    def register(
        self,
        platform_name: str,
        kind: str,
        name: str,
        provider: Optional[str],
        model: Optional[str],
        provenance: dict[str, Any],
        permissions: dict[str, Any],
        tools: list[str],
    ) -> str:
        aid = str(uuid.uuid4())

        security = {
            "prompt_injection_defense": True,
            "data_leakage_prevention": True,
            "secret_exfiltration_forbidden": True,
            "tool_boundary_enforced": True,
            "owner_boundary": OWNER,
            "unsafe_shell_forbidden": True,
            "generated_code_requires_verification": True,
            "destructive_actions_policy_gated": True,
            "untrusted_context_not_authoritative": True,
        }

        evaluations = {
            "functional": "REQUIRED",
            "security": "REQUIRED",
            "regression": "REQUIRED",
            "red_team": "REQUIRED_WHEN_APPLICABLE",
            "drift": "CONTINUOUS",
        }

        self.db.db.execute("""
            INSERT INTO ai_assets
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            aid,
            platform_name,
            kind,
            name,
            provider,
            model,
            stable_json(provenance),
            stable_json(permissions),
            stable_json(tools),
            stable_json(evaluations),
            stable_json(security),
            "MONITORED",
            now(),
        ))
        self.db.db.commit()
        return aid


class QualityManagement:
    def __init__(self, db: Database):
        self.db = db

    def product_gate(
        self,
        platform_name: str,
        checks: dict[str, bool],
    ) -> dict[str, Any]:
        required = (
            "backend",
            "ui",
            "api",
            "permissions",
            "persistence",
            "critical_workflows",
            "error_handling",
            "security",
            "independent_verification",
            "deployment",
            "post_launch_monitoring",
        )

        missing = [
            key for key in required
            if not checks.get(key, False)
        ]

        result = (
            "READY_FOR_LAUNCH"
            if not missing
            else "NOT_READY_FOR_LAUNCH"
        )

        gate_id = str(uuid.uuid4())

        self.db.db.execute("""
            INSERT INTO quality_gates
            VALUES(?,?,?,?,?,?,?)
        """, (
            gate_id,
            platform_name,
            "MAJD_PRODUCT_QUALITY_GATE",
            stable_json(checks),
            result,
            stable_json({"missing": missing}),
            now(),
        ))
        self.db.db.commit()

        return {
            "result": result,
            "missing": missing,
        }

    def service(
        self,
        platform_name: str,
        service: str,
        criticality: int,
        requirements: dict[str, Any],
        dependencies: list[str],
        continuity: dict[str, Any],
    ) -> str:
        sid = str(uuid.uuid4())

        self.db.db.execute("""
            INSERT INTO service_catalog
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """, (
            sid,
            platform_name,
            service,
            OWNER,
            criticality,
            stable_json(requirements),
            stable_json(dependencies),
            requirements.get("availability_target"),
            requirements.get("latency_target_ms"),
            stable_json(continuity),
            now(),
        ))
        self.db.db.commit()
        return sid

    def customer_journey(
        self,
        platform_name: str,
        name: str,
        steps: list[dict[str, Any]],
        expected_result: str,
        critical: bool = True,
    ) -> str:
        jid = str(uuid.uuid4())

        self.db.db.execute("""
            INSERT INTO customer_journeys
            VALUES(?,?,?,?,?,?,?)
        """, (
            jid,
            platform_name,
            name,
            stable_json(steps),
            int(critical),
            expected_result,
            now(),
        ))
        self.db.db.commit()
        return jid

    def innovation(
        self,
        platform_name: str,
        idea: str,
        value: dict[str, Any],
        risk: dict[str, Any],
        compatibility: dict[str, Any],
        priority: int,
    ) -> str:
        iid = str(uuid.uuid4())

        self.db.db.execute("""
            INSERT INTO innovation
            VALUES(?,?,?,?,?,?,?,?,?,?)
        """, (
            iid,
            platform_name,
            idea,
            stable_json(value),
            stable_json(risk),
            stable_json(compatibility),
            priority,
            "DISCOVERED",
            stable_json({}),
            now(),
        ))
        self.db.db.commit()
        return iid


class PhysicalIntelligence:
    def __init__(self, db: Database):
        self.db = db

    def register(
        self,
        asset_type: str,
        name: str,
        *,
        platform_name: Optional[str] = None,
        parent_id: Optional[str] = None,
        visibility: str = "NOT_VISIBLE",
        desired: Any = None,
        observed: Any = None,
        supplier: Optional[str] = None,
        model: Optional[str] = None,
        serial: Optional[str] = None,
        firmware: Optional[str] = None,
        warranty: Optional[str] = None,
        eol: Optional[str] = None,
        replacement_lead_time: Optional[str] = None,
    ) -> str:
        if visibility not in VISIBILITY:
            raise ValueError("invalid visibility")

        aid = str(uuid.uuid4())

        self.db.db.execute("""
            INSERT INTO physical_assets
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            aid,
            platform_name,
            asset_type,
            name,
            parent_id,
            visibility,
            stable_json(desired or {}),
            stable_json(observed or {}),
            supplier,
            model,
            serial,
            firmware,
            warranty,
            eol,
            replacement_lead_time,
            now(),
        ))
        self.db.db.commit()
        return aid

    def capacity_gate(
        self,
        platform_name: str,
        requirements: dict[str, float],
        observed: dict[str, float],
    ) -> dict[str, Any]:
        checks = {}
        allowed = True

        for key, required in requirements.items():
            available = float(observed.get(key, 0))
            ok = available >= float(required)
            checks[key] = {
                "required": required,
                "available": available,
                "ok": ok,
            }
            allowed = allowed and ok

        return {
            "allowed": allowed,
            "checks": checks,
            "rule": (
                "Workload placement is denied when physical "
                "or infrastructure headroom is insufficient."
            ),
        }


class Planner:
    def __init__(
        self,
        db: Database,
        policy: PolicyEngine,
    ):
        self.db = db
        self.policy = policy

    def plan(
        self,
        platform_name: str,
        objective: str,
    ) -> str:
        resources = [
            dict(row)
            for row in self.db.db.execute("""
                SELECT * FROM resources
                WHERE platform=? OR platform IS NULL
            """, (platform_name,))
        ]

        lower = objective.lower()
        risk = 10

        high_risk = (
            "delete",
            "drop",
            "database",
            "migration",
            "payment",
            "dns",
            "tls",
            "certificate",
            "firewall",
            "identity",
            "secret",
            "production",
            "firmware",
            "power",
            "storage",
            "decommission",
        )

        matched = [
            item for item in high_risk
            if item in lower
        ]

        risk += len(matched) * 8
        risk += min(
            30,
            sum(
                1 for resource in resources
                if resource["criticality"] >= 8
            ) * 4,
        )
        risk = min(risk, 100)

        plan_id = str(uuid.uuid4())

        discovery = {
            "resource_count": len(resources),
            "knowledge_graph_required": True,
            "critical_workflows_required": True,
            "data_flows_required": True,
            "trust_boundaries_required": True,
            "failure_domains_required": True,
        }

        applicability = {
            "regulatory_check_required": True,
            "sector_overlay_required": True,
            "country_overlay_required": True,
            "data_residency_required": True,
        }

        impact = {
            "blast_radius_required": True,
            "dependencies_required": True,
            "business_impact_required": True,
            "physical_impact_required": True,
        }

        build = {
            "refactor_allowed": True,
            "rebuild_allowed": True,
            "modernization_allowed": True,
            "dependency_upgrade_allowed": True,
            "migration_allowed": True,
            "architecture_improvement_allowed": True,
            "performance_optimization_allowed": True,
            "security_hardening_required": True,
            "ui_ux_allowed": True,
            "database_api_evolution_allowed": True,
        }

        security = {
            "zero_trust": True,
            "supply_chain": True,
            "secret_check": True,
            "ai_tool_boundary": True,
            "file_integrity": True,
            "vulnerability_check": True,
        }

        verification = {
            "independent": True,
            "critical_workflow": True,
            "product_quality": True,
            "data_quality": True,
            "security": True,
            "restore": True,
            "production_observation": True,
        }

        deployment = {
            "progressive": True,
            "maintenance_window_when_required": True,
            "dependency_ordering": True,
            "go_no_go_evidence": True,
        }

        rollback = {
            "automatic_on_failed_verification": True,
            "backup_reference_required": True,
            "restore_verification_required": True,
        }

        self.db.db.execute("""
            INSERT INTO plans
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            plan_id,
            platform_name,
            objective,
            stable_json(discovery),
            stable_json(applicability),
            stable_json(impact),
            stable_json({
                "score": risk,
                "matched": matched,
            }),
            stable_json({
                "required": True,
                "restore_verification": True,
            }),
            stable_json(build),
            stable_json(security),
            stable_json(verification),
            stable_json(deployment),
            stable_json(rollback),
            "PLANNED",
            now(),
        ))
        self.db.db.commit()

        self.db.evidence(
            "ENGINEERING_PLAN",
            plan_id,
            {
                "platform": platform_name,
                "objective": objective,
                "risk": risk,
            },
        )
        return plan_id

    def queue(
        self,
        platform_name: str,
        action: str,
        payload: dict[str, Any],
        risk: int,
        owner_required: bool = False,
    ) -> str:
        did = str(uuid.uuid4())

        state = (
            "OWNER_ACTION_REQUIRED"
            if owner_required
            else "QUEUED"
        )

        self.db.db.execute("""
            INSERT INTO decisions
            VALUES(?,?,?,?,?,?,?,?,?)
        """, (
            did,
            platform_name,
            action,
            stable_json(payload),
            OWNER,
            risk,
            int(owner_required),
            state,
            now(),
        ))
        self.db.db.commit()

        if not owner_required:
            (QUEUE / f"executor-{did}.json").write_text(
                json.dumps({
                    "decision_id": did,
                    "platform": platform_name,
                    "action": action,
                    "payload": payload,
                    "risk": risk,
                    "authority": OWNER,
                }, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        return did


class Mastermind:
    def __init__(self):
        self.db = Database()
        self.world = WorldModel(self.db)
        self.constitution = Constitution(self.db)
        self.policy = PolicyEngine(self.db)
        self.regulatory = RegulatoryBrain(self.db)
        self.data = DataGovernance(self.db)
        self.ai = AIGovernance(self.db)
        self.quality = QualityManagement(self.db)
        self.physical = PhysicalIntelligence(self.db)
        self.planner = Planner(self.db, self.policy)

    def bootstrap(self) -> dict[str, Any]:
        constitution_id = self.constitution.install()

        self.policy.set(
            "PRODUCTION_CHANGE_GATE",
            "GLOBAL",
            {
                "required": {
                    "impact_assessed": True,
                    "risk_assessed": True,
                    "backup_verified": True,
                    "compatibility_verified": True,
                    "security_verified": True,
                },
                "forbidden": {
                    "latest_equals_install": True,
                    "fake_success": True,
                },
            },
        )

        self.policy.set(
            "PRODUCT_COMPLETENESS",
            "GLOBAL",
            {
                "required": {
                    "backend": True,
                    "ui": True,
                    "api": True,
                    "permissions": True,
                    "persistence": True,
                    "critical_workflows": True,
                    "independent_verification": True,
                }
            },
        )

        self.policy.set(
            "OWNER_SUPREMACY",
            "GLOBAL",
            {
                "required": {
                    "authority": OWNER,
                },
                "forbidden": {
                    "agent_overrides_owner": True,
                },
            },
        )

        self.policy.set(
            "PHYSICAL_SAFETY",
            "GLOBAL",
            {
                "required": {
                    "sensor_trust_checked": True,
                    "deterministic_safety_controller": True,
                }
            },
        )

        return {
            "version": VERSION,
            "authority": OWNER,
            "constitution": constitution_id,
            "primary_files": PRIMARY_FILES,
            "file_05": "FORBIDDEN",
            "lifecycle": LIFECYCLE,
            "physical_chain": PHYSICAL_CHAIN,
        }

    def cycle(self) -> dict[str, Any]:
        world = self.world.discover()

        result = {
            "started": now(),
            "world": world,
            "regulatory_sources":
                self.db.db.execute(
                    "SELECT COUNT(*) FROM official_sources"
                ).fetchone()[0],
            "pending_regulatory_changes":
                self.db.db.execute(
                    "SELECT COUNT(*) FROM regulatory_changes"
                ).fetchone()[0],
            "platforms":
                self.db.db.execute(
                    "SELECT COUNT(*) FROM platforms"
                ).fetchone()[0],
            "data_assets":
                self.db.db.execute(
                    "SELECT COUNT(*) FROM data_assets"
                ).fetchone()[0],
            "ai_assets":
                self.db.db.execute(
                    "SELECT COUNT(*) FROM ai_assets"
                ).fetchone()[0],
            "physical_assets":
                self.db.db.execute(
                    "SELECT COUNT(*) FROM physical_assets"
                ).fetchone()[0],
            "finished": now(),
        }

        self.db.evidence(
            "MASTERMIND_CYCLE",
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

    sub.add_parser("bootstrap")
    sub.add_parser("discover")
    sub.add_parser("cycle")

    p_plan = sub.add_parser("plan")
    p_plan.add_argument("platform")
    p_plan.add_argument("objective")

    p_source = sub.add_parser("register-source")
    p_source.add_argument("jurisdiction")
    p_source.add_argument("authority")
    p_source.add_argument("title")
    p_source.add_argument("url")
    p_source.add_argument("source_type")
    p_source.add_argument("official_domains", nargs="+")

    p_fetch = sub.add_parser("fetch-source")
    p_fetch.add_argument("source_id")

    p_loop = sub.add_parser("loop")
    p_loop.add_argument(
        "--interval",
        type=int,
        default=int(
            os.environ.get(
                "MAJD_MASTERMIND_INTERVAL",
                "3600",
            )
        ),
    )

    args = parser.parse_args()
    app = Mastermind()

    if args.command == "bootstrap":
        print(json.dumps(
            app.bootstrap(),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    if args.command == "discover":
        print(json.dumps(
            app.world.discover(),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    if args.command == "cycle":
        print(json.dumps(
            app.cycle(),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    if args.command == "plan":
        print(app.planner.plan(
            args.platform,
            args.objective,
        ))
        return 0

    if args.command == "register-source":
        print(app.regulatory.register(
            args.jurisdiction,
            args.authority,
            args.title,
            args.url,
            args.source_type,
            args.official_domains,
        ))
        return 0

    if args.command == "fetch-source":
        print(json.dumps(
            app.regulatory.fetch(args.source_id),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    if args.command == "loop":
        app.bootstrap()
        import time
        while True:
            try:
                app.cycle()
            except Exception as exc:
                app.db.evidence(
                    "MASTERMIND_FAILURE",
                    "GLOBAL",
                    {"error": repr(exc)},
                )
            time.sleep(max(60, args.interval))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

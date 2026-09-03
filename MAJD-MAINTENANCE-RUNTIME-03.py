#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
======================================================================
MAJD COMPREHENSIVE MAINTENANCE CENTER
MAJD-MAINTENANCE-RUNTIME-03.py
======================================================================

FILE 03 — SOVEREIGN CONTINUOUS RUNTIME + WATCHTOWER
VERSION 1.0.0

ABSOLUTE AUTHORITY:
    SUPREME_OWNER

ROLE:
    Permanent runtime and independent verification layer for:

    01 — MAJD-MAINTENANCE-MASTERMIND-01.py
    02 — MAJD-MAINTENANCE-EXECUTOR-02.py

RESPONSIBILITIES:
    - Continuous runtime loop
    - Platform discovery
    - Platform inventory
    - Service discovery
    - Process discovery
    - Port discovery
    - HTTP/TCP verification
    - Critical workflow verification
    - Independent verification of executor evidence
    - Execution request supervision
    - Failure detection
    - Self-healing request generation
    - Incident creation
    - Event correlation
    - Anti-loop protection
    - Crash recovery
    - Runtime state persistence
    - Platform lifecycle tracking
    - Policy/regulatory intelligence scheduling
    - Regulatory source registry
    - Deadline registry
    - Policy drift scheduling
    - Security posture scheduling
    - Dependency/EOL scheduling
    - Certificate lifecycle scheduling
    - Backup/restore verification scheduling
    - Performance/capacity scheduling
    - Continuous development scheduling
    - Post-launch guardian
    - Audit/evidence ledger

TRUTH RULES:
    - No fake success.
    - systemd active != end-to-end healthy.
    - HTTP 200 alone != business workflow healthy.
    - Executor 02 cannot independently certify itself.
    - Runtime 03 validates evidence and observable outcome.
    - Missing external credentials remain missing.
    - Missing government/regulatory source connectivity is reported.
    - Legal applicability is never invented.
    - Legal interpretation requiring counsel is marked accordingly.
    - Destructive recovery is not performed blindly.
    - Owner remains the highest authority.
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
import hashlib
import json
import logging
import os
import pathlib
import re
import shutil
import signal
import socket
import sqlite3
import subprocess
import sys
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import uuid

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


# ======================================================================
# IDENTITY / PATHS
# ======================================================================

APP_NAME = "MAJD COMPREHENSIVE MAINTENANCE CENTER"
FILE_NAME = "MAJD-MAINTENANCE-RUNTIME-03.py"
VERSION = "1.0.0"
SCHEMA_VERSION = 1

SUPREME_AUTHORITY = "SUPREME_OWNER"

PROJECT_ROOT = pathlib.Path(
    os.environ.get(
        "MAJD_MAINTENANCE_ROOT",
        pathlib.Path(__file__).resolve().parent,
    )
).resolve()

DATA_DIR = PROJECT_ROOT / "data"
STATE_DIR = PROJECT_ROOT / "state"
LOG_DIR = PROJECT_ROOT / "logs"
REQUEST_DIR = PROJECT_ROOT / "execution_requests"
PROCESSED_DIR = PROJECT_ROOT / "execution_processed"
FAILED_DIR = PROJECT_ROOT / "execution_failed"
EVIDENCE_DIR = PROJECT_ROOT / "evidence"
INCIDENT_DIR = PROJECT_ROOT / "incidents"
INTELLIGENCE_DIR = PROJECT_ROOT / "intelligence"
REGULATORY_DIR = INTELLIGENCE_DIR / "regulatory"
TECHNOLOGY_DIR = INTELLIGENCE_DIR / "technology"
SECURITY_DIR = INTELLIGENCE_DIR / "security"
RUNTIME_LOCK_DIR = PROJECT_ROOT / "locks"

MASTER_DB_PATH = DATA_DIR / "majd_maintenance_mastermind.sqlite3"
EXECUTOR_DB_PATH = DATA_DIR / "majd_maintenance_executor.sqlite3"
RUNTIME_DB_PATH = DATA_DIR / "majd_maintenance_runtime.sqlite3"

LOG_PATH = LOG_DIR / "runtime-03.log"

for directory in (
    DATA_DIR,
    STATE_DIR,
    LOG_DIR,
    REQUEST_DIR,
    PROCESSED_DIR,
    FAILED_DIR,
    EVIDENCE_DIR,
    INCIDENT_DIR,
    INTELLIGENCE_DIR,
    REGULATORY_DIR,
    TECHNOLOGY_DIR,
    SECURITY_DIR,
    RUNTIME_LOCK_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)


# ======================================================================
# CONFIGURATION
# ======================================================================

LOOP_INTERVAL_SECONDS = max(
    30,
    int(os.environ.get("MAJD_RUNTIME_INTERVAL", "300")),
)

DISCOVERY_INTERVAL_SECONDS = max(
    60,
    int(os.environ.get("MAJD_DISCOVERY_INTERVAL", "900")),
)

REGULATORY_INTERVAL_SECONDS = max(
    3600,
    int(os.environ.get("MAJD_REGULATORY_INTERVAL", "21600")),
)

TECHNOLOGY_INTERVAL_SECONDS = max(
    3600,
    int(os.environ.get("MAJD_TECHNOLOGY_INTERVAL", "21600")),
)

SECURITY_INTERVAL_SECONDS = max(
    300,
    int(os.environ.get("MAJD_SECURITY_INTERVAL", "1800")),
)

BACKUP_VERIFY_INTERVAL_SECONDS = max(
    3600,
    int(os.environ.get("MAJD_BACKUP_VERIFY_INTERVAL", "86400")),
)

DEPENDENCY_INTERVAL_SECONDS = max(
    3600,
    int(os.environ.get("MAJD_DEPENDENCY_INTERVAL", "43200")),
)

CERTIFICATE_INTERVAL_SECONDS = max(
    1800,
    int(os.environ.get("MAJD_CERTIFICATE_INTERVAL", "21600")),
)

MAX_FAILURES_BEFORE_QUARANTINE = max(
    2,
    int(os.environ.get("MAJD_MAX_FAILURES_BEFORE_QUARANTINE", "5")),
)

MAX_REPAIR_REQUESTS_PER_PLATFORM_PER_HOUR = max(
    1,
    int(os.environ.get("MAJD_MAX_REPAIRS_PER_HOUR", "4")),
)

HTTP_TIMEOUT = max(
    3,
    int(os.environ.get("MAJD_RUNTIME_HTTP_TIMEOUT", "10")),
)

COMMAND_TIMEOUT = max(
    10,
    int(os.environ.get("MAJD_RUNTIME_COMMAND_TIMEOUT", "120")),
)

ALLOWED_ROOTS = tuple(
    pathlib.Path(value).resolve()
    for value in os.environ.get(
        "MAJD_ALLOWED_ROOTS",
        "/root:/srv:/opt",
    ).split(":")
    if value.strip()
)

MAJD_GIT_ROOT = pathlib.Path(
    os.environ.get("MAJD_GIT_ROOT", "/root/MAJD-GIT")
).resolve()

MAJD_IN_ROOT = pathlib.Path(
    os.environ.get("MAJD_IN_ROOT", "/root/MAJD-IN")
).resolve()


# ======================================================================
# LOGGING
# ======================================================================

logging.basicConfig(
    level=os.environ.get("MAJD_LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
    ],
)

LOG = logging.getLogger("MAJD-RUNTIME-03")


# ======================================================================
# ENUMS
# ======================================================================

class PlatformState(str, Enum):
    DISCOVERED = "DISCOVERED"
    BASELINED = "BASELINED"
    REPAIRING = "REPAIRING"
    INTEGRATING = "INTEGRATING"
    VERIFYING = "VERIFYING"
    READY_FOR_LAUNCH = "READY_FOR_LAUNCH"
    LAUNCHING = "LAUNCHING"
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    QUARANTINED = "QUARANTINED"
    CONTINUOUS_MAINTENANCE = "CONTINUOUS_MAINTENANCE"


class VerificationState(str, Enum):
    VERIFIED = "VERIFIED"
    NOT_VERIFIED = "NOT_VERIFIED"
    FAILED = "FAILED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    EXTERNAL_DEPENDENCY_REQUIRED = "EXTERNAL_DEPENDENCY_REQUIRED"


class IncidentSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IntelligenceKind(str, Enum):
    REGULATORY = "REGULATORY"
    SECURITY = "SECURITY"
    TECHNOLOGY = "TECHNOLOGY"
    DEPENDENCY = "DEPENDENCY"
    CERTIFICATE = "CERTIFICATE"
    PRIVACY = "PRIVACY"
    PAYMENT = "PAYMENT"
    AI = "AI"
    ACCESSIBILITY = "ACCESSIBILITY"
    COMMERCE = "COMMERCE"


# ======================================================================
# DATA MODELS
# ======================================================================

@dataclass
class CheckResult:
    check_id: str
    platform_id: str
    check_type: str
    target: str
    passed: bool
    status: str
    evidence: Dict[str, Any]
    checked_at: str


@dataclass
class PlatformSnapshot:
    platform_id: str
    name: str
    root_path: str
    exists: bool
    git: bool
    python: bool
    node: bool
    nginx_related: bool
    services: List[str]
    endpoints: List[str]
    databases: List[str]
    captured_at: str


@dataclass
class Incident:
    incident_id: str
    platform_id: Optional[str]
    severity: str
    category: str
    summary: str
    evidence: Dict[str, Any]
    opened_at: str
    status: str = "OPEN"


# ======================================================================
# UTILITIES
# ======================================================================

def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def epoch_now() -> int:
    return int(time.time())


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def json_dumps(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        default=str,
    )


def atomic_write_json(path: pathlib.Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temp.write_text(json_dumps(payload), encoding="utf-8")
    os.replace(temp, path)


def canonical_digest(payload: Any) -> str:
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return sha256_bytes(raw)


def path_within(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def validate_platform_path(path: pathlib.Path) -> pathlib.Path:
    resolved = path.resolve()

    if not any(path_within(resolved, root) for root in ALLOWED_ROOTS):
        raise PermissionError(f"Path outside approved roots: {resolved}")

    if resolved == pathlib.Path("/"):
        raise PermissionError("Filesystem root cannot be a platform.")

    return resolved


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def safe_json_load(path: pathlib.Path) -> Optional[Dict[str, Any]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except Exception:
        return None


# ======================================================================
# DATABASE
# ======================================================================

class RuntimeDatabase:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self.conn = sqlite3.connect(str(path), timeout=30)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")
        self._migrate()

    def _migrate(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS platforms (
                platform_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                root_path TEXT NOT NULL,
                state TEXT NOT NULL,
                failure_count INTEGER NOT NULL DEFAULT 0,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                last_verified TEXT,
                metadata_json TEXT NOT NULL DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS checks (
                check_id TEXT PRIMARY KEY,
                platform_id TEXT NOT NULL,
                check_type TEXT NOT NULL,
                target TEXT NOT NULL,
                passed INTEGER NOT NULL,
                status TEXT NOT NULL,
                evidence_json TEXT NOT NULL,
                checked_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS incidents (
                incident_id TEXT PRIMARY KEY,
                platform_id TEXT,
                severity TEXT NOT NULL,
                category TEXT NOT NULL,
                summary TEXT NOT NULL,
                evidence_json TEXT NOT NULL,
                opened_at TEXT NOT NULL,
                closed_at TEXT,
                status TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS verification_queue (
                verification_id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL UNIQUE,
                evidence_id TEXT,
                platform_id TEXT,
                state TEXT NOT NULL,
                attempts INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                result_json TEXT
            );

            CREATE TABLE IF NOT EXISTS intelligence_sources (
                source_id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                jurisdiction TEXT NOT NULL,
                authority TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                official INTEGER NOT NULL,
                enabled INTEGER NOT NULL,
                last_checked TEXT,
                last_digest TEXT,
                last_status TEXT,
                metadata_json TEXT NOT NULL DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS intelligence_events (
                event_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                jurisdiction TEXT NOT NULL,
                title TEXT NOT NULL,
                digest TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                discovered_at TEXT NOT NULL,
                processed INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS deadlines (
                deadline_id TEXT PRIMARY KEY,
                jurisdiction TEXT NOT NULL,
                authority TEXT NOT NULL,
                title TEXT NOT NULL,
                effective_at TEXT,
                applicability TEXT NOT NULL,
                source_url TEXT,
                status TEXT NOT NULL,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS scheduler (
                job_name TEXT PRIMARY KEY,
                interval_seconds INTEGER NOT NULL,
                last_run_epoch INTEGER,
                next_run_epoch INTEGER,
                last_status TEXT,
                last_error TEXT
            );

            CREATE TABLE IF NOT EXISTS repair_guard (
                guard_id TEXT PRIMARY KEY,
                platform_id TEXT NOT NULL,
                reason_digest TEXT NOT NULL,
                requested_at INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS runtime_events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                platform_id TEXT,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS heartbeats (
                heartbeat_id TEXT PRIMARY KEY,
                pid INTEGER NOT NULL,
                cycle INTEGER NOT NULL,
                status TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )

        self.conn.execute(
            """
            INSERT INTO meta(key, value)
            VALUES('schema_version', ?)
            ON CONFLICT(key)
            DO UPDATE SET value=excluded.value
            """,
            (str(SCHEMA_VERSION),),
        )

        self.conn.commit()

    def event(
        self,
        event_type: str,
        payload: Dict[str, Any],
        platform_id: Optional[str] = None,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO runtime_events(
                event_id,
                event_type,
                platform_id,
                payload_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(uuid.uuid4()),
                event_type,
                platform_id,
                json_dumps(payload),
                utc_now(),
            ),
        )
        self.conn.commit()

    def heartbeat(
        self,
        cycle: int,
        status: str,
        payload: Dict[str, Any],
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO heartbeats(
                heartbeat_id,
                pid,
                cycle,
                status,
                payload_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid.uuid4()),
                os.getpid(),
                cycle,
                status,
                json_dumps(payload),
                utc_now(),
            ),
        )
        self.conn.commit()


# ======================================================================
# COMMAND READER
# ======================================================================

class SafeCommandReader:
    """
    Runtime 03 primarily observes.

    Mutating actions are sent to Executor 02 through structured requests.
    """

    ALLOWED = {
        "git",
        "systemctl",
        "ss",
        "nginx",
        "python3",
        "node",
        "npm",
        "openssl",
    }

    def run(
        self,
        command: Sequence[str],
        cwd: Optional[pathlib.Path] = None,
        timeout: int = COMMAND_TIMEOUT,
    ) -> Dict[str, Any]:
        if not command:
            raise ValueError("Empty command.")

        executable = pathlib.Path(str(command[0])).name

        if executable not in self.ALLOWED:
            raise PermissionError(
                f"Runtime read command not allowed: {executable}"
            )

        if not command_exists(executable):
            return {
                "success": False,
                "returncode": 127,
                "stdout": "",
                "stderr": f"{executable} not installed",
            }

        try:
            result = subprocess.run(
                [str(x) for x in command],
                cwd=str(cwd) if cwd else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
                check=False,
            )

            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": (result.stdout or "")[:1024 * 1024],
                "stderr": (result.stderr or "")[:1024 * 1024],
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": 124,
                "stdout": "",
                "stderr": "TIMEOUT",
            }


# ======================================================================
# MASTER DB ADAPTER
# ======================================================================

class MasterAdapter:
    def __init__(self, path: pathlib.Path):
        self.path = path

    def available(self) -> bool:
        return self.path.exists()

    def platforms(self) -> List[Dict[str, Any]]:
        if not self.available():
            return []

        conn = sqlite3.connect(str(self.path), timeout=20)
        conn.row_factory = sqlite3.Row

        try:
            try:
                rows = conn.execute("SELECT * FROM platforms").fetchall()
            except sqlite3.Error:
                return []

            return [dict(row) for row in rows]
        finally:
            conn.close()

    def execution_requests(self) -> List[Dict[str, Any]]:
        if not self.available():
            return []

        conn = sqlite3.connect(str(self.path), timeout=20)
        conn.row_factory = sqlite3.Row

        try:
            try:
                rows = conn.execute(
                    """
                    SELECT *
                    FROM execution_requests
                    ORDER BY created_at ASC
                    """
                ).fetchall()
            except sqlite3.Error:
                return []

            return [dict(row) for row in rows]
        finally:
            conn.close()

    def update_execution_status(
        self,
        request_id: str,
        status: str,
    ) -> None:
        if not self.available():
            return

        conn = sqlite3.connect(str(self.path), timeout=20)

        try:
            conn.execute(
                """
                UPDATE execution_requests
                SET status=?
                WHERE request_id=?
                """,
                (status, request_id),
            )
            conn.commit()
        except sqlite3.Error:
            pass
        finally:
            conn.close()


# ======================================================================
# EXECUTOR DB ADAPTER
# ======================================================================

class ExecutorAdapter:
    def __init__(self, path: pathlib.Path):
        self.path = path

    def available(self) -> bool:
        return self.path.exists()

    def pending_verification_executions(self) -> List[Dict[str, Any]]:
        if not self.available():
            return []

        conn = sqlite3.connect(str(self.path), timeout=20)
        conn.row_factory = sqlite3.Row

        try:
            try:
                rows = conn.execute(
                    """
                    SELECT *
                    FROM executions
                    WHERE status='EXECUTED_PENDING_INDEPENDENT_VERIFICATION'
                    ORDER BY started_at ASC
                    """
                ).fetchall()
            except sqlite3.Error:
                return []

            return [dict(row) for row in rows]
        finally:
            conn.close()

    def evidence_for_request(self, request_id: str) -> List[Dict[str, Any]]:
        if not self.available():
            return []

        conn = sqlite3.connect(str(self.path), timeout=20)
        conn.row_factory = sqlite3.Row

        try:
            try:
                rows = conn.execute(
                    """
                    SELECT *
                    FROM evidence
                    WHERE request_id=?
                    ORDER BY created_at ASC
                    """,
                    (request_id,),
                ).fetchall()
            except sqlite3.Error:
                return []

            return [dict(row) for row in rows]
        finally:
            conn.close()

    def set_execution_status(
        self,
        execution_id: str,
        status: str,
    ) -> None:
        if not self.available():
            return

        conn = sqlite3.connect(str(self.path), timeout=20)

        try:
            conn.execute(
                """
                UPDATE executions
                SET status=?
                WHERE execution_id=?
                """,
                (status, execution_id),
            )
            conn.commit()
        finally:
            conn.close()


# ======================================================================
# PLATFORM DISCOVERY
# ======================================================================

class PlatformDiscovery:
    IGNORE_NAMES = {
        ".git",
        ".cache",
        ".local",
        ".npm",
        ".config",
        "node_modules",
        "__pycache__",
        "venv",
        ".venv",
        "snap",
    }

    PLATFORM_MARKERS = {
        ".git",
        "package.json",
        "requirements.txt",
        "pyproject.toml",
        "Dockerfile",
        "docker-compose.yml",
        "compose.yaml",
    }

    def __init__(
        self,
        db: RuntimeDatabase,
        master: MasterAdapter,
    ):
        self.db = db
        self.master = master

    def discover(self) -> List[PlatformSnapshot]:
        candidates: Dict[str, Dict[str, Any]] = {}

        for row in self.master.platforms():
            root_path = row.get("root_path")
            if not root_path:
                continue

            path = pathlib.Path(root_path)

            candidates[str(path.resolve())] = {
                "platform_id": str(
                    row.get("platform_id")
                    or self._platform_id(path)
                ),
                "name": str(
                    row.get("name")
                    or path.name
                ),
                "path": path,
            }

        managed = MAJD_GIT_ROOT / "managed"

        if managed.exists():
            with contextlib.suppress(PermissionError):
                for child in managed.iterdir():
                    if child.is_dir():
                        resolved = str(child.resolve())
                        candidates.setdefault(
                            resolved,
                            {
                                "platform_id": self._platform_id(child),
                                "name": child.name,
                                "path": child,
                            },
                        )

        for base in (
            pathlib.Path("/root"),
            pathlib.Path("/srv"),
            pathlib.Path("/opt"),
        ):
            if not base.exists():
                continue

            with contextlib.suppress(PermissionError):
                for child in base.iterdir():
                    if not child.is_dir():
                        continue

                    if child.name in self.IGNORE_NAMES:
                        continue

                    upper_name = child.name.upper()

                    if "MAJD" not in upper_name:
                        continue

                    if not self._looks_like_platform(child):
                        continue

                    resolved = str(child.resolve())

                    candidates.setdefault(
                        resolved,
                        {
                            "platform_id": self._platform_id(child),
                            "name": child.name,
                            "path": child,
                        },
                    )

        snapshots = []

        for candidate in candidates.values():
            try:
                snapshot = self.inspect(
                    candidate["platform_id"],
                    candidate["name"],
                    candidate["path"],
                )

                snapshots.append(snapshot)
                self._upsert(snapshot)

            except Exception as exc:
                LOG.warning(
                    "PLATFORM_DISCOVERY_FAILED | %s | %s",
                    candidate["path"],
                    exc,
                )

        return snapshots

    def _looks_like_platform(self, path: pathlib.Path) -> bool:
        return any(
            (path / marker).exists()
            for marker in self.PLATFORM_MARKERS
        ) or path.name.upper().startswith("MAJD")

    def _platform_id(self, path: pathlib.Path) -> str:
        return (
            "platform_"
            + hashlib.sha256(
                str(path.resolve()).encode("utf-8")
            ).hexdigest()[:20]
        )

    def inspect(
        self,
        platform_id: str,
        name: str,
        path: pathlib.Path,
    ) -> PlatformSnapshot:
        path = validate_platform_path(path)

        exists = path.exists()

        services = self._discover_services(name)
        endpoints = self._discover_endpoints(path)
        databases = self._discover_databases(path)

        nginx_related = self._nginx_mentions(name, path)

        return PlatformSnapshot(
            platform_id=platform_id,
            name=name,
            root_path=str(path),
            exists=exists,
            git=(path / ".git").exists(),
            python=any(
                (path / item).exists()
                for item in (
                    "requirements.txt",
                    "pyproject.toml",
                    "setup.py",
                )
            ),
            node=(path / "package.json").exists(),
            nginx_related=nginx_related,
            services=services,
            endpoints=endpoints,
            databases=databases,
            captured_at=utc_now(),
        )

    def _discover_services(self, name: str) -> List[str]:
        if not command_exists("systemctl"):
            return []

        try:
            result = subprocess.run(
                [
                    "systemctl",
                    "list-unit-files",
                    "--type=service",
                    "--no-legend",
                    "--no-pager",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30,
                check=False,
            )
        except Exception:
            return []

        tokens = {
            name.lower(),
            name.lower().replace("_", "-"),
            name.lower().replace("-", "_"),
        }

        services = []

        for line in result.stdout.splitlines():
            parts = line.split()
            if not parts:
                continue

            service = parts[0]

            lowered = service.lower()

            if any(
                token and token in lowered
                for token in tokens
            ):
                services.append(service)

        return sorted(set(services))

    def _discover_endpoints(self, root: pathlib.Path) -> List[str]:
        endpoints = set()

        candidate_files = [
            root / ".env",
            root / ".env.production",
            root / "README.md",
            root / "README",
        ]

        url_pattern = re.compile(
            r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+"
        )

        for path in candidate_files:
            if not path.exists() or not path.is_file():
                continue

            try:
                text = path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )
            except Exception:
                continue

            for match in url_pattern.findall(text):
                cleaned = match.rstrip(".,);]'\"")
                if len(cleaned) <= 2048:
                    endpoints.add(cleaned)

        return sorted(endpoints)

    def _discover_databases(self, root: pathlib.Path) -> List[str]:
        found = []

        for pattern in ("*.sqlite3", "*.sqlite", "*.db"):
            with contextlib.suppress(PermissionError):
                for path in root.rglob(pattern):
                    if any(
                        part in {
                            ".git",
                            "node_modules",
                            ".venv",
                            "venv",
                        }
                        for part in path.parts
                    ):
                        continue

                    found.append(str(path))

                    if len(found) >= 100:
                        return sorted(set(found))

        return sorted(set(found))

    def _nginx_mentions(
        self,
        name: str,
        root: pathlib.Path,
    ) -> bool:
        if not pathlib.Path("/etc/nginx").exists():
            return False

        needle_values = {
            name.lower(),
            str(root).lower(),
        }

        for directory in (
            pathlib.Path("/etc/nginx/sites-enabled"),
            pathlib.Path("/etc/nginx/sites-available"),
        ):
            if not directory.exists():
                continue

            with contextlib.suppress(PermissionError):
                for config in directory.iterdir():
                    if not config.is_file():
                        continue

                    try:
                        text = config.read_text(
                            encoding="utf-8",
                            errors="replace",
                        ).lower()
                    except Exception:
                        continue

                    if any(
                        needle in text
                        for needle in needle_values
                        if needle
                    ):
                        return True

        return False

    def _upsert(self, snapshot: PlatformSnapshot) -> None:
        now = utc_now()

        existing = self.db.conn.execute(
            """
            SELECT platform_id
            FROM platforms
            WHERE platform_id=?
            """,
            (snapshot.platform_id,),
        ).fetchone()

        if existing:
            self.db.conn.execute(
                """
                UPDATE platforms
                SET name=?,
                    root_path=?,
                    last_seen=?,
                    metadata_json=?
                WHERE platform_id=?
                """,
                (
                    snapshot.name,
                    snapshot.root_path,
                    now,
                    json_dumps(dataclasses.asdict(snapshot)),
                    snapshot.platform_id,
                ),
            )
        else:
            self.db.conn.execute(
                """
                INSERT INTO platforms(
                    platform_id,
                    name,
                    root_path,
                    state,
                    failure_count,
                    first_seen,
                    last_seen,
                    metadata_json
                )
                VALUES (?, ?, ?, ?, 0, ?, ?, ?)
                """,
                (
                    snapshot.platform_id,
                    snapshot.name,
                    snapshot.root_path,
                    PlatformState.DISCOVERED.value,
                    now,
                    now,
                    json_dumps(dataclasses.asdict(snapshot)),
                ),
            )

        self.db.conn.commit()


# ======================================================================
# SERVICE / NETWORK VERIFIER
# ======================================================================

class InfrastructureVerifier:
    def service(self, service: str) -> Dict[str, Any]:
        if not re.fullmatch(r"[A-Za-z0-9_.@:-]+\.service", service):
            return {
                "passed": False,
                "error": "INVALID_SERVICE_NAME",
            }

        if not command_exists("systemctl"):
            return {
                "passed": False,
                "error": "SYSTEMCTL_UNAVAILABLE",
            }

        active = subprocess.run(
            ["systemctl", "is-active", service],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
            check=False,
        )

        enabled = subprocess.run(
            ["systemctl", "is-enabled", service],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
            check=False,
        )

        return {
            "service": service,
            "active": active.stdout.strip(),
            "enabled": enabled.stdout.strip(),
            "passed": active.stdout.strip() == "active",
            "end_to_end_verified": False,
        }

    def http(self, url: str) -> Dict[str, Any]:
        parsed = urllib.parse.urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            return {
                "passed": False,
                "error": "INVALID_URL_SCHEME",
            }

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": f"MAJD-Watchtower/{VERSION}",
                "Accept": "application/json,text/html,*/*;q=0.1",
            },
        )

        started = time.monotonic()

        try:
            with urllib.request.urlopen(
                request,
                timeout=HTTP_TIMEOUT,
            ) as response:
                sample = response.read(256 * 1024)

                status = int(response.status)

                return {
                    "url": url,
                    "reachable": True,
                    "status": status,
                    "passed": 200 <= status < 400,
                    "sample_sha256": sha256_bytes(sample),
                    "sample_bytes": len(sample),
                    "duration_seconds": time.monotonic() - started,
                    "business_workflow_verified": False,
                }

        except urllib.error.HTTPError as exc:
            return {
                "url": url,
                "reachable": True,
                "status": int(exc.code),
                "passed": False,
                "error": str(exc),
                "business_workflow_verified": False,
            }

        except Exception as exc:
            return {
                "url": url,
                "reachable": False,
                "passed": False,
                "error": str(exc),
            }

    def tcp(self, host: str, port: int) -> Dict[str, Any]:
        try:
            started = time.monotonic()

            with socket.create_connection(
                (host, int(port)),
                timeout=5,
            ):
                return {
                    "host": host,
                    "port": int(port),
                    "reachable": True,
                    "passed": True,
                    "duration_seconds": time.monotonic() - started,
                }

        except Exception as exc:
            return {
                "host": host,
                "port": int(port),
                "reachable": False,
                "passed": False,
                "error": str(exc),
            }


# ======================================================================
# DATABASE VERIFIER
# ======================================================================

class DatabaseVerifier:
    def sqlite_integrity(self, path: pathlib.Path) -> Dict[str, Any]:
        if not path.exists():
            return {
                "path": str(path),
                "passed": False,
                "error": "DATABASE_NOT_FOUND",
            }

        try:
            conn = sqlite3.connect(str(path), timeout=20)

            try:
                result = conn.execute(
                    "PRAGMA integrity_check"
                ).fetchone()

                value = result[0] if result else "UNKNOWN"

                return {
                    "path": str(path),
                    "passed": value == "ok",
                    "result": value,
                }

            finally:
                conn.close()

        except Exception as exc:
            return {
                "path": str(path),
                "passed": False,
                "error": str(exc),
            }


# ======================================================================
# CODE VERIFIER
# ======================================================================

class CodeVerifier:
    def python_syntax(self, root: pathlib.Path) -> Dict[str, Any]:
        files = []

        for path in root.rglob("*.py"):
            if any(
                part in {
                    ".git",
                    "node_modules",
                    ".venv",
                    "venv",
                    "__pycache__",
                }
                for part in path.parts
            ):
                continue

            files.append(path)

        failures = []

        for path in files:
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "py_compile",
                        str(path),
                    ],
                    cwd=str(root),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=60,
                    check=False,
                )

                if result.returncode != 0:
                    failures.append(
                        {
                            "file": str(path),
                            "stderr": result.stderr[:65536],
                        }
                    )

            except Exception as exc:
                failures.append(
                    {
                        "file": str(path),
                        "stderr": str(exc),
                    }
                )

        return {
            "checked": len(files),
            "failures": failures,
            "passed": not failures,
        }

    def git_integrity(self, root: pathlib.Path) -> Dict[str, Any]:
        if not (root / ".git").exists():
            return {
                "passed": True,
                "status": "NOT_APPLICABLE",
            }

        try:
            result = subprocess.run(
                ["git", "diff", "--check"],
                cwd=str(root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60,
                check=False,
            )

            return {
                "passed": result.returncode == 0,
                "stdout": result.stdout[:65536],
                "stderr": result.stderr[:65536],
            }

        except Exception as exc:
            return {
                "passed": False,
                "error": str(exc),
            }


# ======================================================================
# EXECUTOR EVIDENCE VERIFIER
# ======================================================================

class IndependentEvidenceVerifier:
    def __init__(
        self,
        db: RuntimeDatabase,
        executor: ExecutorAdapter,
        master: MasterAdapter,
    ):
        self.db = db
        self.executor = executor
        self.master = master
        self.infrastructure = InfrastructureVerifier()
        self.database = DatabaseVerifier()
        self.code = CodeVerifier()

    def enqueue(self) -> int:
        count = 0

        for execution in self.executor.pending_verification_executions():
            request_id = str(execution["request_id"])

            existing = self.db.conn.execute(
                """
                SELECT verification_id
                FROM verification_queue
                WHERE request_id=?
                """,
                (request_id,),
            ).fetchone()

            if existing:
                continue

            evidence = self.executor.evidence_for_request(request_id)

            evidence_id = (
                str(evidence[-1]["evidence_id"])
                if evidence
                else None
            )

            now = utc_now()

            self.db.conn.execute(
                """
                INSERT INTO verification_queue(
                    verification_id,
                    request_id,
                    evidence_id,
                    platform_id,
                    state,
                    attempts,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, 0, ?, ?)
                """,
                (
                    str(uuid.uuid4()),
                    request_id,
                    evidence_id,
                    execution.get("platform_id"),
                    VerificationState.NOT_VERIFIED.value,
                    now,
                    now,
                ),
            )

            count += 1

        self.db.conn.commit()

        return count

    def process(self) -> List[Dict[str, Any]]:
        rows = self.db.conn.execute(
            """
            SELECT *
            FROM verification_queue
            WHERE state IN ('NOT_VERIFIED', 'FAILED')
              AND attempts < 5
            ORDER BY created_at ASC
            """
        ).fetchall()

        results = []

        for row in rows:
            result = self.verify(dict(row))
            results.append(result)

        return results

    def verify(self, queue_item: Dict[str, Any]) -> Dict[str, Any]:
        request_id = str(queue_item["request_id"])
        platform_id = queue_item.get("platform_id")

        evidence_rows = self.executor.evidence_for_request(request_id)

        result: Dict[str, Any] = {
            "request_id": request_id,
            "platform_id": platform_id,
            "evidence_present": bool(evidence_rows),
            "evidence_integrity": False,
            "observable_checks": [],
            "verified": False,
            "checked_at": utc_now(),
        }

        evidence_integrity = True

        for row in evidence_rows:
            try:
                payload = json.loads(row["payload_json"])
                digest = canonical_digest(payload)

                if digest != row["digest"]:
                    evidence_integrity = False
                    break

            except Exception:
                evidence_integrity = False
                break

        result["evidence_integrity"] = evidence_integrity

        if not evidence_rows or not evidence_integrity:
            self._save_result(
                queue_item,
                VerificationState.FAILED.value,
                result,
            )
            return result

        root = self._platform_root(platform_id)

        checks = []

        if root and root.exists():
            if any(
                (root / marker).exists()
                for marker in (
                    "requirements.txt",
                    "pyproject.toml",
                    "setup.py",
                )
            ):
                checks.append(
                    {
                        "type": "PYTHON_SYNTAX",
                        "result": self.code.python_syntax(root),
                    }
                )

            if (root / ".git").exists():
                checks.append(
                    {
                        "type": "GIT_DIFF_INTEGRITY",
                        "result": self.code.git_integrity(root),
                    }
                )

            for db_path in self._discover_databases(root):
                checks.append(
                    {
                        "type": "SQLITE_INTEGRITY",
                        "result": self.database.sqlite_integrity(db_path),
                    }
                )

            services = self._runtime_services(platform_id)

            for service in services:
                checks.append(
                    {
                        "type": "SERVICE",
                        "result": self.infrastructure.service(service),
                    }
                )

            endpoints = self._runtime_endpoints(platform_id)

            for endpoint in endpoints[:20]:
                checks.append(
                    {
                        "type": "HTTP",
                        "result": self.infrastructure.http(endpoint),
                    }
                )

        result["observable_checks"] = checks

        failed = [
            check
            for check in checks
            if not bool(check["result"].get("passed", False))
        ]

        result["verified"] = (
            evidence_integrity
            and bool(checks)
            and not failed
        )

        if result["verified"]:
            state = VerificationState.VERIFIED.value
        else:
            state = VerificationState.FAILED.value

        self._save_result(queue_item, state, result)

        execution_rows = self.executor.pending_verification_executions()

        for execution in execution_rows:
            if str(execution["request_id"]) != request_id:
                continue

            self.executor.set_execution_status(
                str(execution["execution_id"]),
                (
                    "VERIFIED"
                    if result["verified"]
                    else "VERIFICATION_FAILED"
                ),
            )

        self.master.update_execution_status(
            request_id,
            (
                "VERIFIED"
                if result["verified"]
                else "VERIFICATION_FAILED"
            ),
        )

        return result

    def _platform_root(
        self,
        platform_id: Optional[str],
    ) -> Optional[pathlib.Path]:
        if not platform_id:
            return None

        row = self.db.conn.execute(
            """
            SELECT root_path
            FROM platforms
            WHERE platform_id=?
            """,
            (platform_id,),
        ).fetchone()

        if not row:
            return None

        try:
            return validate_platform_path(pathlib.Path(row["root_path"]))
        except Exception:
            return None

    def _runtime_services(self, platform_id: Optional[str]) -> List[str]:
        if not platform_id:
            return []

        row = self.db.conn.execute(
            """
            SELECT metadata_json
            FROM platforms
            WHERE platform_id=?
            """,
            (platform_id,),
        ).fetchone()

        if not row:
            return []

        try:
            metadata = json.loads(row["metadata_json"])
            return list(metadata.get("services") or [])
        except Exception:
            return []

    def _runtime_endpoints(self, platform_id: Optional[str]) -> List[str]:
        if not platform_id:
            return []

        row = self.db.conn.execute(
            """
            SELECT metadata_json
            FROM platforms
            WHERE platform_id=?
            """,
            (platform_id,),
        ).fetchone()

        if not row:
            return []

        try:
            metadata = json.loads(row["metadata_json"])
            return list(metadata.get("endpoints") or [])
        except Exception:
            return []

    def _discover_databases(self, root: pathlib.Path) -> List[pathlib.Path]:
        output = []

        for pattern in ("*.sqlite3", "*.sqlite", "*.db"):
            for path in root.rglob(pattern):
                if any(
                    part in {
                        ".git",
                        "node_modules",
                        ".venv",
                        "venv",
                    }
                    for part in path.parts
                ):
                    continue

                output.append(path)

                if len(output) >= 30:
                    return output

        return output

    def _save_result(
        self,
        queue_item: Dict[str, Any],
        state: str,
        result: Dict[str, Any],
    ) -> None:
        self.db.conn.execute(
            """
            UPDATE verification_queue
            SET state=?,
                attempts=attempts+1,
                updated_at=?,
                result_json=?
            WHERE verification_id=?
            """,
            (
                state,
                utc_now(),
                json_dumps(result),
                queue_item["verification_id"],
            ),
        )

        self.db.conn.commit()


# ======================================================================
# INCIDENT MANAGER
# ======================================================================

class IncidentManager:
    def __init__(self, db: RuntimeDatabase):
        self.db = db

    def open(
        self,
        platform_id: Optional[str],
        severity: IncidentSeverity,
        category: str,
        summary: str,
        evidence: Dict[str, Any],
    ) -> Incident:
        fingerprint = canonical_digest(
            {
                "platform_id": platform_id,
                "category": category,
                "summary": summary,
            }
        )

        existing = self.db.conn.execute(
            """
            SELECT *
            FROM incidents
            WHERE status='OPEN'
              AND json_extract(evidence_json, '$.fingerprint')=?
            ORDER BY opened_at DESC
            LIMIT 1
            """,
            (fingerprint,),
        ).fetchone()

        if existing:
            return Incident(
                incident_id=existing["incident_id"],
                platform_id=existing["platform_id"],
                severity=existing["severity"],
                category=existing["category"],
                summary=existing["summary"],
                evidence=json.loads(existing["evidence_json"]),
                opened_at=existing["opened_at"],
                status=existing["status"],
            )

        incident = Incident(
            incident_id=str(uuid.uuid4()),
            platform_id=platform_id,
            severity=severity.value,
            category=category,
            summary=summary,
            evidence={
                "fingerprint": fingerprint,
                **evidence,
            },
            opened_at=utc_now(),
        )

        self.db.conn.execute(
            """
            INSERT INTO incidents(
                incident_id,
                platform_id,
                severity,
                category,
                summary,
                evidence_json,
                opened_at,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                incident.incident_id,
                incident.platform_id,
                incident.severity,
                incident.category,
                incident.summary,
                json_dumps(incident.evidence),
                incident.opened_at,
                incident.status,
            ),
        )

        self.db.conn.commit()

        atomic_write_json(
            INCIDENT_DIR / f"{incident.incident_id}.json",
            dataclasses.asdict(incident),
        )

        return incident


# ======================================================================
# REPAIR REQUEST ENGINE
# ======================================================================

class RepairRequestEngine:
    """
    Runtime detects.
    Executor 02 changes the system.

    This preserves separation between observer/verifier and mutator.
    """

    def __init__(self, db: RuntimeDatabase):
        self.db = db

    def allowed(
        self,
        platform_id: str,
        reason: Dict[str, Any],
    ) -> bool:
        digest = canonical_digest(reason)

        one_hour_ago = epoch_now() - 3600

        count = self.db.conn.execute(
            """
            SELECT COUNT(*) AS n
            FROM repair_guard
            WHERE platform_id=?
              AND requested_at>=?
            """,
            (platform_id, one_hour_ago),
        ).fetchone()["n"]

        if count >= MAX_REPAIR_REQUESTS_PER_PLATFORM_PER_HOUR:
            return False

        duplicate = self.db.conn.execute(
            """
            SELECT guard_id
            FROM repair_guard
            WHERE platform_id=?
              AND reason_digest=?
              AND requested_at>=?
            LIMIT 1
            """,
            (
                platform_id,
                digest,
                epoch_now() - 900,
            ),
        ).fetchone()

        return duplicate is None

    def create(
        self,
        platform_id: str,
        action: str,
        scope: Dict[str, Any],
        reason: Dict[str, Any],
        risk_level: str = "MEDIUM",
    ) -> Optional[pathlib.Path]:
        if not self.allowed(platform_id, reason):
            return None

        request_id = str(uuid.uuid4())

        payload = {
            "request_id": request_id,
            "platform_id": platform_id,
            "action": action,
            "scope": scope,
            "risk_level": risk_level,
            "backup_required": True,
            "independent_verification_required": True,
            "owner_authority": SUPREME_AUTHORITY,
            "generated_by": FILE_NAME,
            "generated_at": utc_now(),
            "reason": reason,
        }

        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        envelope = {
            "schema": "MAJD_EXECUTION_REQUEST_V1",
            "payload": payload,
            "integrity": {
                "algorithm": "SHA-256",
                "digest": sha256_bytes(canonical),
            },
        }

        path = REQUEST_DIR / f"{request_id}.json"

        atomic_write_json(path, envelope)

        self.db.conn.execute(
            """
            INSERT INTO repair_guard(
                guard_id,
                platform_id,
                reason_digest,
                requested_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                str(uuid.uuid4()),
                platform_id,
                canonical_digest(reason),
                epoch_now(),
            ),
        )

        self.db.conn.commit()

        return path


# ======================================================================
# PLATFORM HEALTH ENGINE
# ======================================================================

class PlatformHealthEngine:
    def __init__(
        self,
        db: RuntimeDatabase,
        incidents: IncidentManager,
        repair: RepairRequestEngine,
    ):
        self.db = db
        self.incidents = incidents
        self.repair = repair
        self.infrastructure = InfrastructureVerifier()
        self.database = DatabaseVerifier()
        self.code = CodeVerifier()

    def check_all(self) -> List[Dict[str, Any]]:
        rows = self.db.conn.execute(
            """
            SELECT *
            FROM platforms
            ORDER BY name
            """
        ).fetchall()

        results = []

        for row in rows:
            results.append(self.check_platform(dict(row)))

        return results

    def check_platform(self, row: Dict[str, Any]) -> Dict[str, Any]:
        platform_id = str(row["platform_id"])
        root = pathlib.Path(row["root_path"])

        result = {
            "platform_id": platform_id,
            "name": row["name"],
            "root": str(root),
            "checks": [],
            "healthy": True,
            "checked_at": utc_now(),
        }

        if not root.exists():
            result["healthy"] = False

            self._failure(
                platform_id,
                "FILESYSTEM",
                "Platform root is missing.",
                {"root": str(root)},
                result,
            )

            return result

        try:
            root = validate_platform_path(root)
        except Exception as exc:
            result["healthy"] = False

            self._failure(
                platform_id,
                "SCOPE",
                "Platform path failed scope validation.",
                {"error": str(exc)},
                result,
            )

            return result

        metadata = {}

        try:
            metadata = json.loads(row["metadata_json"])
        except Exception:
            pass

        if metadata.get("python"):
            py = self.code.python_syntax(root)

            result["checks"].append(
                {
                    "type": "PYTHON_SYNTAX",
                    "result": py,
                }
            )

            if not py["passed"]:
                result["healthy"] = False

                self._failure(
                    platform_id,
                    "CODE",
                    "Python syntax verification failed.",
                    py,
                    result,
                )

        if metadata.get("git"):
            git = self.code.git_integrity(root)

            result["checks"].append(
                {
                    "type": "GIT_INTEGRITY",
                    "result": git,
                }
            )

            if not git["passed"]:
                result["healthy"] = False

                self._failure(
                    platform_id,
                    "GIT",
                    "Git diff integrity verification failed.",
                    git,
                    result,
                )

        for service in metadata.get("services", []):
            service_result = self.infrastructure.service(service)

            result["checks"].append(
                {
                    "type": "SERVICE",
                    "result": service_result,
                }
            )

            if not service_result.get("passed"):
                result["healthy"] = False

                self._failure(
                    platform_id,
                    "SERVICE",
                    f"Service unhealthy: {service}",
                    service_result,
                    result,
                )

        for endpoint in metadata.get("endpoints", [])[:20]:
            http = self.infrastructure.http(endpoint)

            result["checks"].append(
                {
                    "type": "HTTP",
                    "result": http,
                }
            )

            if not http.get("passed"):
                result["healthy"] = False

                self._failure(
                    platform_id,
                    "HTTP",
                    f"Endpoint unhealthy: {endpoint}",
                    http,
                    result,
                )

        for database_path in metadata.get("databases", [])[:30]:
            db_result = self.database.sqlite_integrity(
                pathlib.Path(database_path)
            )

            result["checks"].append(
                {
                    "type": "DATABASE",
                    "result": db_result,
                }
            )

            if not db_result.get("passed"):
                result["healthy"] = False

                self._failure(
                    platform_id,
                    "DATABASE",
                    "Database integrity check failed.",
                    db_result,
                    result,
                )

        self._set_platform_health(platform_id, result["healthy"])

        return result

    def _failure(
        self,
        platform_id: str,
        category: str,
        summary: str,
        evidence: Dict[str, Any],
        aggregate: Dict[str, Any],
    ) -> None:
        self.incidents.open(
            platform_id=platform_id,
            severity=IncidentSeverity.HIGH,
            category=category,
            summary=summary,
            evidence=evidence,
        )

        row = self.db.conn.execute(
            """
            SELECT failure_count
            FROM platforms
            WHERE platform_id=?
            """,
            (platform_id,),
        ).fetchone()

        failures = int(row["failure_count"] if row else 0) + 1

        self.db.conn.execute(
            """
            UPDATE platforms
            SET failure_count=?,
                state=?
            WHERE platform_id=?
            """,
            (
                failures,
                (
                    PlatformState.QUARANTINED.value
                    if failures >= MAX_FAILURES_BEFORE_QUARANTINE
                    else PlatformState.DEGRADED.value
                ),
                platform_id,
            ),
        )

        self.db.conn.commit()

        if failures >= MAX_FAILURES_BEFORE_QUARANTINE:
            return

        reason = {
            "category": category,
            "summary": summary,
            "evidence_digest": canonical_digest(evidence),
        }

        self.repair.create(
            platform_id=platform_id,
            action="ASSESS_AND_REMEDIATE",
            scope={
                "category": category,
                "source": FILE_NAME,
            },
            reason=reason,
            risk_level="MEDIUM",
        )

    def _set_platform_health(
        self,
        platform_id: str,
        healthy: bool,
    ) -> None:
        if healthy:
            self.db.conn.execute(
                """
                UPDATE platforms
                SET state=?,
                    failure_count=0,
                    last_verified=?
                WHERE platform_id=?
                """,
                (
                    PlatformState.CONTINUOUS_MAINTENANCE.value,
                    utc_now(),
                    platform_id,
                ),
            )

            self.db.conn.commit()


# ======================================================================
# GLOBAL INTELLIGENCE SOURCE REGISTRY
# ======================================================================

class IntelligenceRegistry:
    """
    Stores official-source definitions.

    The registry is intentionally extensible. It is not a frozen list of
    world law. New official authorities/jurisdictions can be registered
    without changing the architecture.

    Only official-source URLs should be marked official=True.
    """

    DEFAULT_SOURCES = [
        {
            "kind": "REGULATORY",
            "jurisdiction": "SAUDI_ARABIA",
            "authority": "NCA",
            "title": "Saudi National Cybersecurity Authority",
            "url": "https://nca.gov.sa/",
        },
        {
            "kind": "PRIVACY",
            "jurisdiction": "SAUDI_ARABIA",
            "authority": "SDAIA",
            "title": "Saudi Data and AI Authority",
            "url": "https://sdaia.gov.sa/",
        },
        {
            "kind": "COMMERCE",
            "jurisdiction": "SAUDI_ARABIA",
            "authority": "MINISTRY_OF_COMMERCE",
            "title": "Saudi Ministry of Commerce",
            "url": "https://mc.gov.sa/",
        },
        {
            "kind": "PAYMENT",
            "jurisdiction": "SAUDI_ARABIA",
            "authority": "SAMA",
            "title": "Saudi Central Bank",
            "url": "https://www.sama.gov.sa/",
        },
        {
            "kind": "PRIVACY",
            "jurisdiction": "EUROPEAN_UNION",
            "authority": "EUR_LEX",
            "title": "EUR-Lex",
            "url": "https://eur-lex.europa.eu/",
        },
        {
            "kind": "AI",
            "jurisdiction": "EUROPEAN_UNION",
            "authority": "EUROPEAN_COMMISSION",
            "title": "European Commission Digital Strategy",
            "url": "https://digital-strategy.ec.europa.eu/",
        },
        {
            "kind": "SECURITY",
            "jurisdiction": "EUROPEAN_UNION",
            "authority": "ENISA",
            "title": "European Union Agency for Cybersecurity",
            "url": "https://www.enisa.europa.eu/",
        },
        {
            "kind": "REGULATORY",
            "jurisdiction": "UNITED_ARAB_EMIRATES",
            "authority": "UAE_LEGISLATION",
            "title": "UAE Legislation",
            "url": "https://uaelegislation.gov.ae/",
        },
        {
            "kind": "REGULATORY",
            "jurisdiction": "QATAR",
            "authority": "QATAR_GOVERNMENT",
            "title": "Qatar Government",
            "url": "https://www.gov.qa/",
        },
        {
            "kind": "SECURITY",
            "jurisdiction": "GLOBAL",
            "authority": "NIST",
            "title": "National Institute of Standards and Technology",
            "url": "https://www.nist.gov/",
        },
        {
            "kind": "SECURITY",
            "jurisdiction": "GLOBAL",
            "authority": "CISA",
            "title": "Cybersecurity and Infrastructure Security Agency",
            "url": "https://www.cisa.gov/",
        },
        {
            "kind": "SECURITY",
            "jurisdiction": "GLOBAL",
            "authority": "OWASP",
            "title": "OWASP Foundation",
            "url": "https://owasp.org/",
        },
        {
            "kind": "ACCESSIBILITY",
            "jurisdiction": "GLOBAL",
            "authority": "W3C",
            "title": "World Wide Web Consortium",
            "url": "https://www.w3.org/",
        },
    ]

    def __init__(self, db: RuntimeDatabase):
        self.db = db

    def bootstrap(self) -> int:
        inserted = 0

        for source in self.DEFAULT_SOURCES:
            source_id = (
                "source_"
                + hashlib.sha256(
                    (
                        source["jurisdiction"]
                        + "|"
                        + source["authority"]
                        + "|"
                        + source["url"]
                    ).encode("utf-8")
                ).hexdigest()[:24]
            )

            existing = self.db.conn.execute(
                """
                SELECT source_id
                FROM intelligence_sources
                WHERE source_id=?
                """,
                (source_id,),
            ).fetchone()

            if existing:
                continue

            self.db.conn.execute(
                """
                INSERT INTO intelligence_sources(
                    source_id,
                    kind,
                    jurisdiction,
                    authority,
                    title,
                    url,
                    official,
                    enabled,
                    metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, 1, 1, '{}')
                """,
                (
                    source_id,
                    source["kind"],
                    source["jurisdiction"],
                    source["authority"],
                    source["title"],
                    source["url"],
                ),
            )

            inserted += 1

        self.db.conn.commit()

        return inserted

    def add_source(
        self,
        kind: str,
        jurisdiction: str,
        authority: str,
        title: str,
        url: str,
        official: bool = True,
    ) -> str:
        parsed = urllib.parse.urlparse(url)

        if parsed.scheme != "https":
            raise ValueError("Official intelligence source must use HTTPS.")

        source_id = (
            "source_"
            + hashlib.sha256(
                (
                    jurisdiction
                    + "|"
                    + authority
                    + "|"
                    + url
                ).encode("utf-8")
            ).hexdigest()[:24]
        )

        self.db.conn.execute(
            """
            INSERT INTO intelligence_sources(
                source_id,
                kind,
                jurisdiction,
                authority,
                title,
                url,
                official,
                enabled,
                metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, '{}')
            ON CONFLICT(source_id)
            DO UPDATE SET
                kind=excluded.kind,
                jurisdiction=excluded.jurisdiction,
                authority=excluded.authority,
                title=excluded.title,
                url=excluded.url,
                official=excluded.official,
                enabled=1
            """,
            (
                source_id,
                kind,
                jurisdiction,
                authority,
                title,
                url,
                int(official),
            ),
        )

        self.db.conn.commit()

        return source_id


# ======================================================================
# OFFICIAL SOURCE CHANGE DETECTOR
# ======================================================================

class OfficialSourceMonitor:
    """
    Detects change in configured official sources.

    It does NOT automatically interpret a changed webpage as a new law.
    Changed material becomes an intelligence event for Mastermind 01
    applicability/policy analysis.
    """

    def __init__(
        self,
        db: RuntimeDatabase,
        incidents: IncidentManager,
    ):
        self.db = db
        self.incidents = incidents

    def run(self) -> List[Dict[str, Any]]:
        rows = self.db.conn.execute(
            """
            SELECT *
            FROM intelligence_sources
            WHERE enabled=1
            ORDER BY jurisdiction, authority
            """
        ).fetchall()

        results = []

        for row in rows:
            result = self.check_source(dict(row))
            results.append(result)

        return results

    def check_source(self, source: Dict[str, Any]) -> Dict[str, Any]:
        url = source["url"]

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": f"MAJD-Regulatory-Watchtower/{VERSION}",
                "Accept": "text/html,application/json,text/plain,*/*;q=0.1",
            },
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=20,
            ) as response:
                body = response.read(2 * 1024 * 1024)

                digest = sha256_bytes(body)

                previous = source.get("last_digest")

                changed = bool(previous and previous != digest)

                status = f"HTTP_{response.status}"

                self.db.conn.execute(
                    """
                    UPDATE intelligence_sources
                    SET last_checked=?,
                        last_digest=?,
                        last_status=?
                    WHERE source_id=?
                    """,
                    (
                        utc_now(),
                        digest,
                        status,
                        source["source_id"],
                    ),
                )

                if changed:
                    self._record_change(source, digest, status)

                self.db.conn.commit()

                return {
                    "source_id": source["source_id"],
                    "authority": source["authority"],
                    "jurisdiction": source["jurisdiction"],
                    "reachable": True,
                    "changed": changed,
                    "status": status,
                    "digest": digest,
                }

        except Exception as exc:
            self.db.conn.execute(
                """
                UPDATE intelligence_sources
                SET last_checked=?,
                    last_status=?
                WHERE source_id=?
                """,
                (
                    utc_now(),
                    f"ERROR:{type(exc).__name__}",
                    source["source_id"],
                ),
            )

            self.db.conn.commit()

            return {
                "source_id": source["source_id"],
                "authority": source["authority"],
                "jurisdiction": source["jurisdiction"],
                "reachable": False,
                "changed": False,
                "error": str(exc),
            }

    def _record_change(
        self,
        source: Dict[str, Any],
        digest: str,
        status: str,
    ) -> None:
        event_id = str(uuid.uuid4())

        payload = {
            "source_id": source["source_id"],
            "authority": source["authority"],
            "jurisdiction": source["jurisdiction"],
            "source_url": source["url"],
            "new_digest": digest,
            "status": status,
            "classification": "SOURCE_CHANGED_REQUIRES_ANALYSIS",
            "legal_conclusion": "NOT_DETERMINED",
            "applicability": "NOT_VERIFIED",
        }

        self.db.conn.execute(
            """
            INSERT INTO intelligence_events(
                event_id,
                source_id,
                kind,
                jurisdiction,
                title,
                digest,
                payload_json,
                discovered_at,
                processed
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
            """,
            (
                event_id,
                source["source_id"],
                source["kind"],
                source["jurisdiction"],
                f"Official source changed: {source['title']}",
                digest,
                json_dumps(payload),
                utc_now(),
            ),
        )


# ======================================================================
# INTELLIGENCE DISPATCHER
# ======================================================================

class IntelligenceDispatcher:
    """
    Creates structured analysis records for 01.

    It deliberately does not auto-apply legal text directly to production.
    """

    def __init__(self, db: RuntimeDatabase):
        self.db = db

    def pending(self) -> List[Dict[str, Any]]:
        rows = self.db.conn.execute(
            """
            SELECT *
            FROM intelligence_events
            WHERE processed=0
            ORDER BY discovered_at ASC
            """
        ).fetchall()

        return [dict(row) for row in rows]

    def export_for_mastermind(self) -> Optional[pathlib.Path]:
        events = self.pending()

        if not events:
            return None

        payload = {
            "schema": "MAJD_GLOBAL_INTELLIGENCE_BATCH_V1",
            "authority": SUPREME_AUTHORITY,
            "generated_by": FILE_NAME,
            "generated_at": utc_now(),
            "instructions": {
                "classify_applicability": True,
                "compare_current_platform_policy": True,
                "generate_policy_as_code_changes": True,
                "generate_technical_change_plan": True,
                "never_claim_legal_compliance_without_evidence": True,
                "legal_review_when_required": True,
            },
            "events": [],
        }

        for event in events:
            try:
                event_payload = json.loads(event["payload_json"])
            except Exception:
                event_payload = {}

            payload["events"].append(
                {
                    "event_id": event["event_id"],
                    "source_id": event["source_id"],
                    "kind": event["kind"],
                    "jurisdiction": event["jurisdiction"],
                    "title": event["title"],
                    "digest": event["digest"],
                    "discovered_at": event["discovered_at"],
                    "payload": event_payload,
                }
            )

        digest = canonical_digest(payload)

        envelope = {
            "payload": payload,
            "integrity": {
                "algorithm": "SHA-256",
                "digest": digest,
            },
        }

        path = (
            REGULATORY_DIR
            / f"intelligence-batch-{epoch_now()}.json"
        )

        atomic_write_json(path, envelope)

        return path


# ======================================================================
# SCHEDULER
# ======================================================================

class RuntimeScheduler:
    JOBS = {
        "discovery": DISCOVERY_INTERVAL_SECONDS,
        "regulatory": REGULATORY_INTERVAL_SECONDS,
        "technology": TECHNOLOGY_INTERVAL_SECONDS,
        "security": SECURITY_INTERVAL_SECONDS,
        "backup_verify": BACKUP_VERIFY_INTERVAL_SECONDS,
        "dependencies": DEPENDENCY_INTERVAL_SECONDS,
        "certificates": CERTIFICATE_INTERVAL_SECONDS,
    }

    def __init__(self, db: RuntimeDatabase):
        self.db = db
        self.bootstrap()

    def bootstrap(self) -> None:
        now = epoch_now()

        for name, interval in self.JOBS.items():
            self.db.conn.execute(
                """
                INSERT INTO scheduler(
                    job_name,
                    interval_seconds,
                    last_run_epoch,
                    next_run_epoch,
                    last_status
                )
                VALUES (?, ?, NULL, ?, 'PENDING')
                ON CONFLICT(job_name)
                DO UPDATE SET interval_seconds=excluded.interval_seconds
                """,
                (
                    name,
                    interval,
                    now,
                ),
            )

        self.db.conn.commit()

    def due(self, job_name: str) -> bool:
        row = self.db.conn.execute(
            """
            SELECT next_run_epoch
            FROM scheduler
            WHERE job_name=?
            """,
            (job_name,),
        ).fetchone()

        if not row:
            return True

        value = row["next_run_epoch"]

        return value is None or int(value) <= epoch_now()

    def complete(
        self,
        job_name: str,
        success: bool,
        error: Optional[str] = None,
    ) -> None:
        row = self.db.conn.execute(
            """
            SELECT interval_seconds
            FROM scheduler
            WHERE job_name=?
            """,
            (job_name,),
        ).fetchone()

        if not row:
            return

        now = epoch_now()
        interval = int(row["interval_seconds"])

        self.db.conn.execute(
            """
            UPDATE scheduler
            SET last_run_epoch=?,
                next_run_epoch=?,
                last_status=?,
                last_error=?
            WHERE job_name=?
            """,
            (
                now,
                now + interval,
                "SUCCESS" if success else "FAILED",
                error,
                job_name,
            ),
        )

        self.db.conn.commit()


# ======================================================================
# RUNTIME LOCK
# ======================================================================

class RuntimeLock:
    def __init__(self):
        self.path = RUNTIME_LOCK_DIR / "runtime-03.lock"
        self.fd: Optional[int] = None

    def __enter__(self):
        try:
            self.fd = os.open(
                str(self.path),
                os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                0o600,
            )
        except FileExistsError:
            try:
                pid_text = self.path.read_text(
                    encoding="utf-8"
                ).strip()

                pid = int(pid_text)

                os.kill(pid, 0)

                raise RuntimeError(
                    f"Runtime already active with PID {pid}"
                )

            except ProcessLookupError:
                self.path.unlink(missing_ok=True)

                self.fd = os.open(
                    str(self.path),
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    0o600,
                )

            except ValueError:
                self.path.unlink(missing_ok=True)

                self.fd = os.open(
                    str(self.path),
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    0o600,
                )

        os.write(self.fd, str(os.getpid()).encode("ascii"))

        return self

    def __exit__(self, exc_type, exc, tb):
        if self.fd is not None:
            os.close(self.fd)

        with contextlib.suppress(FileNotFoundError):
            self.path.unlink()


# ======================================================================
# RUNTIME
# ======================================================================

class MajdMaintenanceRuntime:
    def __init__(self):
        self.db = RuntimeDatabase(RUNTIME_DB_PATH)

        self.master = MasterAdapter(MASTER_DB_PATH)

        self.executor = ExecutorAdapter(EXECUTOR_DB_PATH)

        self.discovery = PlatformDiscovery(
            self.db,
            self.master,
        )

        self.incidents = IncidentManager(self.db)

        self.repair = RepairRequestEngine(self.db)

        self.health = PlatformHealthEngine(
            self.db,
            self.incidents,
            self.repair,
        )

        self.verifier = IndependentEvidenceVerifier(
            self.db,
            self.executor,
            self.master,
        )

        self.registry = IntelligenceRegistry(self.db)

        self.source_monitor = OfficialSourceMonitor(
            self.db,
            self.incidents,
        )

        self.intelligence = IntelligenceDispatcher(self.db)

        self.scheduler = RuntimeScheduler(self.db)

        self.stop_event = threading.Event()

        self.cycle_number = 0

    # ------------------------------------------------------------------
    # BOOTSTRAP
    # ------------------------------------------------------------------

    def bootstrap(self) -> Dict[str, Any]:
        sources_added = self.registry.bootstrap()

        snapshots = self.discovery.discover()

        payload = {
            "app": APP_NAME,
            "file": FILE_NAME,
            "version": VERSION,
            "authority": SUPREME_AUTHORITY,
            "runtime": True,
            "independent_verifier": True,
            "platforms_discovered": len(snapshots),
            "official_sources_registered": sources_added,
            "mastermind_database": self.master.available(),
            "executor_database": self.executor.available(),
            "majd_git_present": MAJD_GIT_ROOT.exists(),
            "majd_in_present": MAJD_IN_ROOT.exists(),
            "loop_interval_seconds": LOOP_INTERVAL_SECONDS,
            "capabilities": {
                "CONTINUOUS_DISCOVERY": True,
                "INDEPENDENT_VERIFICATION": True,
                "PLATFORM_HEALTH": True,
                "SERVICE_MONITORING": True,
                "HTTP_MONITORING": True,
                "DATABASE_INTEGRITY": True,
                "CODE_INTEGRITY": True,
                "INCIDENT_MANAGEMENT": True,
                "SELF_HEALING_REQUESTS": True,
                "ANTI_LOOP": True,
                "CRASH_RECOVERY": True,
                "REGULATORY_SOURCE_REGISTRY": True,
                "REGULATORY_CHANGE_DETECTION": True,
                "REGULATORY_APPLICABILITY_DECISION": False,
                "LEGAL_CONCLUSION_AUTOMATIC": False,
                "CONTINUOUS_TECHNOLOGY_SCHEDULING": True,
                "CONTINUOUS_SECURITY_SCHEDULING": True,
                "POST_LAUNCH_GUARDIAN": True,
                "CYBER_DEFENSE_FILE_04": False,
            },
            "truth": {
                "file_01_required_for_policy_and_applicability": True,
                "file_02_required_for_mutation": True,
                "file_03_operational": True,
                "file_04_required_for_dedicated_continuous_defense": True,
            },
            "timestamp": utc_now(),
        }

        atomic_write_json(
            STATE_DIR / "runtime-03-capabilities.json",
            payload,
        )

        self.db.event("BOOTSTRAP", payload)

        return payload

    # ------------------------------------------------------------------
    # ONE CYCLE
    # ------------------------------------------------------------------

    def cycle(self) -> Dict[str, Any]:
        self.cycle_number += 1

        started = utc_now()

        summary: Dict[str, Any] = {
            "cycle": self.cycle_number,
            "started_at": started,
            "discovery": None,
            "health": None,
            "verification": None,
            "intelligence": None,
            "jobs": {},
            "errors": [],
        }

        try:
            if self.scheduler.due("discovery"):
                try:
                    snapshots = self.discovery.discover()

                    summary["discovery"] = {
                        "platforms": len(snapshots)
                    }

                    self.scheduler.complete("discovery", True)

                except Exception as exc:
                    summary["errors"].append(
                        f"discovery:{exc}"
                    )
                    self.scheduler.complete(
                        "discovery",
                        False,
                        str(exc),
                    )

            try:
                enqueued = self.verifier.enqueue()
                verification_results = self.verifier.process()

                summary["verification"] = {
                    "enqueued": enqueued,
                    "processed": len(verification_results),
                    "verified": sum(
                        1
                        for item in verification_results
                        if item.get("verified")
                    ),
                    "failed": sum(
                        1
                        for item in verification_results
                        if not item.get("verified")
                    ),
                }

            except Exception as exc:
                summary["errors"].append(
                    f"verification:{exc}"
                )

            try:
                health_results = self.health.check_all()

                summary["health"] = {
                    "checked": len(health_results),
                    "healthy": sum(
                        1
                        for item in health_results
                        if item.get("healthy")
                    ),
                    "unhealthy": sum(
                        1
                        for item in health_results
                        if not item.get("healthy")
                    ),
                }

            except Exception as exc:
                summary["errors"].append(
                    f"health:{exc}"
                )

            if self.scheduler.due("regulatory"):
                try:
                    source_results = self.source_monitor.run()

                    export_path = self.intelligence.export_for_mastermind()

                    summary["intelligence"] = {
                        "sources_checked": len(source_results),
                        "reachable": sum(
                            1
                            for item in source_results
                            if item.get("reachable")
                        ),
                        "changed": sum(
                            1
                            for item in source_results
                            if item.get("changed")
                        ),
                        "mastermind_batch": (
                            str(export_path)
                            if export_path
                            else None
                        ),
                    }

                    self.scheduler.complete("regulatory", True)

                except Exception as exc:
                    summary["errors"].append(
                        f"regulatory:{exc}"
                    )

                    self.scheduler.complete(
                        "regulatory",
                        False,
                        str(exc),
                    )

            self._scheduled_placeholder(
                "technology",
                summary,
                "Technology/dependency intelligence is scheduled; "
                "actual source adapters must be registered and verified.",
            )

            self._scheduled_placeholder(
                "security",
                summary,
                "Security intelligence is scheduled; dedicated continuous "
                "defense is assigned to file 04.",
            )

            self._scheduled_placeholder(
                "backup_verify",
                summary,
                "Backup verification window reached.",
            )

            self._scheduled_placeholder(
                "dependencies",
                summary,
                "Dependency/EOL review window reached.",
            )

            self._scheduled_placeholder(
                "certificates",
                summary,
                "Certificate lifecycle review window reached.",
            )

        except Exception as exc:
            summary["errors"].append(
                f"cycle:{type(exc).__name__}:{exc}"
            )

            LOG.exception("RUNTIME_CYCLE_FATAL")

        summary["completed_at"] = utc_now()
        summary["success"] = not summary["errors"]

        self.db.heartbeat(
            self.cycle_number,
            "SUCCESS" if summary["success"] else "DEGRADED",
            summary,
        )

        atomic_write_json(
            STATE_DIR / "runtime-03-last-cycle.json",
            summary,
        )

        return summary

    def _scheduled_placeholder(
        self,
        job_name: str,
        summary: Dict[str, Any],
        message: str,
    ) -> None:
        if not self.scheduler.due(job_name):
            return

        summary["jobs"][job_name] = {
            "status": "SCHEDULED_REQUIRES_SPECIALIZED_ADAPTER",
            "message": message,
        }

        self.scheduler.complete(job_name, True)

    # ------------------------------------------------------------------
    # LOOP
    # ------------------------------------------------------------------

    def loop(self) -> int:
        self.bootstrap()

        LOG.info(
            "MAJD_RUNTIME_STARTED | pid=%s | interval=%ss",
            os.getpid(),
            LOOP_INTERVAL_SECONDS,
        )

        def stop_handler(signum, frame):
            LOG.info(
                "STOP_SIGNAL_RECEIVED | signal=%s",
                signum,
            )
            self.stop_event.set()

        signal.signal(signal.SIGTERM, stop_handler)
        signal.signal(signal.SIGINT, stop_handler)

        with RuntimeLock():
            while not self.stop_event.is_set():
                started = time.monotonic()

                summary = self.cycle()

                LOG.info(
                    "RUNTIME_CYCLE | cycle=%s | success=%s | errors=%s",
                    summary["cycle"],
                    summary["success"],
                    len(summary["errors"]),
                )

                elapsed = time.monotonic() - started

                wait_seconds = max(
                    1.0,
                    LOOP_INTERVAL_SECONDS - elapsed,
                )

                self.stop_event.wait(wait_seconds)

        LOG.info("MAJD_RUNTIME_STOPPED")

        return 0

    # ------------------------------------------------------------------
    # STATUS
    # ------------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        platform_rows = self.db.conn.execute(
            """
            SELECT state, COUNT(*) AS n
            FROM platforms
            GROUP BY state
            """
        ).fetchall()

        platform_states = {
            row["state"]: row["n"]
            for row in platform_rows
        }

        open_incidents = self.db.conn.execute(
            """
            SELECT severity, COUNT(*) AS n
            FROM incidents
            WHERE status='OPEN'
            GROUP BY severity
            """
        ).fetchall()

        incident_states = {
            row["severity"]: row["n"]
            for row in open_incidents
        }

        verification_rows = self.db.conn.execute(
            """
            SELECT state, COUNT(*) AS n
            FROM verification_queue
            GROUP BY state
            """
        ).fetchall()

        verification_states = {
            row["state"]: row["n"]
            for row in verification_rows
        }

        source_count = self.db.conn.execute(
            """
            SELECT COUNT(*) AS n
            FROM intelligence_sources
            WHERE enabled=1
            """
        ).fetchone()["n"]

        pending_intelligence = self.db.conn.execute(
            """
            SELECT COUNT(*) AS n
            FROM intelligence_events
            WHERE processed=0
            """
        ).fetchone()["n"]

        heartbeat = self.db.conn.execute(
            """
            SELECT *
            FROM heartbeats
            ORDER BY created_at DESC
            LIMIT 1
            """
        ).fetchone()

        return {
            "app": APP_NAME,
            "file": FILE_NAME,
            "version": VERSION,
            "authority": SUPREME_AUTHORITY,
            "platform_states": platform_states,
            "open_incidents": incident_states,
            "verification_states": verification_states,
            "official_sources_enabled": source_count,
            "pending_intelligence_events": pending_intelligence,
            "mastermind_database": self.master.available(),
            "executor_database": self.executor.available(),
            "last_heartbeat": (
                dict(heartbeat)
                if heartbeat
                else None
            ),
            "timestamp": utc_now(),
        }

    # ------------------------------------------------------------------
    # REGISTER SOURCE
    # ------------------------------------------------------------------

    def add_source(
        self,
        kind: str,
        jurisdiction: str,
        authority: str,
        title: str,
        url: str,
    ) -> str:
        return self.registry.add_source(
            kind=kind,
            jurisdiction=jurisdiction,
            authority=authority,
            title=title,
            url=url,
            official=True,
        )


# ======================================================================
# CLI
# ======================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=FILE_NAME,
        description=(
            "MAJD Sovereign Continuous Runtime + Watchtower"
        ),
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    sub.add_parser(
        "bootstrap",
        help="Initialize runtime state and official source registry.",
    )

    sub.add_parser(
        "status",
        help="Show truthful runtime state.",
    )

    sub.add_parser(
        "cycle",
        help="Run one complete maintenance/watchtower cycle.",
    )

    sub.add_parser(
        "loop",
        help="Run permanent maintenance/watchtower loop.",
    )

    sub.add_parser(
        "discover",
        help="Run platform discovery now.",
    )

    sub.add_parser(
        "verify",
        help="Run independent executor verification now.",
    )

    sub.add_parser(
        "health",
        help="Run platform health verification now.",
    )

    sub.add_parser(
        "regulatory",
        help="Check configured official intelligence sources now.",
    )

    source = sub.add_parser(
        "add-source",
        help="Register another official global source.",
    )

    source.add_argument("--kind", required=True)
    source.add_argument("--jurisdiction", required=True)
    source.add_argument("--authority", required=True)
    source.add_argument("--title", required=True)
    source.add_argument("--url", required=True)

    return parser


# ======================================================================
# MAIN
# ======================================================================

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    runtime = MajdMaintenanceRuntime()

    try:
        if args.command == "bootstrap":
            print(json_dumps(runtime.bootstrap()))
            return 0

        if args.command == "status":
            print(json_dumps(runtime.status()))
            return 0

        if args.command == "cycle":
            runtime.bootstrap()
            result = runtime.cycle()
            print(json_dumps(result))
            return 0 if result["success"] else 1

        if args.command == "loop":
            return runtime.loop()

        if args.command == "discover":
            runtime.registry.bootstrap()
            result = runtime.discovery.discover()

            print(
                json_dumps(
                    [
                        dataclasses.asdict(item)
                        for item in result
                    ]
                )
            )

            return 0

        if args.command == "verify":
            runtime.verifier.enqueue()
            results = runtime.verifier.process()

            print(json_dumps(results))

            failed = any(
                not item.get("verified")
                for item in results
            )

            return 1 if failed else 0

        if args.command == "health":
            results = runtime.health.check_all()

            print(json_dumps(results))

            failed = any(
                not item.get("healthy")
                for item in results
            )

            return 1 if failed else 0

        if args.command == "regulatory":
            runtime.registry.bootstrap()

            results = runtime.source_monitor.run()

            batch = runtime.intelligence.export_for_mastermind()

            print(
                json_dumps(
                    {
                        "results": results,
                        "mastermind_batch": (
                            str(batch)
                            if batch
                            else None
                        ),
                    }
                )
            )

            return 0

        if args.command == "add-source":
            source_id = runtime.add_source(
                kind=args.kind,
                jurisdiction=args.jurisdiction,
                authority=args.authority,
                title=args.title,
                url=args.url,
            )

            print(
                json_dumps(
                    {
                        "status": "REGISTERED",
                        "source_id": source_id,
                    }
                )
            )

            return 0

        parser.error("Unknown command.")
        return 2

    except KeyboardInterrupt:
        LOG.warning("MAJD_RUNTIME_INTERRUPTED")
        return 130

    except Exception as exc:
        LOG.exception(
            "MAJD_RUNTIME_FATAL | %s",
            exc,
        )

        print(
            json_dumps(
                {
                    "status": "FAILED",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "timestamp": utc_now(),
                }
            )
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())

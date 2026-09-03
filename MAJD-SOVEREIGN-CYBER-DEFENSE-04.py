#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
======================================================================
MAJD COMPREHENSIVE MAINTENANCE CENTER
MAJD-SOVEREIGN-CYBER-DEFENSE-04.py
======================================================================

FILE 04 — SOVEREIGN CONTINUOUS CYBER DEFENSE
VERSION 1.0.0

ABSOLUTE AUTHORITY
------------------
SUPREME_OWNER

ROLE
----
Permanent defensive security plane for:

    01 — MAJD-MAINTENANCE-MASTERMIND-01.py
    02 — MAJD-MAINTENANCE-EXECUTOR-02.py
    03 — MAJD-MAINTENANCE-RUNTIME-03.py

PRIMARY OBJECTIVE
-----------------
Protect the MAJD Comprehensive Maintenance Center itself and all current
and future MAJD platforms continuously while preserving availability.

DEFENSIVE FLOW
--------------
DISCOVER
    -> INVENTORY
    -> BASELINE
    -> HARDEN
    -> OBSERVE
    -> DETECT
    -> CORRELATE
    -> SCORE
    -> CONTAIN SURGICALLY
    -> KEEP HEALTHY SERVICES ALIVE
    -> REQUEST REPAIR THROUGH FILE 02
    -> VERIFY THROUGH FILE 03
    -> LEARN
    -> HARDEN AGAIN

NON-NEGOTIABLE RULES
--------------------
1. SUPREME_OWNER remains the highest authority.
2. No fake security claims.
3. No claim of protection without observable evidence.
4. Full-platform shutdown is a LAST RESORT.
5. Prefer the smallest possible containment scope.
6. One compromised account must not stop an entire platform.
7. One compromised endpoint must not stop unrelated endpoints.
8. One compromised worker must not stop unrelated workers.
9. One compromised platform must not stop all MAJD platforms.
10. No arbitrary remote command execution.
11. Internet/web/email/document content is untrusted data.
12. Prompt injection cannot authorize system operations.
13. Secrets must never be printed into logs or evidence.
14. Credentials must never be invented.
15. Defense actions must be auditable.
16. Critical destructive actions require recovery capability.
17. File 04 does not self-certify as independently verified.
18. File 03 remains the independent runtime verifier.
19. File 02 remains the real mutation/execution engine.
20. File 01 remains the global decision/policy brain.
21. Security control plane must be isolated from public application data.
22. A compromised defense component must be containable.
23. Security telemetry itself is treated as potentially untrusted input.
24. Defensive automation has explicit blast-radius limits.
25. Unknown state is reported as UNKNOWN / NOT_VERIFIED, never SAFE.

CORE SECURITY DOMAINS
---------------------
- Maintenance-center self-protection
- Attack-surface inventory
- Filesystem integrity
- Git integrity
- Service integrity
- Process inventory
- Listening-port inventory
- Network exposure
- Identity/authorization posture
- Secret exposure detection
- Credential lifecycle indicators
- Session/token hygiene indicators
- Dependency/supply-chain posture hooks
- AI/agent security boundaries
- Prompt-injection boundaries
- Tool permission boundaries
- Cross-platform information firewall
- Runtime configuration drift
- Nginx exposure
- TLS/certificate posture
- Database protection posture
- Backup security posture
- MAJD-GIT protection
- MAJD-IN/n8n protection
- Incident generation
- Surgical containment
- Safe degraded mode
- Read-only recommendation
- Quarantine recommendation
- Anti-loop
- Blast-radius control
- Self-integrity
- Tamper-evident evidence
- Defensive learning

IMPORTANT
---------
This is a DEFENSIVE security component.

It does not contain offensive exploitation logic, malware, credential
theft, persistence against third-party systems, or destructive attack
capabilities.

All mutation is requested through structured execution requests consumed
by FILE 02.
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
import hashlib
import ipaddress
import json
import logging
import os
import pathlib
import re
import shutil
import signal
import socket
import sqlite3
import stat
import subprocess
import sys
import threading
import time
import urllib.parse
import uuid

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


# =====================================================================
# IDENTITY
# =====================================================================

APP_NAME = "MAJD COMPREHENSIVE MAINTENANCE CENTER"
FILE_NAME = "MAJD-SOVEREIGN-CYBER-DEFENSE-04.py"
VERSION = "1.0.0"
SCHEMA_VERSION = 1

SUPREME_AUTHORITY = "SUPREME_OWNER"


# =====================================================================
# PATHS
# =====================================================================

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
EVIDENCE_DIR = PROJECT_ROOT / "evidence"
SECURITY_DIR = PROJECT_ROOT / "security"
SECURITY_STATE_DIR = SECURITY_DIR / "state"
SECURITY_EVIDENCE_DIR = SECURITY_DIR / "evidence"
SECURITY_INCIDENT_DIR = SECURITY_DIR / "incidents"
SECURITY_BASELINE_DIR = SECURITY_DIR / "baselines"
SECURITY_QUARANTINE_DIR = SECURITY_DIR / "quarantine"
LOCK_DIR = PROJECT_ROOT / "locks"

MASTER_DB_PATH = DATA_DIR / "majd_maintenance_mastermind.sqlite3"
EXECUTOR_DB_PATH = DATA_DIR / "majd_maintenance_executor.sqlite3"
RUNTIME_DB_PATH = DATA_DIR / "majd_maintenance_runtime.sqlite3"
DEFENSE_DB_PATH = DATA_DIR / "majd_sovereign_cyber_defense.sqlite3"

LOG_PATH = LOG_DIR / "cyber-defense-04.log"

MAJD_GIT_ROOT = pathlib.Path(
    os.environ.get(
        "MAJD_GIT_ROOT",
        "/root/MAJD-GIT",
    )
).resolve()

MAJD_IN_ROOT = pathlib.Path(
    os.environ.get(
        "MAJD_IN_ROOT",
        "/root/MAJD-IN",
    )
).resolve()

for directory in (
    DATA_DIR,
    STATE_DIR,
    LOG_DIR,
    REQUEST_DIR,
    EVIDENCE_DIR,
    SECURITY_DIR,
    SECURITY_STATE_DIR,
    SECURITY_EVIDENCE_DIR,
    SECURITY_INCIDENT_DIR,
    SECURITY_BASELINE_DIR,
    SECURITY_QUARANTINE_DIR,
    LOCK_DIR,
):
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


# =====================================================================
# CONFIGURATION
# =====================================================================

DEFENSE_INTERVAL_SECONDS = max(
    30,
    int(
        os.environ.get(
            "MAJD_DEFENSE_INTERVAL",
            "120",
        )
    ),
)

FULL_SCAN_INTERVAL_SECONDS = max(
    300,
    int(
        os.environ.get(
            "MAJD_DEFENSE_FULL_SCAN_INTERVAL",
            "1800",
        )
    ),
)

MAX_REPAIR_REQUESTS_PER_HOUR = max(
    1,
    int(
        os.environ.get(
            "MAJD_DEFENSE_MAX_REPAIRS_PER_HOUR",
            "6",
        )
    ),
)

MAX_CONTAINMENT_REQUESTS_PER_HOUR = max(
    1,
    int(
        os.environ.get(
            "MAJD_DEFENSE_MAX_CONTAINMENTS_PER_HOUR",
            "4",
        )
    ),
)

MAX_SCAN_FILES = max(
    500,
    int(
        os.environ.get(
            "MAJD_DEFENSE_MAX_SCAN_FILES",
            "20000",
        )
    ),
)

MAX_FILE_HASH_BYTES = max(
    1024 * 1024,
    int(
        os.environ.get(
            "MAJD_DEFENSE_MAX_HASH_FILE_BYTES",
            str(64 * 1024 * 1024),
        )
    ),
)

MAX_FILE_SAMPLE_BYTES = max(
    4096,
    int(
        os.environ.get(
            "MAJD_DEFENSE_MAX_SAMPLE_BYTES",
            str(512 * 1024),
        )
    ),
)

ALLOWED_ROOTS = tuple(
    pathlib.Path(value).resolve()
    for value in os.environ.get(
        "MAJD_ALLOWED_ROOTS",
        "/root:/srv:/opt",
    ).split(":")
    if value.strip()
)

PUBLIC_LISTEN_ADDRESSES = {
    "0.0.0.0",
    "::",
    "*",
}

CRITICAL_SYSTEM_PORTS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
}

SENSITIVE_FILENAME_PATTERNS = (
    ".env",
    ".env.production",
    ".env.local",
    "credentials",
    "credential",
    "secrets",
    "secret",
    "private",
    "id_rsa",
    "id_ed25519",
    ".pem",
    ".key",
    "token",
)

SENSITIVE_VALUE_PATTERNS = (
    re.compile(
        r"(?i)(password|passwd|secret|token|api[_-]?key)"
        r"\s*[:=]\s*['\"]?([^\s'\";]+)"
    ),
    re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
)

UNSAFE_FILE_MODES = {
    0o777,
    0o666,
}

PROTECTED_CENTER_FILES = (
    "MAJD-MAINTENANCE-MASTERMIND-01.py",
    "MAJD-MAINTENANCE-EXECUTOR-02.py",
    "MAJD-MAINTENANCE-RUNTIME-03.py",
    "MAJD-SOVEREIGN-CYBER-DEFENSE-04.py",
)

PUBLIC_CONTROL_PLANE_PORTS = {
    11434,  # local AI commonly expected local-only
    5678,   # n8n commonly should not be naked public
}

SECURITY_REQUEST_SCHEMA = "MAJD_EXECUTION_REQUEST_V1"


# =====================================================================
# LOGGING
# =====================================================================

logging.basicConfig(
    level=os.environ.get(
        "MAJD_LOG_LEVEL",
        "INFO",
    ).upper(),
    format=(
        "%(asctime)s | %(levelname)s | %(message)s"
    ),
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            LOG_PATH,
            encoding="utf-8",
        ),
    ],
)

LOG = logging.getLogger(
    "MAJD-CYBER-DEFENSE-04"
)


# =====================================================================
# ENUMS
# =====================================================================

class Severity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SecurityState(str, Enum):
    HEALTHY = "HEALTHY"
    OBSERVING = "OBSERVING"
    DEGRADED = "DEGRADED"
    CONTAINED = "CONTAINED"
    QUARANTINED = "QUARANTINED"
    UNKNOWN = "UNKNOWN"
    NOT_VERIFIED = "NOT_VERIFIED"


class ContainmentMode(str, Enum):
    NONE = "NONE"
    TOKEN_REVOKE = "TOKEN_REVOKE"
    ACCOUNT_RESTRICT = "ACCOUNT_RESTRICT"
    ENDPOINT_RESTRICT = "ENDPOINT_RESTRICT"
    SERVICE_RESTRICT = "SERVICE_RESTRICT"
    READ_ONLY = "READ_ONLY"
    WORKER_QUARANTINE = "WORKER_QUARANTINE"
    NETWORK_RESTRICT = "NETWORK_RESTRICT"
    PLATFORM_QUARANTINE = "PLATFORM_QUARANTINE"
    FULL_SHUTDOWN_LAST_RESORT = "FULL_SHUTDOWN_LAST_RESORT"


class Visibility(str, Enum):
    DIRECT = "DIRECT"
    DERIVED = "DERIVED"
    PROVIDER_REPORTED = "PROVIDER_REPORTED"
    NOT_VISIBLE = "NOT_VISIBLE"


class FindingCategory(str, Enum):
    SELF_INTEGRITY = "SELF_INTEGRITY"
    FILE_INTEGRITY = "FILE_INTEGRITY"
    FILE_PERMISSION = "FILE_PERMISSION"
    SECRET_EXPOSURE = "SECRET_EXPOSURE"
    NETWORK_EXPOSURE = "NETWORK_EXPOSURE"
    SERVICE = "SERVICE"
    PROCESS = "PROCESS"
    GIT = "GIT"
    CONFIGURATION = "CONFIGURATION"
    TLS = "TLS"
    DATABASE = "DATABASE"
    IDENTITY = "IDENTITY"
    SUPPLY_CHAIN = "SUPPLY_CHAIN"
    AI_AGENT = "AI_AGENT"
    CONTROL_PLANE = "CONTROL_PLANE"
    CROSS_PLATFORM = "CROSS_PLATFORM"
    TELEMETRY = "TELEMETRY"
    BACKUP = "BACKUP"
    UNKNOWN = "UNKNOWN"


# =====================================================================
# DATA MODELS
# =====================================================================

@dataclass
class PlatformRecord:
    platform_id: str
    name: str
    root_path: str


@dataclass
class SecurityFinding:
    finding_id: str
    platform_id: Optional[str]
    category: str
    severity: str
    title: str
    description: str
    target: str
    evidence: Dict[str, Any]
    containment_recommendation: str
    auto_repair_allowed: bool
    discovered_at: str


@dataclass
class IncidentRecord:
    incident_id: str
    platform_id: Optional[str]
    severity: str
    title: str
    category: str
    summary: str
    finding_ids: List[str]
    state: str
    opened_at: str


@dataclass
class DefenseCycleResult:
    cycle_id: str
    started_at: str
    completed_at: str
    platforms_checked: int
    findings: int
    critical_findings: int
    high_findings: int
    incidents_opened: int
    repair_requests_created: int
    containment_requests_created: int
    success: bool
    errors: List[str] = field(
        default_factory=list
    )


# =====================================================================
# UTILITIES
# =====================================================================

def utc_now() -> str:
    return dt.datetime.now(
        dt.timezone.utc
    ).isoformat()


def epoch_now() -> int:
    return int(
        time.time()
    )


def json_dumps(
    value: Any,
) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        default=str,
    )


def atomic_write_json(
    path: pathlib.Path,
    payload: Any,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary = path.with_name(
        f".{path.name}.{uuid.uuid4().hex}.tmp"
    )

    temporary.write_text(
        json_dumps(payload),
        encoding="utf-8",
    )

    os.replace(
        temporary,
        path,
    )


def sha256_bytes(
    data: bytes,
) -> str:
    return hashlib.sha256(
        data
    ).hexdigest()


def sha256_file(
    path: pathlib.Path,
) -> str:
    digest = hashlib.sha256()

    with path.open(
        "rb"
    ) as handle:
        remaining = (
            MAX_FILE_HASH_BYTES
        )

        while remaining > 0:
            chunk = handle.read(
                min(
                    1024 * 1024,
                    remaining,
                )
            )

            if not chunk:
                break

            digest.update(
                chunk
            )

            remaining -= len(
                chunk
            )

    return digest.hexdigest()


def canonical_digest(
    value: Any,
) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode(
        "utf-8"
    )

    return sha256_bytes(
        raw
    )


def path_within(
    path: pathlib.Path,
    root: pathlib.Path,
) -> bool:
    try:
        path.resolve().relative_to(
            root.resolve()
        )
        return True
    except ValueError:
        return False


def validate_platform_path(
    path: pathlib.Path,
) -> pathlib.Path:
    resolved = path.resolve()

    if resolved == pathlib.Path("/"):
        raise PermissionError(
            "Root filesystem cannot be treated as platform root."
        )

    if not any(
        path_within(
            resolved,
            root,
        )
        for root in ALLOWED_ROOTS
    ):
        raise PermissionError(
            f"Path outside approved MAJD roots: {resolved}"
        )

    return resolved


def command_exists(
    name: str,
) -> bool:
    return shutil.which(
        name
    ) is not None


def safe_file_mode(
    path: pathlib.Path,
) -> Optional[int]:
    try:
        return stat.S_IMODE(
            path.stat().st_mode
        )
    except OSError:
        return None


def sanitize_for_evidence(
    value: Any,
) -> Any:
    """
    Avoid storing obvious secret values in evidence.
    """

    sensitive_keys = (
        "password",
        "passwd",
        "secret",
        "token",
        "authorization",
        "cookie",
        "private_key",
        "apikey",
        "api_key",
        "client_secret",
    )

    if isinstance(
        value,
        dict,
    ):
        output = {}

        for key, item in value.items():
            lowered = str(
                key
            ).lower()

            if any(
                marker in lowered
                for marker in sensitive_keys
            ):
                output[key] = (
                    "***REDACTED***"
                )
            else:
                output[key] = (
                    sanitize_for_evidence(
                        item
                    )
                )

        return output

    if isinstance(
        value,
        list,
    ):
        return [
            sanitize_for_evidence(
                item
            )
            for item in value
        ]

    return value


# =====================================================================
# DATABASE
# =====================================================================

class DefenseDatabase:
    def __init__(
        self,
        path: pathlib.Path,
    ):
        self.path = path

        self.conn = sqlite3.connect(
            str(path),
            timeout=30,
        )

        self.conn.row_factory = (
            sqlite3.Row
        )

        self.conn.execute(
            "PRAGMA journal_mode=WAL"
        )

        self.conn.execute(
            "PRAGMA foreign_keys=ON"
        )

        self._migrate()

    def _migrate(
        self,
    ) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS platform_security (
                platform_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                root_path TEXT NOT NULL,
                state TEXT NOT NULL,
                last_scan TEXT,
                last_clean_scan TEXT,
                risk_score INTEGER NOT NULL DEFAULT 0,
                metadata_json TEXT NOT NULL DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS findings (
                finding_id TEXT PRIMARY KEY,
                platform_id TEXT,
                category TEXT NOT NULL,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                target TEXT NOT NULL,
                evidence_json TEXT NOT NULL,
                containment_recommendation TEXT NOT NULL,
                auto_repair_allowed INTEGER NOT NULL,
                discovered_at TEXT NOT NULL,
                resolved_at TEXT,
                status TEXT NOT NULL DEFAULT 'OPEN',
                fingerprint TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_findings_platform
            ON findings(platform_id);

            CREATE INDEX IF NOT EXISTS idx_findings_status
            ON findings(status);

            CREATE INDEX IF NOT EXISTS idx_findings_fingerprint
            ON findings(fingerprint);

            CREATE TABLE IF NOT EXISTS incidents (
                incident_id TEXT PRIMARY KEY,
                platform_id TEXT,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                summary TEXT NOT NULL,
                finding_ids_json TEXT NOT NULL,
                state TEXT NOT NULL,
                opened_at TEXT NOT NULL,
                closed_at TEXT
            );

            CREATE TABLE IF NOT EXISTS baselines (
                baseline_id TEXT PRIMARY KEY,
                platform_id TEXT,
                target TEXT NOT NULL,
                baseline_type TEXT NOT NULL,
                digest TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(platform_id, target, baseline_type)
            );

            CREATE TABLE IF NOT EXISTS network_inventory (
                inventory_id TEXT PRIMARY KEY,
                local_address TEXT NOT NULL,
                port INTEGER NOT NULL,
                process_name TEXT,
                pid INTEGER,
                public_exposure INTEGER NOT NULL,
                observed_at TEXT NOT NULL,
                UNIQUE(local_address, port)
            );

            CREATE TABLE IF NOT EXISTS repair_guard (
                guard_id TEXT PRIMARY KEY,
                platform_id TEXT,
                action_class TEXT NOT NULL,
                reason_digest TEXT NOT NULL,
                requested_epoch INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS self_integrity (
                file_name TEXT PRIMARY KEY,
                path TEXT NOT NULL,
                digest TEXT NOT NULL,
                observed_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS evidence (
                evidence_id TEXT PRIMARY KEY,
                platform_id TEXT,
                evidence_type TEXT NOT NULL,
                target TEXT NOT NULL,
                digest TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS audit (
                audit_id TEXT PRIMARY KEY,
                action TEXT NOT NULL,
                target TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS heartbeats (
                heartbeat_id TEXT PRIMARY KEY,
                pid INTEGER NOT NULL,
                status TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )

        self.conn.execute(
            """
            INSERT INTO meta(
                key,
                value
            )
            VALUES(
                'schema_version',
                ?
            )
            ON CONFLICT(key)
            DO UPDATE SET
                value=excluded.value
            """,
            (
                str(
                    SCHEMA_VERSION
                ),
            ),
        )

        self.conn.commit()

    def audit(
        self,
        action: str,
        target: str,
        payload: Optional[
            Dict[str, Any]
        ] = None,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO audit(
                audit_id,
                action,
                target,
                payload_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(
                    uuid.uuid4()
                ),
                action,
                target,
                json_dumps(
                    sanitize_for_evidence(
                        payload or {}
                    )
                ),
                utc_now(),
            ),
        )

        self.conn.commit()

    def heartbeat(
        self,
        status: str,
        payload: Dict[str, Any],
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO heartbeats(
                heartbeat_id,
                pid,
                status,
                payload_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(
                    uuid.uuid4()
                ),
                os.getpid(),
                status,
                json_dumps(
                    sanitize_for_evidence(
                        payload
                    )
                ),
                utc_now(),
            ),
        )

        self.conn.commit()


# =====================================================================
# PLATFORM SOURCE
# =====================================================================

class PlatformSource:
    def __init__(
        self,
        master_db: pathlib.Path,
        runtime_db: pathlib.Path,
    ):
        self.master_db = (
            master_db
        )

        self.runtime_db = (
            runtime_db
        )

    def platforms(
        self,
    ) -> List[PlatformRecord]:
        records: Dict[
            str,
            PlatformRecord
        ] = {}

        self._read_master(
            records
        )

        self._read_runtime(
            records
        )

        self._read_majd_git(
            records
        )

        self._read_common_roots(
            records
        )

        return sorted(
            records.values(),
            key=lambda item: (
                item.name.lower()
            ),
        )

    def _read_master(
        self,
        records: Dict[
            str,
            PlatformRecord
        ],
    ) -> None:
        if not self.master_db.exists():
            return

        conn = sqlite3.connect(
            str(
                self.master_db
            ),
            timeout=20,
        )

        conn.row_factory = (
            sqlite3.Row
        )

        try:
            with contextlib.suppress(
                sqlite3.Error
            ):
                rows = conn.execute(
                    """
                    SELECT
                        platform_id,
                        name,
                        root_path
                    FROM platforms
                    """
                ).fetchall()

                for row in rows:
                    self._insert_record(
                        records,
                        PlatformRecord(
                            platform_id=str(
                                row[
                                    "platform_id"
                                ]
                            ),
                            name=str(
                                row[
                                    "name"
                                ]
                            ),
                            root_path=str(
                                row[
                                    "root_path"
                                ]
                            ),
                        ),
                    )
        finally:
            conn.close()

    def _read_runtime(
        self,
        records: Dict[
            str,
            PlatformRecord
        ],
    ) -> None:
        if not self.runtime_db.exists():
            return

        conn = sqlite3.connect(
            str(
                self.runtime_db
            ),
            timeout=20,
        )

        conn.row_factory = (
            sqlite3.Row
        )

        try:
            with contextlib.suppress(
                sqlite3.Error
            ):
                rows = conn.execute(
                    """
                    SELECT
                        platform_id,
                        name,
                        root_path
                    FROM platforms
                    """
                ).fetchall()

                for row in rows:
                    self._insert_record(
                        records,
                        PlatformRecord(
                            platform_id=str(
                                row[
                                    "platform_id"
                                ]
                            ),
                            name=str(
                                row[
                                    "name"
                                ]
                            ),
                            root_path=str(
                                row[
                                    "root_path"
                                ]
                            ),
                        ),
                    )
        finally:
            conn.close()

    def _read_majd_git(
        self,
        records: Dict[
            str,
            PlatformRecord
        ],
    ) -> None:
        managed = (
            MAJD_GIT_ROOT
            / "managed"
        )

        if not managed.exists():
            return

        with contextlib.suppress(
            PermissionError
        ):
            for child in managed.iterdir():
                if not child.is_dir():
                    continue

                record = self._from_path(
                    child
                )

                self._insert_record(
                    records,
                    record,
                )

    def _read_common_roots(
        self,
        records: Dict[
            str,
            PlatformRecord
        ],
    ) -> None:
        for root in (
            pathlib.Path(
                "/root"
            ),
            pathlib.Path(
                "/srv"
            ),
            pathlib.Path(
                "/opt"
            ),
        ):
            if not root.exists():
                continue

            with contextlib.suppress(
                PermissionError
            ):
                for child in root.iterdir():
                    if not child.is_dir():
                        continue

                    if "MAJD" not in (
                        child.name.upper()
                    ):
                        continue

                    self._insert_record(
                        records,
                        self._from_path(
                            child
                        ),
                    )

    def _from_path(
        self,
        path: pathlib.Path,
    ) -> PlatformRecord:
        resolved = path.resolve()

        platform_id = (
            "platform_"
            + hashlib.sha256(
                str(
                    resolved
                ).encode(
                    "utf-8"
                )
            ).hexdigest()[:20]
        )

        return PlatformRecord(
            platform_id=platform_id,
            name=path.name,
            root_path=str(
                resolved
            ),
        )

    def _insert_record(
        self,
        records: Dict[
            str,
            PlatformRecord
        ],
        record: PlatformRecord,
    ) -> None:
        try:
            resolved = (
                pathlib.Path(
                    record.root_path
                ).resolve()
            )
        except Exception:
            return

        key = str(
            resolved
        )

        if key not in records:
            records[key] = (
                record
            )


# =====================================================================
# SELF PROTECTION
# =====================================================================

class SelfIntegrityEngine:
    def __init__(
        self,
        db: DefenseDatabase,
    ):
        self.db = db

    def check(
        self,
    ) -> List[SecurityFinding]:
        findings: List[
            SecurityFinding
        ] = []

        for file_name in (
            PROTECTED_CENTER_FILES
        ):
            path = (
                PROJECT_ROOT
                / file_name
            )

            if not path.exists():
                findings.append(
                    self._finding(
                        Severity.CRITICAL,
                        "MAINTENANCE_CENTER_FILE_MISSING",
                        (
                            f"Protected maintenance-center "
                            f"file is missing: {file_name}"
                        ),
                        str(path),
                        {
                            "exists": False,
                        },
                    )
                )
                continue

            digest = sha256_file(
                path
            )

            row = self.db.conn.execute(
                """
                SELECT digest
                FROM self_integrity
                WHERE file_name=?
                """,
                (
                    file_name,
                ),
            ).fetchone()

            if row is None:
                self.db.conn.execute(
                    """
                    INSERT INTO self_integrity(
                        file_name,
                        path,
                        digest,
                        observed_at
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        file_name,
                        str(path),
                        digest,
                        utc_now(),
                    ),
                )

            elif row[
                "digest"
            ] != digest:
                findings.append(
                    self._finding(
                        Severity.HIGH,
                        "MAINTENANCE_CENTER_FILE_CHANGED",
                        (
                            "Protected control-plane file changed "
                            "since the recorded baseline."
                        ),
                        str(path),
                        {
                            "previous_digest": (
                                row[
                                    "digest"
                                ]
                            ),
                            "current_digest": digest,
                        },
                    )
                )

            mode = safe_file_mode(
                path
            )

            if (
                mode is not None
                and (
                    mode & 0o002
                )
            ):
                findings.append(
                    self._finding(
                        Severity.HIGH,
                        "CONTROL_PLANE_WORLD_WRITABLE",
                        (
                            "Protected maintenance-center file "
                            "is writable by all users."
                        ),
                        str(path),
                        {
                            "mode": oct(
                                mode
                            ),
                        },
                    )
                )

        self.db.conn.commit()

        return findings

    def accept_current_baseline(
        self,
    ) -> Dict[str, Any]:
        updated = []

        for file_name in (
            PROTECTED_CENTER_FILES
        ):
            path = (
                PROJECT_ROOT
                / file_name
            )

            if not path.exists():
                continue

            digest = sha256_file(
                path
            )

            self.db.conn.execute(
                """
                INSERT INTO self_integrity(
                    file_name,
                    path,
                    digest,
                    observed_at
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT(file_name)
                DO UPDATE SET
                    path=excluded.path,
                    digest=excluded.digest,
                    observed_at=excluded.observed_at
                """,
                (
                    file_name,
                    str(path),
                    digest,
                    utc_now(),
                ),
            )

            updated.append(
                {
                    "file": file_name,
                    "digest": digest,
                }
            )

        self.db.conn.commit()

        return {
            "status": "SELF_BASELINE_ACCEPTED",
            "files": updated,
            "authority": SUPREME_AUTHORITY,
            "timestamp": utc_now(),
        }

    def _finding(
        self,
        severity: Severity,
        title: str,
        description: str,
        target: str,
        evidence: Dict[str, Any],
    ) -> SecurityFinding:
        return SecurityFinding(
            finding_id=str(
                uuid.uuid4()
            ),
            platform_id=None,
            category=(
                FindingCategory
                .SELF_INTEGRITY
                .value
            ),
            severity=severity.value,
            title=title,
            description=description,
            target=target,
            evidence=evidence,
            containment_recommendation=(
                ContainmentMode
                .SERVICE_RESTRICT
                .value
            ),
            auto_repair_allowed=False,
            discovered_at=utc_now(),
        )


# =====================================================================
# FILE SYSTEM SECURITY
# =====================================================================

class FilesystemSecurityEngine:
    IGNORE_PARTS = {
        ".git",
        "node_modules",
        ".venv",
        "venv",
        "__pycache__",
        ".cache",
    }

    def scan(
        self,
        platform: PlatformRecord,
    ) -> List[SecurityFinding]:
        findings: List[
            SecurityFinding
        ] = []

        root = validate_platform_path(
            pathlib.Path(
                platform.root_path
            )
        )

        if not root.exists():
            return [
                self._finding(
                    platform,
                    FindingCategory.FILE_INTEGRITY,
                    Severity.CRITICAL,
                    "PLATFORM_ROOT_MISSING",
                    (
                        "Platform root is not present."
                    ),
                    str(root),
                    {
                        "exists": False,
                    },
                    ContainmentMode.NONE,
                    False,
                )
            ]

        scanned = 0

        for path in root.rglob(
            "*"
        ):
            if scanned >= (
                MAX_SCAN_FILES
            ):
                break

            if any(
                part in self.IGNORE_PARTS
                for part in path.parts
            ):
                continue

            if not path.is_file():
                continue

            scanned += 1

            mode = safe_file_mode(
                path
            )

            if (
                mode is not None
                and (
                    mode & 0o002
                )
            ):
                findings.append(
                    self._finding(
                        platform,
                        FindingCategory.FILE_PERMISSION,
                        Severity.HIGH,
                        "WORLD_WRITABLE_FILE",
                        (
                            "File is writable by all local users."
                        ),
                        str(path),
                        {
                            "mode": oct(
                                mode
                            ),
                        },
                        ContainmentMode.NONE,
                        True,
                    )
                )

            if self._looks_sensitive(
                path
            ):
                findings.extend(
                    self._check_sensitive_file(
                        platform,
                        path,
                        mode,
                    )
                )

        return findings

    def _looks_sensitive(
        self,
        path: pathlib.Path,
    ) -> bool:
        lowered = (
            path.name.lower()
        )

        return any(
            marker in lowered
            for marker in (
                SENSITIVE_FILENAME_PATTERNS
            )
        )

    def _check_sensitive_file(
        self,
        platform: PlatformRecord,
        path: pathlib.Path,
        mode: Optional[int],
    ) -> List[SecurityFinding]:
        findings: List[
            SecurityFinding
        ] = []

        if (
            mode is not None
            and (
                mode & 0o077
            )
        ):
            findings.append(
                self._finding(
                    platform,
                    FindingCategory.FILE_PERMISSION,
                    Severity.HIGH,
                    "SENSITIVE_FILE_TOO_PERMISSIVE",
                    (
                        "Potentially sensitive file is readable "
                        "or writable by group/others."
                    ),
                    str(path),
                    {
                        "mode": oct(
                            mode
                        ),
                    },
                    ContainmentMode.NONE,
                    True,
                )
            )

        try:
            size = (
                path.stat().st_size
            )

            if size > (
                MAX_FILE_SAMPLE_BYTES
            ):
                return findings

            data = path.read_bytes()

        except Exception:
            return findings

        text = data.decode(
            "utf-8",
            errors="ignore",
        )

        detected_types = []

        for pattern in (
            SENSITIVE_VALUE_PATTERNS
        ):
            if pattern.search(
                text
            ):
                detected_types.append(
                    pattern.pattern[:80]
                )

        if detected_types:
            findings.append(
                self._finding(
                    platform,
                    FindingCategory.SECRET_EXPOSURE,
                    Severity.HIGH,
                    "POSSIBLE_SECRET_MATERIAL",
                    (
                        "Potential secret material detected in a "
                        "file. Secret values were not copied into evidence."
                    ),
                    str(path),
                    {
                        "file_sha256": sha256_file(
                            path
                        ),
                        "size": len(
                            data
                        ),
                        "pattern_count": len(
                            detected_types
                        ),
                        "secret_value_recorded": False,
                    },
                    ContainmentMode.NONE,
                    False,
                )
            )

        return findings

    def _finding(
        self,
        platform: PlatformRecord,
        category: FindingCategory,
        severity: Severity,
        title: str,
        description: str,
        target: str,
        evidence: Dict[str, Any],
        containment: ContainmentMode,
        auto_repair: bool,
    ) -> SecurityFinding:
        return SecurityFinding(
            finding_id=str(
                uuid.uuid4()
            ),
            platform_id=(
                platform.platform_id
            ),
            category=category.value,
            severity=severity.value,
            title=title,
            description=description,
            target=target,
            evidence=evidence,
            containment_recommendation=(
                containment.value
            ),
            auto_repair_allowed=auto_repair,
            discovered_at=utc_now(),
        )


# =====================================================================
# GIT SECURITY
# =====================================================================

class GitSecurityEngine:
    def scan(
        self,
        platform: PlatformRecord,
    ) -> List[SecurityFinding]:
        root = pathlib.Path(
            platform.root_path
        )

        if not (
            root
            / ".git"
        ).exists():
            return []

        findings = []

        status = self._run_git(
            root,
            [
                "status",
                "--porcelain",
            ],
        )

        diff_check = self._run_git(
            root,
            [
                "diff",
                "--check",
            ],
        )

        if not diff_check[
            "success"
        ]:
            findings.append(
                self._finding(
                    platform,
                    Severity.MEDIUM,
                    "GIT_DIFF_INTEGRITY_FAILED",
                    (
                        "Git diff integrity check reported a problem."
                    ),
                    str(root),
                    {
                        "returncode": diff_check[
                            "returncode"
                        ],
                        "stderr": diff_check[
                            "stderr"
                        ][:8192],
                    },
                )
            )

        if status[
            "success"
        ] and status[
            "stdout"
        ].strip():
            findings.append(
                self._finding(
                    platform,
                    Severity.LOW,
                    "UNCOMMITTED_CHANGES_PRESENT",
                    (
                        "Repository contains uncommitted changes. "
                        "This is not automatically malicious, but it "
                        "requires traceability."
                    ),
                    str(root),
                    {
                        "changed_entries": len(
                            status[
                                "stdout"
                            ].splitlines()
                        ),
                    },
                )
            )

        return findings

    def _run_git(
        self,
        root: pathlib.Path,
        args: Sequence[str],
    ) -> Dict[str, Any]:
        if not command_exists(
            "git"
        ):
            return {
                "success": False,
                "returncode": 127,
                "stdout": "",
                "stderr": "git unavailable",
            }

        try:
            result = subprocess.run(
                [
                    "git",
                    *args,
                ],
                cwd=str(
                    root
                ),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60,
                check=False,
            )

            return {
                "success": (
                    result.returncode
                    == 0
                ),
                "returncode": (
                    result.returncode
                ),
                "stdout": (
                    result.stdout
                    or ""
                ),
                "stderr": (
                    result.stderr
                    or ""
                ),
            }

        except Exception as exc:
            return {
                "success": False,
                "returncode": 1,
                "stdout": "",
                "stderr": str(
                    exc
                ),
            }

    def _finding(
        self,
        platform: PlatformRecord,
        severity: Severity,
        title: str,
        description: str,
        target: str,
        evidence: Dict[str, Any],
    ) -> SecurityFinding:
        return SecurityFinding(
            finding_id=str(
                uuid.uuid4()
            ),
            platform_id=(
                platform.platform_id
            ),
            category=(
                FindingCategory
                .GIT
                .value
            ),
            severity=severity.value,
            title=title,
            description=description,
            target=target,
            evidence=evidence,
            containment_recommendation=(
                ContainmentMode.NONE.value
            ),
            auto_repair_allowed=False,
            discovered_at=utc_now(),
        )


# =====================================================================
# NETWORK EXPOSURE ENGINE
# =====================================================================

class NetworkExposureEngine:
    LISTEN_RE = re.compile(
        r"^(?P<proto>\S+)\s+"
        r"(?P<state>\S+)\s+"
        r"(?P<recv>\S+)\s+"
        r"(?P<send>\S+)\s+"
        r"(?P<local>\S+)\s+"
        r"(?P<peer>\S+)"
    )

    def __init__(
        self,
        db: DefenseDatabase,
    ):
        self.db = db

    def inventory(
        self,
    ) -> List[Dict[str, Any]]:
        if not command_exists(
            "ss"
        ):
            return []

        try:
            result = subprocess.run(
                [
                    "ss",
                    "-lntup",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30,
                check=False,
            )

        except Exception:
            return []

        entries = []

        for line in (
            result.stdout.splitlines()
        ):
            line = line.strip()

            if not line:
                continue

            if line.lower().startswith(
                "netid"
            ):
                continue

            parts = line.split()

            if len(parts) < 5:
                continue

            local = (
                parts[4]
                if len(parts) > 4
                else ""
            )

            address, port = (
                self._split_address(
                    local
                )
            )

            if port is None:
                continue

            public = self._is_public_bind(
                address
            )

            process_name, pid = (
                self._parse_process(
                    line
                )
            )

            entry = {
                "address": address,
                "port": port,
                "public": public,
                "process_name": process_name,
                "pid": pid,
            }

            entries.append(
                entry
            )

            inventory_id = (
                "net_"
                + hashlib.sha256(
                    (
                        f"{address}|{port}"
                    ).encode(
                        "utf-8"
                    )
                ).hexdigest()[:24]
            )

            self.db.conn.execute(
                """
                INSERT INTO network_inventory(
                    inventory_id,
                    local_address,
                    port,
                    process_name,
                    pid,
                    public_exposure,
                    observed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(local_address, port)
                DO UPDATE SET
                    process_name=excluded.process_name,
                    pid=excluded.pid,
                    public_exposure=excluded.public_exposure,
                    observed_at=excluded.observed_at
                """,
                (
                    inventory_id,
                    address,
                    port,
                    process_name,
                    pid,
                    int(
                        public
                    ),
                    utc_now(),
                ),
            )

        self.db.conn.commit()

        return entries

    def findings(
        self,
        inventory: Sequence[
            Dict[str, Any]
        ],
    ) -> List[
        SecurityFinding
    ]:
        output = []

        for item in inventory:
            if not item[
                "public"
            ]:
                continue

            port = int(
                item[
                    "port"
                ]
            )

            if port in (
                PUBLIC_CONTROL_PLANE_PORTS
            ):
                output.append(
                    SecurityFinding(
                        finding_id=str(
                            uuid.uuid4()
                        ),
                        platform_id=None,
                        category=(
                            FindingCategory
                            .CONTROL_PLANE
                            .value
                        ),
                        severity=(
                            Severity.CRITICAL.value
                        ),
                        title=(
                            "CONTROL_PLANE_PORT_PUBLICLY_EXPOSED"
                        ),
                        description=(
                            "A control-plane style service appears "
                            "bound to a public interface."
                        ),
                        target=(
                            f"{item['address']}:{port}"
                        ),
                        evidence={
                            "port": port,
                            "process_name": (
                                item[
                                    "process_name"
                                ]
                            ),
                            "pid": item[
                                "pid"
                            ],
                            "public_bind": True,
                        },
                        containment_recommendation=(
                            ContainmentMode
                            .NETWORK_RESTRICT
                            .value
                        ),
                        auto_repair_allowed=False,
                        discovered_at=utc_now(),
                    )
                )

        return output

    def _split_address(
        self,
        value: str,
    ) -> Tuple[
        str,
        Optional[int],
    ]:
        value = value.strip()

        if value.startswith(
            "["
        ):
            match = re.match(
                r"^\[(.+)\]:(\d+)$",
                value,
            )

            if match:
                return (
                    match.group(
                        1
                    ),
                    int(
                        match.group(
                            2
                        )
                    ),
                )

        if ":" not in value:
            return (
                value,
                None,
            )

        address, port_text = (
            value.rsplit(
                ":",
                1,
            )
        )

        try:
            return (
                address,
                int(
                    port_text
                ),
            )
        except ValueError:
            return (
                address,
                None,
            )

    def _is_public_bind(
        self,
        address: str,
    ) -> bool:
        if address in (
            PUBLIC_LISTEN_ADDRESSES
        ):
            return True

        stripped = (
            address.strip(
                "[]"
            )
        )

        try:
            ip = ipaddress.ip_address(
                stripped
            )

            if ip.is_loopback:
                return False

            return True

        except ValueError:
            return False

    def _parse_process(
        self,
        line: str,
    ) -> Tuple[
        Optional[str],
        Optional[int],
    ]:
        process_name = None
        pid = None

        match_name = re.search(
            r'users:\(\("([^"]+)"',
            line,
        )

        if match_name:
            process_name = (
                match_name.group(
                    1
                )
            )

        match_pid = re.search(
            r"pid=(\d+)",
            line,
        )

        if match_pid:
            pid = int(
                match_pid.group(
                    1
                )
            )

        return (
            process_name,
            pid,
        )


# =====================================================================
# NGINX SECURITY
# =====================================================================

class NginxSecurityEngine:
    def scan(
        self,
    ) -> List[
        SecurityFinding
    ]:
        if not command_exists(
            "nginx"
        ):
            return []

        findings = []

        try:
            result = subprocess.run(
                [
                    "nginx",
                    "-t",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30,
                check=False,
            )

        except Exception as exc:
            return [
                SecurityFinding(
                    finding_id=str(
                        uuid.uuid4()
                    ),
                    platform_id=None,
                    category=(
                        FindingCategory
                        .CONFIGURATION
                        .value
                    ),
                    severity=(
                        Severity.HIGH.value
                    ),
                    title=(
                        "NGINX_CHECK_FAILED"
                    ),
                    description=(
                        "Nginx configuration could not be checked."
                    ),
                    target=(
                        "/etc/nginx"
                    ),
                    evidence={
                        "error": str(
                            exc
                        ),
                    },
                    containment_recommendation=(
                        ContainmentMode.NONE.value
                    ),
                    auto_repair_allowed=False,
                    discovered_at=utc_now(),
                )
            ]

        if result.returncode != 0:
            findings.append(
                SecurityFinding(
                    finding_id=str(
                        uuid.uuid4()
                    ),
                    platform_id=None,
                    category=(
                        FindingCategory
                        .CONFIGURATION
                        .value
                    ),
                    severity=(
                        Severity.HIGH.value
                    ),
                    title=(
                        "NGINX_CONFIGURATION_INVALID"
                    ),
                    description=(
                        "Nginx configuration validation failed."
                    ),
                    target=(
                        "/etc/nginx"
                    ),
                    evidence={
                        "returncode": (
                            result.returncode
                        ),
                        "stderr": (
                            result.stderr
                            or ""
                        )[:16384],
                    },
                    containment_recommendation=(
                        ContainmentMode.NONE.value
                    ),
                    auto_repair_allowed=False,
                    discovered_at=utc_now(),
                )
            )

        return findings


# =====================================================================
# SERVICE SECURITY
# =====================================================================

class ServiceSecurityEngine:
    def scan_known_control_plane(
        self,
    ) -> List[
        SecurityFinding
    ]:
        findings = []

        for service_name in (
            "nginx.service",
        ):
            state = self._service_state(
                service_name
            )

            if state is None:
                continue

            if (
                state[
                    "active"
                ]
                not in {
                    "active",
                }
            ):
                findings.append(
                    SecurityFinding(
                        finding_id=str(
                            uuid.uuid4()
                        ),
                        platform_id=None,
                        category=(
                            FindingCategory
                            .SERVICE
                            .value
                        ),
                        severity=(
                            Severity.HIGH.value
                        ),
                        title=(
                            "CRITICAL_INFRASTRUCTURE_SERVICE_INACTIVE"
                        ),
                        description=(
                            "A shared infrastructure service is not active."
                        ),
                        target=service_name,
                        evidence=state,
                        containment_recommendation=(
                            ContainmentMode.NONE.value
                        ),
                        auto_repair_allowed=True,
                        discovered_at=utc_now(),
                    )
                )

        return findings

    def _service_state(
        self,
        service: str,
    ) -> Optional[
        Dict[str, Any]
    ]:
        if not command_exists(
            "systemctl"
        ):
            return None

        active = subprocess.run(
            [
                "systemctl",
                "is-active",
                service,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
            check=False,
        )

        enabled = subprocess.run(
            [
                "systemctl",
                "is-enabled",
                service,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
            check=False,
        )

        return {
            "service": service,
            "active": (
                active.stdout.strip()
            ),
            "enabled": (
                enabled.stdout.strip()
            ),
        }


# =====================================================================
# AI / AGENT SECURITY
# =====================================================================

class AIAgentSecurityEngine:
    """
    Defensive policy checks for local AI/automation boundaries.

    It does not inspect user prompts for content moderation.
    It checks operational security boundaries.
    """

    def scan(
        self,
    ) -> List[
        SecurityFinding
    ]:
        findings = []

        ollama_host = os.environ.get(
            "OLLAMA_HOST",
            ""
        ).strip()

        if ollama_host:
            parsed = self._normalize_host(
                ollama_host
            )

            if parsed and parsed not in {
                "127.0.0.1",
                "localhost",
                "::1",
            }:
                findings.append(
                    SecurityFinding(
                        finding_id=str(
                            uuid.uuid4()
                        ),
                        platform_id=None,
                        category=(
                            FindingCategory
                            .AI_AGENT
                            .value
                        ),
                        severity=(
                            Severity.HIGH.value
                        ),
                        title=(
                            "LOCAL_AI_CONTROL_SURFACE_NOT_LOOPBACK"
                        ),
                        description=(
                            "Local AI service configuration appears "
                            "to use a non-loopback bind or host."
                        ),
                        target="OLLAMA_HOST",
                        evidence={
                            "configured_host": parsed,
                        },
                        containment_recommendation=(
                            ContainmentMode
                            .NETWORK_RESTRICT
                            .value
                        ),
                        auto_repair_allowed=False,
                        discovered_at=utc_now(),
                    )
                )

        return findings

    def _normalize_host(
        self,
        value: str,
    ) -> Optional[str]:
        candidate = value

        if "://" not in candidate:
            candidate = (
                "http://"
                + candidate
            )

        try:
            parsed = urllib.parse.urlparse(
                candidate
            )

            return parsed.hostname

        except Exception:
            return None


# =====================================================================
# CROSS PLATFORM FIREWALL
# =====================================================================

class CrossPlatformBoundaryEngine:
    """
    Looks for obvious direct references from one MAJD platform root to
    another platform's absolute filesystem path.

    This is a heuristic and does not claim complete data-flow analysis.
    """

    TEXT_SUFFIXES = {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".ini",
        ".conf",
        ".service",
        ".md",
    }

    def scan(
        self,
        platforms: Sequence[
            PlatformRecord
        ],
    ) -> List[
        SecurityFinding
    ]:
        findings = []

        roots = {
            platform.platform_id: (
                pathlib.Path(
                    platform.root_path
                ).resolve()
            )
            for platform in platforms
        }

        for platform in platforms:
            root = roots[
                platform.platform_id
            ]

            if not root.exists():
                continue

            other_roots = {
                other_id: other_path
                for other_id, other_path
                in roots.items()
                if other_id
                != platform.platform_id
            }

            checked = 0

            for path in root.rglob(
                "*"
            ):
                if checked >= 2000:
                    break

                if not path.is_file():
                    continue

                if (
                    path.suffix.lower()
                    not in self.TEXT_SUFFIXES
                ):
                    continue

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

                checked += 1

                try:
                    if (
                        path.stat().st_size
                        > 512 * 1024
                    ):
                        continue

                    text = path.read_text(
                        encoding="utf-8",
                        errors="ignore",
                    )

                except Exception:
                    continue

                for (
                    other_id,
                    other_root,
                ) in other_roots.items():
                    if str(
                        other_root
                    ) not in text:
                        continue

                    findings.append(
                        SecurityFinding(
                            finding_id=str(
                                uuid.uuid4()
                            ),
                            platform_id=(
                                platform.platform_id
                            ),
                            category=(
                                FindingCategory
                                .CROSS_PLATFORM
                                .value
                            ),
                            severity=(
                                Severity.MEDIUM.value
                            ),
                            title=(
                                "DIRECT_CROSS_PLATFORM_FILESYSTEM_REFERENCE"
                            ),
                            description=(
                                "A platform contains an absolute "
                                "filesystem reference to another MAJD "
                                "platform. Review whether this is an "
                                "approved dependency."
                            ),
                            target=str(
                                path
                            ),
                            evidence={
                                "referenced_platform_id": (
                                    other_id
                                ),
                                "referenced_root": str(
                                    other_root
                                ),
                            },
                            containment_recommendation=(
                                ContainmentMode.NONE.value
                            ),
                            auto_repair_allowed=False,
                            discovered_at=utc_now(),
                        )
                    )

        return findings


# =====================================================================
# BASELINE ENGINE
# =====================================================================

class BaselineEngine:
    def __init__(
        self,
        db: DefenseDatabase,
    ):
        self.db = db

    def baseline_platform(
        self,
        platform: PlatformRecord,
    ) -> Dict[str, Any]:
        root = validate_platform_path(
            pathlib.Path(
                platform.root_path
            )
        )

        tracked = []

        for file_name in (
            "requirements.txt",
            "pyproject.toml",
            "package.json",
            "package-lock.json",
            "Dockerfile",
            "docker-compose.yml",
            "compose.yaml",
        ):
            path = (
                root
                / file_name
            )

            if not path.exists():
                continue

            digest = sha256_file(
                path
            )

            self._save_baseline(
                platform.platform_id,
                str(path),
                "CRITICAL_PROJECT_FILE",
                digest,
                {
                    "size": (
                        path.stat().st_size
                    ),
                },
            )

            tracked.append(
                {
                    "path": str(
                        path
                    ),
                    "sha256": digest,
                }
            )

        return {
            "platform_id": (
                platform.platform_id
            ),
            "tracked": tracked,
            "timestamp": utc_now(),
        }

    def drift(
        self,
        platform: PlatformRecord,
    ) -> List[
        SecurityFinding
    ]:
        findings = []

        rows = self.db.conn.execute(
            """
            SELECT *
            FROM baselines
            WHERE platform_id=?
            """,
            (
                platform.platform_id,
            ),
        ).fetchall()

        for row in rows:
            path = pathlib.Path(
                row[
                    "target"
                ]
            )

            if not path.exists():
                findings.append(
                    SecurityFinding(
                        finding_id=str(
                            uuid.uuid4()
                        ),
                        platform_id=(
                            platform.platform_id
                        ),
                        category=(
                            FindingCategory
                            .FILE_INTEGRITY
                            .value
                        ),
                        severity=(
                            Severity.MEDIUM.value
                        ),
                        title=(
                            "BASELINED_FILE_MISSING"
                        ),
                        description=(
                            "A baselined project file is no longer present."
                        ),
                        target=str(
                            path
                        ),
                        evidence={
                            "baseline_digest": (
                                row[
                                    "digest"
                                ]
                            ),
                        },
                        containment_recommendation=(
                            ContainmentMode.NONE.value
                        ),
                        auto_repair_allowed=False,
                        discovered_at=utc_now(),
                    )
                )

                continue

            digest = sha256_file(
                path
            )

            if digest != row[
                "digest"
            ]:
                findings.append(
                    SecurityFinding(
                        finding_id=str(
                            uuid.uuid4()
                        ),
                        platform_id=(
                            platform.platform_id
                        ),
                        category=(
                            FindingCategory
                            .FILE_INTEGRITY
                            .value
                        ),
                        severity=(
                            Severity.LOW.value
                        ),
                        title=(
                            "BASELINED_FILE_CHANGED"
                        ),
                        description=(
                            "A baselined project file changed. "
                            "Change must be correlated with Git/audit "
                            "history before being considered suspicious."
                        ),
                        target=str(
                            path
                        ),
                        evidence={
                            "baseline_digest": (
                                row[
                                    "digest"
                                ]
                            ),
                            "current_digest": digest,
                        },
                        containment_recommendation=(
                            ContainmentMode.NONE.value
                        ),
                        auto_repair_allowed=False,
                        discovered_at=utc_now(),
                    )
                )

        return findings

    def _save_baseline(
        self,
        platform_id: Optional[str],
        target: str,
        baseline_type: str,
        digest: str,
        metadata: Dict[str, Any],
    ) -> None:
        baseline_id = (
            "baseline_"
            + hashlib.sha256(
                (
                    f"{platform_id}|"
                    f"{target}|"
                    f"{baseline_type}"
                ).encode(
                    "utf-8"
                )
            ).hexdigest()[:24]
        )

        now = utc_now()

        self.db.conn.execute(
            """
            INSERT INTO baselines(
                baseline_id,
                platform_id,
                target,
                baseline_type,
                digest,
                metadata_json,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(
                platform_id,
                target,
                baseline_type
            )
            DO NOTHING
            """,
            (
                baseline_id,
                platform_id,
                target,
                baseline_type,
                digest,
                json_dumps(
                    metadata
                ),
                now,
                now,
            ),
        )

        self.db.conn.commit()


# =====================================================================
# RISK ENGINE
# =====================================================================

class SecurityRiskEngine:
    WEIGHTS = {
        Severity.INFO.value: 0,
        Severity.LOW.value: 2,
        Severity.MEDIUM.value: 6,
        Severity.HIGH.value: 15,
        Severity.CRITICAL.value: 30,
    }

    def score(
        self,
        findings: Sequence[
            SecurityFinding
        ],
    ) -> int:
        total = sum(
            self.WEIGHTS.get(
                finding.severity,
                0,
            )
            for finding in findings
        )

        return min(
            total,
            100,
        )

    def state(
        self,
        score: int,
    ) -> SecurityState:
        if score >= 70:
            return (
                SecurityState
                .DEGRADED
            )

        if score >= 30:
            return (
                SecurityState
                .OBSERVING
            )

        return (
            SecurityState
            .HEALTHY
        )


# =====================================================================
# EVIDENCE ENGINE
# =====================================================================

class SecurityEvidenceEngine:
    def __init__(
        self,
        db: DefenseDatabase,
    ):
        self.db = db

    def write(
        self,
        evidence_type: str,
        target: str,
        payload: Dict[str, Any],
        platform_id: Optional[
            str
        ] = None,
    ) -> str:
        sanitized = (
            sanitize_for_evidence(
                payload
            )
        )

        digest = canonical_digest(
            sanitized
        )

        evidence_id = str(
            uuid.uuid4()
        )

        envelope = {
            "schema": (
                "MAJD_SECURITY_EVIDENCE_V1"
            ),
            "evidence_id": (
                evidence_id
            ),
            "platform_id": (
                platform_id
            ),
            "evidence_type": (
                evidence_type
            ),
            "target": target,
            "payload": sanitized,
            "digest": digest,
            "created_at": utc_now(),
        }

        atomic_write_json(
            SECURITY_EVIDENCE_DIR
            / f"{evidence_id}.json",
            envelope,
        )

        self.db.conn.execute(
            """
            INSERT INTO evidence(
                evidence_id,
                platform_id,
                evidence_type,
                target,
                digest,
                payload_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                evidence_id,
                platform_id,
                evidence_type,
                target,
                digest,
                json_dumps(
                    sanitized
                ),
                envelope[
                    "created_at"
                ],
            ),
        )

        self.db.conn.commit()

        return evidence_id


# =====================================================================
# FINDING STORE
# =====================================================================

class FindingStore:
    def __init__(
        self,
        db: DefenseDatabase,
    ):
        self.db = db

    def save(
        self,
        finding: SecurityFinding,
    ) -> str:
        fingerprint = (
            self._fingerprint(
                finding
            )
        )

        existing = self.db.conn.execute(
            """
            SELECT finding_id
            FROM findings
            WHERE fingerprint=?
              AND status='OPEN'
            ORDER BY discovered_at DESC
            LIMIT 1
            """,
            (
                fingerprint,
            ),
        ).fetchone()

        if existing:
            return str(
                existing[
                    "finding_id"
                ]
            )

        self.db.conn.execute(
            """
            INSERT INTO findings(
                finding_id,
                platform_id,
                category,
                severity,
                title,
                description,
                target,
                evidence_json,
                containment_recommendation,
                auto_repair_allowed,
                discovered_at,
                status,
                fingerprint
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'OPEN', ?)
            """,
            (
                finding.finding_id,
                finding.platform_id,
                finding.category,
                finding.severity,
                finding.title,
                finding.description,
                finding.target,
                json_dumps(
                    sanitize_for_evidence(
                        finding.evidence
                    )
                ),
                finding.containment_recommendation,
                int(
                    finding.auto_repair_allowed
                ),
                finding.discovered_at,
                fingerprint,
            ),
        )

        self.db.conn.commit()

        return (
            finding.finding_id
        )

    def _fingerprint(
        self,
        finding: SecurityFinding,
    ) -> str:
        return canonical_digest(
            {
                "platform_id": (
                    finding.platform_id
                ),
                "category": (
                    finding.category
                ),
                "title": finding.title,
                "target": finding.target,
            }
        )


# =====================================================================
# INCIDENT ENGINE
# =====================================================================

class SecurityIncidentEngine:
    def __init__(
        self,
        db: DefenseDatabase,
    ):
        self.db = db

    def correlate(
        self,
        findings: Sequence[
            SecurityFinding
        ],
    ) -> List[
        IncidentRecord
    ]:
        groups: Dict[
            Tuple[
                Optional[str],
                str,
            ],
            List[
                SecurityFinding
            ],
        ] = {}

        for finding in findings:
            key = (
                finding.platform_id,
                finding.category,
            )

            groups.setdefault(
                key,
                [],
            ).append(
                finding
            )

        incidents = []

        for (
            platform_id,
            category,
        ), group in groups.items():
            if not group:
                continue

            highest = self._highest(
                group
            )

            if highest in {
                Severity.INFO.value,
                Severity.LOW.value,
            }:
                continue

            incident = self._open(
                platform_id,
                category,
                highest,
                group,
            )

            if incident:
                incidents.append(
                    incident
                )

        return incidents

    def _highest(
        self,
        findings: Sequence[
            SecurityFinding
        ],
    ) -> str:
        order = {
            Severity.INFO.value: 0,
            Severity.LOW.value: 1,
            Severity.MEDIUM.value: 2,
            Severity.HIGH.value: 3,
            Severity.CRITICAL.value: 4,
        }

        return max(
            (
                finding.severity
                for finding in findings
            ),
            key=lambda value: (
                order.get(
                    value,
                    0,
                )
            ),
        )

    def _open(
        self,
        platform_id: Optional[str],
        category: str,
        severity: str,
        findings: Sequence[
            SecurityFinding
        ],
    ) -> Optional[
        IncidentRecord
    ]:
        fingerprint = canonical_digest(
            {
                "platform_id": (
                    platform_id
                ),
                "category": category,
                "titles": sorted(
                    set(
                        finding.title
                        for finding
                        in findings
                    )
                ),
            }
        )

        existing = self.db.conn.execute(
            """
            SELECT incident_id
            FROM incidents
            WHERE state='OPEN'
              AND summary LIKE ?
            LIMIT 1
            """,
            (
                f"%{fingerprint}%",
            ),
        ).fetchone()

        if existing:
            return None

        finding_ids = [
            finding.finding_id
            for finding in findings
        ]

        incident = IncidentRecord(
            incident_id=str(
                uuid.uuid4()
            ),
            platform_id=(
                platform_id
            ),
            severity=severity,
            title=(
                f"MAJD security incident: "
                f"{category}"
            ),
            category=category,
            summary=(
                f"fingerprint={fingerprint}; "
                f"correlated_findings="
                f"{len(findings)}"
            ),
            finding_ids=(
                finding_ids
            ),
            state="OPEN",
            opened_at=utc_now(),
        )

        self.db.conn.execute(
            """
            INSERT INTO incidents(
                incident_id,
                platform_id,
                severity,
                title,
                category,
                summary,
                finding_ids_json,
                state,
                opened_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                incident.incident_id,
                incident.platform_id,
                incident.severity,
                incident.title,
                incident.category,
                incident.summary,
                json_dumps(
                    incident.finding_ids
                ),
                incident.state,
                incident.opened_at,
            ),
        )

        self.db.conn.commit()

        atomic_write_json(
            SECURITY_INCIDENT_DIR
            / (
                f"{incident.incident_id}"
                ".json"
            ),
            dataclasses.asdict(
                incident
            ),
        )

        return incident


# =====================================================================
# SURGICAL CONTAINMENT POLICY
# =====================================================================

class SurgicalContainmentPolicy:
    """
    Chooses the smallest defensive scope consistent with the finding.

    It does NOT directly mutate the host.
    It returns a recommendation that can be converted into an executor
    request.

    Full shutdown is deliberately excluded from normal automatic flow.
    """

    def decide(
        self,
        finding: SecurityFinding,
    ) -> ContainmentMode:
        if (
            finding.category
            == FindingCategory
            .SECRET_EXPOSURE
            .value
        ):
            return (
                ContainmentMode
                .TOKEN_REVOKE
            )

        if (
            finding.category
            == FindingCategory
            .CONTROL_PLANE
            .value
        ):
            return (
                ContainmentMode
                .NETWORK_RESTRICT
            )

        if (
            finding.category
            == FindingCategory
            .NETWORK_EXPOSURE
            .value
        ):
            return (
                ContainmentMode
                .NETWORK_RESTRICT
            )

        if (
            finding.category
            == FindingCategory
            .AI_AGENT
            .value
        ):
            return (
                ContainmentMode
                .SERVICE_RESTRICT
            )

        if (
            finding.category
            == FindingCategory
            .SERVICE
            .value
        ):
            return (
                ContainmentMode.NONE
            )

        if (
            finding.category
            == FindingCategory
            .CROSS_PLATFORM
            .value
        ):
            return (
                ContainmentMode.NONE
            )

        return (
            ContainmentMode.NONE
        )

    def allow_automatic(
        self,
        finding: SecurityFinding,
        mode: ContainmentMode,
    ) -> bool:
        if mode == (
            ContainmentMode
            .FULL_SHUTDOWN_LAST_RESORT
        ):
            return False

        if finding.severity == (
            Severity.CRITICAL.value
        ):
            return False

        return (
            finding.auto_repair_allowed
        )


# =====================================================================
# EXECUTOR REQUEST BRIDGE
# =====================================================================

class DefenseExecutionBridge:
    def __init__(
        self,
        db: DefenseDatabase,
    ):
        self.db = db

    def request_repair(
        self,
        platform_id: Optional[str],
        reason: Dict[str, Any],
        risk_level: str,
    ) -> Optional[
        pathlib.Path
    ]:
        if not platform_id:
            return None

        if not self._allowed(
            platform_id,
            "REPAIR",
            reason,
            MAX_REPAIR_REQUESTS_PER_HOUR,
        ):
            return None

        return self._write_request(
            platform_id=platform_id,
            action=(
                "ASSESS_AND_REMEDIATE"
            ),
            scope={
                "security_reason": (
                    reason
                ),
                "source": FILE_NAME,
                "constraints": {
                    "no_fake_success": True,
                    "preserve_service": True,
                    "minimum_blast_radius": True,
                    "backup_before_destructive_change": True,
                    "rollback_required": True,
                },
            },
            reason=reason,
            risk_level=risk_level,
        )

    def request_file_permission_repair(
        self,
        platform_id: str,
        target: str,
        reason: Dict[str, Any],
    ) -> Optional[
        pathlib.Path
    ]:
        if not self._allowed(
            platform_id,
            "PERMISSION_REPAIR",
            reason,
            MAX_REPAIR_REQUESTS_PER_HOUR,
        ):
            return None

        return self._write_request(
            platform_id=platform_id,
            action=(
                "ASSESS_AND_REMEDIATE"
            ),
            scope={
                "category": (
                    "FILE_PERMISSION"
                ),
                "target": target,
                "desired_security_property": (
                    "REMOVE_UNNECESSARY_WORLD_WRITE_OR_READ"
                ),
                "source": FILE_NAME,
            },
            reason=reason,
            risk_level=(
                Severity.HIGH.value
            ),
        )

    def request_containment(
        self,
        platform_id: Optional[str],
        finding: SecurityFinding,
        mode: ContainmentMode,
    ) -> Optional[
        pathlib.Path
    ]:
        if not platform_id:
            return None

        reason = {
            "finding_id": (
                finding.finding_id
            ),
            "category": (
                finding.category
            ),
            "severity": (
                finding.severity
            ),
            "title": finding.title,
            "target": finding.target,
            "containment_mode": (
                mode.value
            ),
        }

        if not self._allowed(
            platform_id,
            "CONTAINMENT",
            reason,
            MAX_CONTAINMENT_REQUESTS_PER_HOUR,
        ):
            return None

        return self._write_request(
            platform_id=platform_id,
            action=(
                "ASSESS_AND_REMEDIATE"
            ),
            scope={
                "security_containment": (
                    mode.value
                ),
                "target": (
                    finding.target
                ),
                "minimum_blast_radius": True,
                "full_shutdown_forbidden": True,
                "preserve_unaffected_services": True,
                "source": FILE_NAME,
            },
            reason=reason,
            risk_level=(
                finding.severity
            ),
        )

    def _allowed(
        self,
        platform_id: str,
        action_class: str,
        reason: Dict[str, Any],
        hourly_limit: int,
    ) -> bool:
        one_hour_ago = (
            epoch_now()
            - 3600
        )

        count = self.db.conn.execute(
            """
            SELECT COUNT(*) AS n
            FROM repair_guard
            WHERE platform_id=?
              AND action_class=?
              AND requested_epoch>=?
            """,
            (
                platform_id,
                action_class,
                one_hour_ago,
            ),
        ).fetchone()[
            "n"
        ]

        if count >= (
            hourly_limit
        ):
            return False

        digest = canonical_digest(
            reason
        )

        duplicate = self.db.conn.execute(
            """
            SELECT guard_id
            FROM repair_guard
            WHERE platform_id=?
              AND action_class=?
              AND reason_digest=?
              AND requested_epoch>=?
            LIMIT 1
            """,
            (
                platform_id,
                action_class,
                digest,
                epoch_now()
                - 900,
            ),
        ).fetchone()

        return (
            duplicate is None
        )

    def _write_request(
        self,
        platform_id: str,
        action: str,
        scope: Dict[str, Any],
        reason: Dict[str, Any],
        risk_level: str,
    ) -> pathlib.Path:
        request_id = str(
            uuid.uuid4()
        )

        payload = {
            "request_id": (
                request_id
            ),
            "platform_id": (
                platform_id
            ),
            "action": action,
            "scope": scope,
            "reason": json_dumps(
                sanitize_for_evidence(
                    reason
                )
            ),
            "risk_level": (
                risk_level
            ),
            "backup_required": True,
            "rollback_required": True,
            "independent_verification_required": True,
            "owner_authority": (
                SUPREME_AUTHORITY
            ),
            "generated_by": FILE_NAME,
            "created_at": utc_now(),
            "status": (
                "PENDING_EXECUTOR"
            ),
        }

        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode(
            "utf-8"
        )

        envelope = {
            "schema": (
                SECURITY_REQUEST_SCHEMA
            ),
            "payload": payload,
            "integrity": {
                "algorithm": (
                    "SHA-256"
                ),
                "digest": (
                    sha256_bytes(
                        canonical
                    )
                ),
            },
        }

        path = (
            REQUEST_DIR
            / f"{request_id}.json"
        )

        atomic_write_json(
            path,
            envelope,
        )

        self.db.conn.execute(
            """
            INSERT INTO repair_guard(
                guard_id,
                platform_id,
                action_class,
                reason_digest,
                requested_epoch
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(
                    uuid.uuid4()
                ),
                platform_id,
                (
                    "CONTAINMENT"
                    if (
                        "security_containment"
                        in scope
                    )
                    else "REPAIR"
                ),
                canonical_digest(
                    reason
                ),
                epoch_now(),
            ),
        )

        self.db.conn.commit()

        return path


# =====================================================================
# SECURITY POSTURE ENGINE
# =====================================================================

class SecurityPostureEngine:
    def __init__(
        self,
        db: DefenseDatabase,
    ):
        self.db = db

    def update_platform(
        self,
        platform: PlatformRecord,
        findings: Sequence[
            SecurityFinding
        ],
        risk_score: int,
        state: SecurityState,
    ) -> None:
        now = utc_now()

        last_clean = (
            now
            if not findings
            else None
        )

        existing = self.db.conn.execute(
            """
            SELECT last_clean_scan
            FROM platform_security
            WHERE platform_id=?
            """,
            (
                platform.platform_id,
            ),
        ).fetchone()

        previous_clean = (
            existing[
                "last_clean_scan"
            ]
            if existing
            else None
        )

        self.db.conn.execute(
            """
            INSERT INTO platform_security(
                platform_id,
                name,
                root_path,
                state,
                last_scan,
                last_clean_scan,
                risk_score,
                metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(platform_id)
            DO UPDATE SET
                name=excluded.name,
                root_path=excluded.root_path,
                state=excluded.state,
                last_scan=excluded.last_scan,
                last_clean_scan=excluded.last_clean_scan,
                risk_score=excluded.risk_score,
                metadata_json=excluded.metadata_json
            """,
            (
                platform.platform_id,
                platform.name,
                platform.root_path,
                state.value,
                now,
                (
                    last_clean
                    or previous_clean
                ),
                risk_score,
                json_dumps(
                    {
                        "open_findings": len(
                            findings
                        ),
                        "highest_severity": (
                            self._highest(
                                findings
                            )
                        ),
                    }
                ),
            ),
        )

        self.db.conn.commit()

    def _highest(
        self,
        findings: Sequence[
            SecurityFinding
        ],
    ) -> Optional[str]:
        if not findings:
            return None

        ranking = {
            Severity.INFO.value: 0,
            Severity.LOW.value: 1,
            Severity.MEDIUM.value: 2,
            Severity.HIGH.value: 3,
            Severity.CRITICAL.value: 4,
        }

        return max(
            (
                finding.severity
                for finding
                in findings
            ),
            key=lambda value: (
                ranking.get(
                    value,
                    0,
                )
            ),
        )


# =====================================================================
# RUNTIME LOCK
# =====================================================================

class DefenseRuntimeLock:
    def __init__(
        self,
    ):
        self.path = (
            LOCK_DIR
            / "cyber-defense-04.lock"
        )

        self.fd: Optional[
            int
        ] = None

    def __enter__(
        self,
    ):
        try:
            self.fd = os.open(
                str(
                    self.path
                ),
                os.O_CREAT
                | os.O_EXCL
                | os.O_WRONLY,
                0o600,
            )

        except FileExistsError:
            try:
                pid = int(
                    self.path.read_text(
                        encoding="utf-8"
                    ).strip()
                )

                os.kill(
                    pid,
                    0,
                )

                raise RuntimeError(
                    f"Cyber defense already running with PID {pid}"
                )

            except (
                ValueError,
                ProcessLookupError,
            ):
                with contextlib.suppress(
                    FileNotFoundError
                ):
                    self.path.unlink()

                self.fd = os.open(
                    str(
                        self.path
                    ),
                    os.O_CREAT
                    | os.O_EXCL
                    | os.O_WRONLY,
                    0o600,
                )

        os.write(
            self.fd,
            str(
                os.getpid()
            ).encode(
                "ascii"
            ),
        )

        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ):
        if self.fd is not None:
            os.close(
                self.fd
            )

        with contextlib.suppress(
            FileNotFoundError
        ):
            self.path.unlink()


# =====================================================================
# MAIN DEFENSE ENGINE
# =====================================================================

class MajdSovereignCyberDefense:
    def __init__(
        self,
    ):
        self.db = DefenseDatabase(
            DEFENSE_DB_PATH
        )

        self.platform_source = (
            PlatformSource(
                MASTER_DB_PATH,
                RUNTIME_DB_PATH,
            )
        )

        self.self_integrity = (
            SelfIntegrityEngine(
                self.db
            )
        )

        self.filesystem = (
            FilesystemSecurityEngine()
        )

        self.git = (
            GitSecurityEngine()
        )

        self.network = (
            NetworkExposureEngine(
                self.db
            )
        )

        self.nginx = (
            NginxSecurityEngine()
        )

        self.services = (
            ServiceSecurityEngine()
        )

        self.ai = (
            AIAgentSecurityEngine()
        )

        self.cross_platform = (
            CrossPlatformBoundaryEngine()
        )

        self.baseline = (
            BaselineEngine(
                self.db
            )
        )

        self.risk = (
            SecurityRiskEngine()
        )

        self.evidence = (
            SecurityEvidenceEngine(
                self.db
            )
        )

        self.finding_store = (
            FindingStore(
                self.db
            )
        )

        self.incidents = (
            SecurityIncidentEngine(
                self.db
            )
        )

        self.containment = (
            SurgicalContainmentPolicy()
        )

        self.executor = (
            DefenseExecutionBridge(
                self.db
            )
        )

        self.posture = (
            SecurityPostureEngine(
                self.db
            )
        )

        self.stop_event = (
            threading.Event()
        )

        self.last_full_scan_epoch = 0

    # -----------------------------------------------------------------
    # BOOTSTRAP
    # -----------------------------------------------------------------

    def bootstrap(
        self,
    ) -> Dict[str, Any]:
        platforms = (
            self.platform_source
            .platforms()
        )

        baseline_count = 0

        for platform in platforms:
            try:
                self.baseline.baseline_platform(
                    platform
                )

                baseline_count += 1

            except Exception as exc:
                LOG.warning(
                    "BASELINE_FAILED | %s | %s",
                    platform.name,
                    exc,
                )

        state = {
            "app": APP_NAME,
            "file": FILE_NAME,
            "version": VERSION,
            "authority": SUPREME_AUTHORITY,
            "platforms_discovered": len(
                platforms
            ),
            "platforms_baselined": (
                baseline_count
            ),
            "majd_git_present": (
                MAJD_GIT_ROOT.exists()
            ),
            "majd_in_present": (
                MAJD_IN_ROOT.exists()
            ),
            "capabilities": {
                "SELF_PROTECTION": True,
                "SELF_INTEGRITY": True,
                "PLATFORM_DISCOVERY": True,
                "FILESYSTEM_SECURITY": True,
                "FILE_PERMISSION_SECURITY": True,
                "SECRET_EXPOSURE_DETECTION": True,
                "GIT_SECURITY": True,
                "NETWORK_EXPOSURE_INVENTORY": True,
                "CONTROL_PLANE_EXPOSURE_DETECTION": True,
                "NGINX_SECURITY_CHECK": True,
                "SERVICE_SECURITY_CHECK": True,
                "AI_AGENT_BOUNDARY_CHECKS": True,
                "CROSS_PLATFORM_BOUNDARY_HEURISTICS": True,
                "BASELINE_DRIFT": True,
                "RISK_SCORING": True,
                "INCIDENT_CORRELATION": True,
                "SURGICAL_CONTAINMENT_POLICY": True,
                "ANTI_LOOP": True,
                "BLAST_RADIUS_LIMIT": True,
                "EXECUTOR_02_BRIDGE": True,
                "INDEPENDENT_VERIFICATION_03_REQUIRED": True,
                "FULL_SHUTDOWN_AUTOMATIC": False,
                "OFFENSIVE_EXPLOITATION": False,
            },
            "availability_policy": {
                "preserve_unaffected_services": True,
                "smallest_containment_scope": True,
                "full_shutdown_last_resort": True,
            },
            "truth": {
                "defense_engine_bootstrapped": True,
                "all_platforms_proven_secure": False,
                "independent_verification_required": True,
            },
            "timestamp": utc_now(),
        }

        atomic_write_json(
            SECURITY_STATE_DIR
            / "cyber-defense-04-capabilities.json",
            state,
        )

        self.db.audit(
            "BOOTSTRAP",
            APP_NAME,
            state,
        )

        return state

    # -----------------------------------------------------------------
    # FULL SCAN
    # -----------------------------------------------------------------

    def scan(
        self,
    ) -> Dict[str, Any]:
        cycle_id = str(
            uuid.uuid4()
        )

        started_at = utc_now()

        LOG.info(
            "SECURITY_SCAN_STARTED | %s",
            cycle_id,
        )

        platforms = (
            self.platform_source
            .platforms()
        )

        all_findings: List[
            SecurityFinding
        ] = []

        errors = []

        # Self protection
        try:
            all_findings.extend(
                self.self_integrity.check()
            )
        except Exception as exc:
            errors.append(
                f"self_integrity:{exc}"
            )

        # Shared infrastructure
        try:
            inventory = (
                self.network.inventory()
            )

            all_findings.extend(
                self.network.findings(
                    inventory
                )
            )
        except Exception as exc:
            errors.append(
                f"network:{exc}"
            )

        try:
            all_findings.extend(
                self.nginx.scan()
            )
        except Exception as exc:
            errors.append(
                f"nginx:{exc}"
            )

        try:
            all_findings.extend(
                self.services
                .scan_known_control_plane()
            )
        except Exception as exc:
            errors.append(
                f"services:{exc}"
            )

        try:
            all_findings.extend(
                self.ai.scan()
            )
        except Exception as exc:
            errors.append(
                f"ai:{exc}"
            )

        # Per platform
        platform_findings_map: Dict[
            str,
            List[
                SecurityFinding
            ],
        ] = {}

        for platform in platforms:
            platform_findings: List[
                SecurityFinding
            ] = []

            try:
                platform_findings.extend(
                    self.filesystem.scan(
                        platform
                    )
                )
            except Exception as exc:
                errors.append(
                    f"{platform.name}:filesystem:{exc}"
                )

            try:
                platform_findings.extend(
                    self.git.scan(
                        platform
                    )
                )
            except Exception as exc:
                errors.append(
                    f"{platform.name}:git:{exc}"
                )

            try:
                platform_findings.extend(
                    self.baseline.drift(
                        platform
                    )
                )
            except Exception as exc:
                errors.append(
                    f"{platform.name}:baseline:{exc}"
                )

            platform_findings_map[
                platform.platform_id
            ] = platform_findings

            all_findings.extend(
                platform_findings
            )

        # Cross-platform boundary
        try:
            cross_findings = (
                self.cross_platform.scan(
                    platforms
                )
            )

            all_findings.extend(
                cross_findings
            )

            for finding in (
                cross_findings
            ):
                if finding.platform_id:
                    platform_findings_map.setdefault(
                        finding.platform_id,
                        [],
                    ).append(
                        finding
                    )

        except Exception as exc:
            errors.append(
                f"cross_platform:{exc}"
            )

        # Store findings/evidence
        stored_findings = []

        for finding in (
            all_findings
        ):
            stored_id = (
                self.finding_store
                .save(
                    finding
                )
            )

            finding.finding_id = (
                stored_id
            )

            stored_findings.append(
                finding
            )

            self.evidence.write(
                evidence_type=(
                    "SECURITY_FINDING"
                ),
                target=(
                    finding.target
                ),
                payload=(
                    dataclasses.asdict(
                        finding
                    )
                ),
                platform_id=(
                    finding.platform_id
                ),
            )

        # Posture update
        for platform in platforms:
            findings = (
                platform_findings_map
                .get(
                    platform.platform_id,
                    [],
                )
            )

            score = self.risk.score(
                findings
            )

            state = self.risk.state(
                score
            )

            self.posture.update_platform(
                platform,
                findings,
                score,
                state,
            )

        # Incidents
        incidents = (
            self.incidents.correlate(
                stored_findings
            )
        )

        # Automated response requests
        repair_requests = 0
        containment_requests = 0

        for finding in (
            stored_findings
        ):
            if not (
                finding.platform_id
            ):
                continue

            mode = (
                self.containment.decide(
                    finding
                )
            )

            if (
                mode
                != ContainmentMode.NONE
            ):
                if (
                    self.containment
                    .allow_automatic(
                        finding,
                        mode,
                    )
                ):
                    request = (
                        self.executor
                        .request_containment(
                            finding.platform_id,
                            finding,
                            mode,
                        )
                    )

                    if request:
                        containment_requests += 1

                continue

            if (
                finding.auto_repair_allowed
            ):
                reason = {
                    "finding_id": (
                        finding.finding_id
                    ),
                    "category": (
                        finding.category
                    ),
                    "title": finding.title,
                    "target": finding.target,
                }

                if (
                    finding.category
                    == FindingCategory
                    .FILE_PERMISSION
                    .value
                ):
                    request = (
                        self.executor
                        .request_file_permission_repair(
                            finding.platform_id,
                            finding.target,
                            reason,
                        )
                    )

                else:
                    request = (
                        self.executor
                        .request_repair(
                            finding.platform_id,
                            reason,
                            finding.severity,
                        )
                    )

                if request:
                    repair_requests += 1

        summary = {
            "cycle_id": cycle_id,
            "started_at": (
                started_at
            ),
            "completed_at": utc_now(),
            "platforms_checked": len(
                platforms
            ),
            "findings": len(
                stored_findings
            ),
            "critical_findings": sum(
                1
                for finding
                in stored_findings
                if finding.severity
                == Severity.CRITICAL.value
            ),
            "high_findings": sum(
                1
                for finding
                in stored_findings
                if finding.severity
                == Severity.HIGH.value
            ),
            "incidents_opened": len(
                incidents
            ),
            "repair_requests_created": (
                repair_requests
            ),
            "containment_requests_created": (
                containment_requests
            ),
            "errors": errors,
            "success": not errors,
            "availability_policy": {
                "full_shutdown_executed": False,
                "surgical_containment_only": True,
                "unaffected_services_preserved": True,
            },
            "independent_verification": (
                "REQUIRED_BY_FILE_03"
            ),
        }

        atomic_write_json(
            SECURITY_STATE_DIR
            / "last-security-scan.json",
            summary,
        )

        self.db.heartbeat(
            (
                "SUCCESS"
                if not errors
                else "DEGRADED"
            ),
            summary,
        )

        self.db.audit(
            "SECURITY_SCAN",
            cycle_id,
            summary,
        )

        LOG.info(
            "SECURITY_SCAN_COMPLETED | %s | findings=%s",
            cycle_id,
            len(
                stored_findings
            ),
        )

        return summary

    # -----------------------------------------------------------------
    # LOOP
    # -----------------------------------------------------------------

    def loop(
        self,
    ) -> int:
        self.bootstrap()

        def stop_handler(
            signum,
            frame,
        ):
            LOG.info(
                "DEFENSE_STOP_SIGNAL | %s",
                signum,
            )

            self.stop_event.set()

        signal.signal(
            signal.SIGTERM,
            stop_handler,
        )

        signal.signal(
            signal.SIGINT,
            stop_handler,
        )

        with DefenseRuntimeLock():
            LOG.info(
                "MAJD_SOVEREIGN_CYBER_DEFENSE_STARTED | pid=%s",
                os.getpid(),
            )

            while not (
                self.stop_event
                .is_set()
            ):
                started = (
                    time.monotonic()
                )

                try:
                    self.scan()

                except Exception as exc:
                    LOG.exception(
                        "DEFENSE_LOOP_SCAN_FAILED | %s",
                        exc,
                    )

                    self.db.heartbeat(
                        "FAILED",
                        {
                            "error": str(
                                exc
                            ),
                            "error_type": (
                                type(
                                    exc
                                ).__name__
                            ),
                            "timestamp": (
                                utc_now()
                            ),
                        },
                    )

                elapsed = (
                    time.monotonic()
                    - started
                )

                wait_seconds = max(
                    1.0,
                    (
                        DEFENSE_INTERVAL_SECONDS
                        - elapsed
                    ),
                )

                self.stop_event.wait(
                    wait_seconds
                )

        LOG.info(
            "MAJD_SOVEREIGN_CYBER_DEFENSE_STOPPED"
        )

        return 0

    # -----------------------------------------------------------------
    # STATUS
    # -----------------------------------------------------------------

    def status(
        self,
    ) -> Dict[str, Any]:
        platform_states = (
            self.db.conn.execute(
                """
                SELECT
                    state,
                    COUNT(*) AS n
                FROM platform_security
                GROUP BY state
                """
            ).fetchall()
        )

        finding_states = (
            self.db.conn.execute(
                """
                SELECT
                    severity,
                    COUNT(*) AS n
                FROM findings
                WHERE status='OPEN'
                GROUP BY severity
                """
            ).fetchall()
        )

        incident_states = (
            self.db.conn.execute(
                """
                SELECT
                    severity,
                    COUNT(*) AS n
                FROM incidents
                WHERE state='OPEN'
                GROUP BY severity
                """
            ).fetchall()
        )

        last_heartbeat = (
            self.db.conn.execute(
                """
                SELECT *
                FROM heartbeats
                ORDER BY created_at DESC
                LIMIT 1
                """
            ).fetchone()
        )

        return {
            "app": APP_NAME,
            "file": FILE_NAME,
            "version": VERSION,
            "authority": (
                SUPREME_AUTHORITY
            ),
            "platform_security_states": {
                row[
                    "state"
                ]: row[
                    "n"
                ]
                for row
                in platform_states
            },
            "open_findings": {
                row[
                    "severity"
                ]: row[
                    "n"
                ]
                for row
                in finding_states
            },
            "open_incidents": {
                row[
                    "severity"
                ]: row[
                    "n"
                ]
                for row
                in incident_states
            },
            "last_heartbeat": (
                dict(
                    last_heartbeat
                )
                if last_heartbeat
                else None
            ),
            "security_truth": {
                "defense_runtime_available": True,
                "continuous_loop_active": (
                    self._lock_active()
                ),
                "full_platform_shutdown_policy": (
                    "LAST_RESORT_ONLY"
                ),
                "automatic_full_shutdown": False,
                "surgical_containment": True,
                "independent_verification": (
                    "FILE_03"
                ),
                "all_platforms_secure_claim": False,
            },
            "timestamp": utc_now(),
        }

    def _lock_active(
        self,
    ) -> bool:
        path = (
            LOCK_DIR
            / "cyber-defense-04.lock"
        )

        if not path.exists():
            return False

        try:
            pid = int(
                path.read_text(
                    encoding="utf-8"
                ).strip()
            )

            os.kill(
                pid,
                0,
            )

            return True

        except Exception:
            return False

    # -----------------------------------------------------------------
    # ACCEPT BASELINES
    # -----------------------------------------------------------------

    def baseline(
        self,
    ) -> Dict[str, Any]:
        self_result = (
            self.self_integrity
            .accept_current_baseline()
        )

        platform_results = []

        for platform in (
            self.platform_source
            .platforms()
        ):
            try:
                platform_results.append(
                    self.baseline_engine_for(
                        platform
                    )
                )

            except Exception as exc:
                platform_results.append(
                    {
                        "platform_id": (
                            platform.platform_id
                        ),
                        "status": "FAILED",
                        "error": str(
                            exc
                        ),
                    }
                )

        return {
            "self": self_result,
            "platforms": (
                platform_results
            ),
            "timestamp": utc_now(),
        }

    def baseline_engine_for(
        self,
        platform: PlatformRecord,
    ) -> Dict[str, Any]:
        return self.baseline.baseline_platform(
            platform
        )


# =====================================================================
# CLI
# =====================================================================

def build_parser(
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=FILE_NAME,
        description=(
            "MAJD Sovereign Continuous Cyber Defense"
        ),
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    sub.add_parser(
        "bootstrap",
        help=(
            "Initialize cyber-defense state."
        ),
    )

    sub.add_parser(
        "baseline",
        help=(
            "Accept current maintenance-center "
            "and platform critical-file baselines."
        ),
    )

    sub.add_parser(
        "scan",
        help=(
            "Run one defensive security scan."
        ),
    )

    sub.add_parser(
        "loop",
        help=(
            "Run permanent sovereign defense loop."
        ),
    )

    sub.add_parser(
        "status",
        help=(
            "Show truthful cyber-defense state."
        ),
    )

    sub.add_parser(
        "network",
        help=(
            "Show current listening-port inventory."
        ),
    )

    sub.add_parser(
        "self-check",
        help=(
            "Check maintenance-center self-integrity."
        ),
    )

    return parser


# =====================================================================
# MAIN
# =====================================================================

def main(
) -> int:
    parser = build_parser()

    args = parser.parse_args()

    defense = (
        MajdSovereignCyberDefense()
    )

    try:
        if args.command == (
            "bootstrap"
        ):
            print(
                json_dumps(
                    defense.bootstrap()
                )
            )

            return 0

        if args.command == (
            "baseline"
        ):
            print(
                json_dumps(
                    defense.baseline()
                )
            )

            return 0

        if args.command == (
            "scan"
        ):
            defense.bootstrap()

            result = defense.scan()

            print(
                json_dumps(
                    result
                )
            )

            return (
                0
                if result[
                    "success"
                ]
                else 1
            )

        if args.command == (
            "loop"
        ):
            return defense.loop()

        if args.command == (
            "status"
        ):
            print(
                json_dumps(
                    defense.status()
                )
            )

            return 0

        if args.command == (
            "network"
        ):
            inventory = (
                defense.network
                .inventory()
            )

            findings = (
                defense.network
                .findings(
                    inventory
                )
            )

            print(
                json_dumps(
                    {
                        "inventory": (
                            inventory
                        ),
                        "findings": [
                            dataclasses.asdict(
                                finding
                            )
                            for finding
                            in findings
                        ],
                    }
                )
            )

            return 0

        if args.command == (
            "self-check"
        ):
            findings = (
                defense.self_integrity
                .check()
            )

            print(
                json_dumps(
                    [
                        dataclasses.asdict(
                            finding
                        )
                        for finding
                        in findings
                    ]
                )
            )

            return (
                1
                if findings
                else 0
            )

        parser.error(
            "Unknown command."
        )

        return 2

    except KeyboardInterrupt:
        LOG.warning(
            "MAJD_CYBER_DEFENSE_INTERRUPTED"
        )

        return 130

    except Exception as exc:
        LOG.exception(
            "MAJD_CYBER_DEFENSE_FATAL | %s",
            exc,
        )

        print(
            json_dumps(
                {
                    "status": "FAILED",
                    "error_type": (
                        type(
                            exc
                        ).__name__
                    ),
                    "error": str(
                        exc
                    ),
                    "timestamp": utc_now(),
                }
            )
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(
        main()
    )

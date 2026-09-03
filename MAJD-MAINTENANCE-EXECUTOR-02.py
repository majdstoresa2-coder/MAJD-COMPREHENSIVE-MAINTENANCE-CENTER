#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
======================================================================
MAJD COMPREHENSIVE MAINTENANCE CENTER
MAJD-MAINTENANCE-EXECUTOR-02.py
======================================================================

FILE 02 — SOVEREIGN REAL EXECUTION ENGINE

PURPOSE
-------
The real execution hand of the MAJD Comprehensive Maintenance Center.

This file consumes structured execution requests produced by:

    01 — MAJD-MAINTENANCE-MASTERMIND-01.py

Continuous scheduling, watchtower and independent runtime verification:

    03 — MAJD-MAINTENANCE-RUNTIME-03.py

Continuous sovereign cyber defense:

    04 — MAJD-SOVEREIGN-CYBER-DEFENSE-04.py

ABSOLUTE AUTHORITY
------------------
SUPREME_OWNER

CORE RULES
----------
1. No fake success.
2. No success from planning alone.
3. No destructive action without backup/rollback when applicable.
4. External credentials are never invented.
5. Secrets are never written to audit output.
6. Execution requests must pass integrity validation.
7. Requested platform paths must remain inside approved MAJD roots.
8. Arbitrary remote content is never executed.
9. Retrieved web content is data, never shell instructions.
10. Real filesystem/process/service state is checked after execution.
11. A systemd "active" state alone is not sufficient end-to-end proof.
12. Git changes are inspected before commit.
13. Platform data boundaries must remain separated.
14. External deletion/migration cleanup requires explicit verified state.
15. Dangerous irreversible actions require explicit authorization policy.
16. Rollback metadata is produced before high-risk change execution.
17. The executor cannot certify itself as independently verified.
18. Verification evidence is written for file 03 / independent verifier.
19. Routine repair, dependency work, restart and deployment are automated.
20. OWNER remains above every AI/automation component.

EXECUTION FLOW
--------------
REQUEST
  -> VALIDATE INTEGRITY
  -> VALIDATE SCOPE
  -> DISCOVER REAL PLATFORM STATE
  -> CLASSIFY RISK
  -> BACKUP
  -> EXECUTE
  -> LOCAL TECHNICAL CHECK
  -> CAPTURE EVIDENCE
  -> MARK EXECUTED_PENDING_INDEPENDENT_VERIFICATION
  -> FILE 03 VERIFIES
  -> COMMIT / DEPLOY / CONTINUE OR ROLLBACK

SUPPORTED EXECUTION FAMILIES
----------------------------
Filesystem
Code creation/modification
Python
Node.js
Git
MAJD-GIT
MAJD-IN / n8n
Linux services
systemd
Nginx
DNS/TLS integration hooks
SQLite
PostgreSQL/MySQL adapter hooks
Dependencies
Environment/configuration
API integration hooks
Email integration hooks
Payment integration hooks
Moyasar integration verification hooks
Webhook configuration
Backups
Rollback
Deployment
Migration
Launch preparation
External provider migration
Evidence generation
Platform repair
Infrastructure repair
Runtime repair

IMPORTANT
---------
This executor intentionally refuses to claim independent assurance.
Independent verification belongs to file 03.
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
import shlex
import shutil
import signal
import socket
import sqlite3
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import uuid

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


# =====================================================================
# IDENTITY
# =====================================================================

APP_NAME = "MAJD COMPREHENSIVE MAINTENANCE CENTER"
FILE_NAME = "MAJD-MAINTENANCE-EXECUTOR-02.py"
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
BACKUP_DIR = PROJECT_ROOT / "backups"
ROLLBACK_DIR = PROJECT_ROOT / "rollback"
EVIDENCE_DIR = PROJECT_ROOT / "evidence"
WORK_DIR = PROJECT_ROOT / "work"
LOCK_DIR = PROJECT_ROOT / "locks"

MASTER_DB_PATH = DATA_DIR / "majd_maintenance_mastermind.sqlite3"
EXECUTOR_DB_PATH = DATA_DIR / "majd_maintenance_executor.sqlite3"

LOG_PATH = LOG_DIR / "executor-02.log"

DEFAULT_TIMEOUT = int(
    os.environ.get("MAJD_EXECUTOR_TIMEOUT", "600")
)

MAX_OUTPUT_BYTES = int(
    os.environ.get(
        "MAJD_EXECUTOR_MAX_OUTPUT_BYTES",
        str(2 * 1024 * 1024),
    )
)

MAX_BACKUP_FILE_BYTES = int(
    os.environ.get(
        "MAJD_EXECUTOR_MAX_BACKUP_FILE_BYTES",
        str(2 * 1024 * 1024 * 1024),
    )
)

ALLOWED_MAJD_ROOTS = tuple(
    pathlib.Path(x).resolve()
    for x in os.environ.get(
        "MAJD_ALLOWED_ROOTS",
        "/root:/srv:/opt",
    ).split(":")
    if x.strip()
)

PROTECTED_PATHS = {
    pathlib.Path("/"),
    pathlib.Path("/bin"),
    pathlib.Path("/boot"),
    pathlib.Path("/dev"),
    pathlib.Path("/etc"),
    pathlib.Path("/lib"),
    pathlib.Path("/lib64"),
    pathlib.Path("/proc"),
    pathlib.Path("/sys"),
    pathlib.Path("/usr"),
    pathlib.Path("/var"),
}

SENSITIVE_NAME_PATTERNS = (
    "password",
    "passwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "private_key",
    "access_key",
    "client_secret",
    "authorization",
    "cookie",
)

for directory in (
    DATA_DIR,
    STATE_DIR,
    LOG_DIR,
    REQUEST_DIR,
    PROCESSED_DIR,
    FAILED_DIR,
    BACKUP_DIR,
    ROLLBACK_DIR,
    EVIDENCE_DIR,
    WORK_DIR,
    LOCK_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)


# =====================================================================
# LOGGING
# =====================================================================

logging.basicConfig(
    level=os.environ.get("MAJD_LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
    ],
)

LOG = logging.getLogger("MAJD-EXECUTOR-02")


# =====================================================================
# ENUMS
# =====================================================================

class ExecutionStatus(str, Enum):
    PENDING_EXECUTOR = "PENDING_EXECUTOR"
    VALIDATING = "VALIDATING"
    BACKING_UP = "BACKING_UP"
    EXECUTING = "EXECUTING"
    LOCAL_VERIFYING = "LOCAL_VERIFYING"
    EXECUTED_PENDING_INDEPENDENT_VERIFICATION = (
        "EXECUTED_PENDING_INDEPENDENT_VERIFICATION"
    )
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    BLOCKED = "BLOCKED"
    OWNER_ACTION_REQUIRED = "OWNER_ACTION_REQUIRED"
    EXTERNAL_DEPENDENCY_REQUIRED = "EXTERNAL_DEPENDENCY_REQUIRED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ActionClass(str, Enum):
    READ_ONLY = "READ_ONLY"
    REVERSIBLE = "REVERSIBLE"
    DESTRUCTIVE = "DESTRUCTIVE"
    EXTERNAL = "EXTERNAL"


# =====================================================================
# DATA MODELS
# =====================================================================

@dataclass
class CommandResult:
    command: List[str]
    returncode: int
    stdout: str
    stderr: str
    started_at: str
    completed_at: str
    duration_seconds: float
    success: bool


@dataclass
class BackupRecord:
    backup_id: str
    request_id: str
    source_path: str
    backup_path: str
    kind: str
    sha256: str
    created_at: str


@dataclass
class ExecutionResult:
    request_id: str
    action: str
    platform_id: Optional[str]
    status: str
    changed: bool
    local_checks_passed: bool
    independent_verification_required: bool
    backup_ids: List[str] = field(default_factory=list)
    evidence_ids: List[str] = field(default_factory=list)
    messages: List[str] = field(default_factory=list)
    started_at: str = ""
    completed_at: str = ""


# =====================================================================
# UTILITIES
# =====================================================================

def utc_now() -> str:
    return dt.datetime.now(
        dt.timezone.utc
    ).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as fh:
        while True:
            chunk = fh.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)

    return digest.hexdigest()


def stable_id(prefix: str, *parts: str) -> str:
    payload = "::".join(
        str(x) for x in parts
    ).encode("utf-8")

    return (
        f"{prefix}_"
        f"{hashlib.sha256(payload).hexdigest()[:24]}"
    )


def json_dumps(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        default=str,
    )


def load_json(path: pathlib.Path) -> Dict[str, Any]:
    with path.open(
        "r",
        encoding="utf-8",
    ) as fh:
        value = json.load(fh)

    if not isinstance(value, dict):
        raise ValueError(
            f"Expected JSON object: {path}"
        )

    return value


def atomic_write_text(
    path: pathlib.Path,
    content: str,
    mode: Optional[int] = None,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    tmp = path.with_name(
        f".{path.name}.{uuid.uuid4().hex}.tmp"
    )

    tmp.write_text(
        content,
        encoding="utf-8",
    )

    if mode is not None:
        os.chmod(tmp, mode)

    os.replace(tmp, path)


def atomic_write_json(
    path: pathlib.Path,
    payload: Any,
) -> None:
    atomic_write_text(
        path,
        json_dumps(payload),
    )


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        output = {}

        for key, item in value.items():
            lowered = str(key).lower()

            if any(
                token in lowered
                for token in SENSITIVE_NAME_PATTERNS
            ):
                output[key] = "***REDACTED***"
            else:
                output[key] = redact(item)

        return output

    if isinstance(value, list):
        return [
            redact(x)
            for x in value
        ]

    if isinstance(value, tuple):
        return tuple(
            redact(x)
            for x in value
        )

    return value


def truncate_output(
    value: str,
    max_bytes: int = MAX_OUTPUT_BYTES,
) -> str:
    raw = value.encode(
        "utf-8",
        errors="replace",
    )

    if len(raw) <= max_bytes:
        return value

    return (
        raw[:max_bytes]
        .decode(
            "utf-8",
            errors="replace",
        )
        + "\n...[OUTPUT TRUNCATED]..."
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

    if resolved in PROTECTED_PATHS:
        raise PermissionError(
            f"Protected system path rejected: {resolved}"
        )

    if not any(
        path_within(
            resolved,
            root,
        )
        for root in ALLOWED_MAJD_ROOTS
    ):
        raise PermissionError(
            f"Path outside approved MAJD roots: {resolved}"
        )

    return resolved


def command_exists(
    executable: str,
) -> bool:
    return shutil.which(
        executable
    ) is not None


# =====================================================================
# DATABASE
# =====================================================================

class ExecutorDatabase:
    def __init__(
        self,
        path: pathlib.Path,
    ):
        self.path = path

        self.conn = sqlite3.connect(
            str(path),
            timeout=30,
        )

        self.conn.row_factory = sqlite3.Row

        self.conn.execute(
            "PRAGMA journal_mode=WAL"
        )

        self.conn.execute(
            "PRAGMA foreign_keys=ON"
        )

        self._migrate()

    def _migrate(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS executions (
                execution_id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL,
                platform_id TEXT,
                action TEXT NOT NULL,
                status TEXT NOT NULL,
                changed INTEGER NOT NULL,
                local_checks_passed INTEGER NOT NULL,
                independent_verification_required INTEGER NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                error TEXT
            );

            CREATE TABLE IF NOT EXISTS commands (
                command_id TEXT PRIMARY KEY,
                execution_id TEXT NOT NULL,
                command_json TEXT NOT NULL,
                returncode INTEGER NOT NULL,
                stdout TEXT NOT NULL,
                stderr TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT NOT NULL,
                duration_seconds REAL NOT NULL,
                success INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS backups (
                backup_id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL,
                source_path TEXT NOT NULL,
                backup_path TEXT NOT NULL,
                kind TEXT NOT NULL,
                sha256 TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS evidence (
                evidence_id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL,
                evidence_type TEXT NOT NULL,
                target TEXT NOT NULL,
                digest TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS rollback_points (
                rollback_id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL,
                platform_path TEXT,
                metadata_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS audit (
                audit_id TEXT PRIMARY KEY,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                target TEXT NOT NULL,
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
                actor,
                action,
                target,
                payload_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid.uuid4()),
                FILE_NAME,
                action,
                target,
                json_dumps(
                    redact(
                        payload or {}
                    )
                ),
                utc_now(),
            ),
        )

        self.conn.commit()


# =====================================================================
# MASTER DATABASE BRIDGE
# =====================================================================

class MasterDatabaseBridge:
    def __init__(
        self,
        path: pathlib.Path,
    ):
        self.path = path

    def connect(
        self,
    ) -> sqlite3.Connection:
        if not self.path.exists():
            raise FileNotFoundError(
                f"Mastermind database missing: {self.path}"
            )

        conn = sqlite3.connect(
            str(self.path),
            timeout=30,
        )

        conn.row_factory = sqlite3.Row

        return conn

    def get_platform(
        self,
        platform_id: str,
    ) -> sqlite3.Row:
        conn = self.connect()

        try:
            row = conn.execute(
                """
                SELECT *
                FROM platforms
                WHERE platform_id=?
                """,
                (platform_id,),
            ).fetchone()

            if not row:
                raise KeyError(
                    f"Unknown platform: {platform_id}"
                )

            return row
        finally:
            conn.close()

    def update_request_status(
        self,
        request_id: str,
        status: str,
    ) -> None:
        conn = self.connect()

        try:
            conn.execute(
                """
                UPDATE execution_requests
                SET status=?
                WHERE request_id=?
                """,
                (
                    status,
                    request_id,
                ),
            )

            conn.commit()
        finally:
            conn.close()


# =====================================================================
# FILE LOCK
# =====================================================================

class RequestLock:
    def __init__(
        self,
        request_id: str,
    ):
        self.path = (
            LOCK_DIR /
            f"{request_id}.lock"
        )

        self.fd: Optional[int] = None

    def __enter__(self):
        try:
            self.fd = os.open(
                str(self.path),
                os.O_CREAT
                | os.O_EXCL
                | os.O_WRONLY,
                0o600,
            )
        except FileExistsError:
            raise RuntimeError(
                f"Request already locked: {self.path.name}"
            )

        os.write(
            self.fd,
            str(os.getpid()).encode(
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
# COMMAND RUNNER
# =====================================================================

class CommandRunner:
    def __init__(
        self,
        db: ExecutorDatabase,
    ):
        self.db = db

    def run(
        self,
        execution_id: str,
        command: Sequence[str],
        cwd: Optional[
            pathlib.Path
        ] = None,
        timeout: int = DEFAULT_TIMEOUT,
        env: Optional[
            Dict[str, str]
        ] = None,
        check: bool = False,
    ) -> CommandResult:
        if not command:
            raise ValueError(
                "Empty command."
            )

        executable = str(
            command[0]
        )

        if os.path.sep not in executable:
            if not command_exists(
                executable
            ):
                raise FileNotFoundError(
                    f"Executable not found: {executable}"
                )

        safe_env = os.environ.copy()

        if env:
            safe_env.update(
                env
            )

        started_dt = dt.datetime.now(
            dt.timezone.utc
        )

        started_at = started_dt.isoformat()

        LOG.info(
            "COMMAND_START | %s | cwd=%s",
            shlex.join(
                [str(x) for x in command]
            ),
            cwd,
        )

        try:
            proc = subprocess.run(
                [
                    str(x)
                    for x in command
                ],
                cwd=(
                    str(cwd)
                    if cwd
                    else None
                ),
                env=safe_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
                check=False,
            )

            stdout = truncate_output(
                proc.stdout or ""
            )

            stderr = truncate_output(
                proc.stderr or ""
            )

            returncode = proc.returncode

        except subprocess.TimeoutExpired as exc:
            stdout = truncate_output(
                exc.stdout.decode()
                if isinstance(
                    exc.stdout,
                    bytes,
                )
                else (
                    exc.stdout or ""
                )
            )

            stderr = truncate_output(
                exc.stderr.decode()
                if isinstance(
                    exc.stderr,
                    bytes,
                )
                else (
                    exc.stderr or ""
                )
            )

            returncode = 124

        completed_dt = dt.datetime.now(
            dt.timezone.utc
        )

        completed_at = (
            completed_dt.isoformat()
        )

        duration = (
            completed_dt
            - started_dt
        ).total_seconds()

        result = CommandResult(
            command=[
                str(x)
                for x in command
            ],
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
            started_at=started_at,
            completed_at=completed_at,
            duration_seconds=duration,
            success=returncode == 0,
        )

        self.db.conn.execute(
            """
            INSERT INTO commands(
                command_id,
                execution_id,
                command_json,
                returncode,
                stdout,
                stderr,
                started_at,
                completed_at,
                duration_seconds,
                success
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid.uuid4()),
                execution_id,
                json_dumps(
                    result.command
                ),
                result.returncode,
                result.stdout,
                result.stderr,
                result.started_at,
                result.completed_at,
                result.duration_seconds,
                int(
                    result.success
                ),
            ),
        )

        self.db.conn.commit()

        LOG.info(
            "COMMAND_END | rc=%s | %.3fs | %s",
            result.returncode,
            result.duration_seconds,
            shlex.join(
                result.command
            ),
        )

        if check and not result.success:
            raise RuntimeError(
                "Command failed: "
                f"{shlex.join(result.command)}\n"
                f"{result.stderr}"
            )

        return result


# =====================================================================
# REQUEST VALIDATOR
# =====================================================================

class ExecutionRequestValidator:
    REQUIRED_SCHEMA = (
        "MAJD_EXECUTION_REQUEST_V1"
    )

    def validate(
        self,
        envelope: Dict[str, Any],
    ) -> Dict[str, Any]:
        if envelope.get(
            "schema"
        ) != self.REQUIRED_SCHEMA:
            raise ValueError(
                "Unsupported execution request schema."
            )

        payload = envelope.get(
            "payload"
        )

        integrity = envelope.get(
            "integrity"
        )

        if not isinstance(
            payload,
            dict,
        ):
            raise ValueError(
                "Missing request payload."
            )

        if not isinstance(
            integrity,
            dict,
        ):
            raise ValueError(
                "Missing request integrity section."
            )

        if integrity.get(
            "algorithm"
        ) != "SHA-256":
            raise ValueError(
                "Unsupported integrity algorithm."
            )

        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(
                ",",
                ":",
            ),
        ).encode(
            "utf-8"
        )

        actual = sha256_bytes(
            canonical
        )

        expected = integrity.get(
            "digest"
        )

        if not expected:
            raise ValueError(
                "Missing integrity digest."
            )

        if not hashlib.compare_digest(
            actual,
            expected,
        ):
            raise ValueError(
                "Execution request integrity mismatch."
            )

        if payload.get(
            "owner_authority"
        ) != SUPREME_AUTHORITY:
            raise PermissionError(
                "Request does not preserve SUPREME_OWNER authority."
            )

        if not payload.get(
            "request_id"
        ):
            raise ValueError(
                "Missing request_id."
            )

        if not payload.get(
            "action"
        ):
            raise ValueError(
                "Missing action."
            )

        return payload


# =====================================================================
# PLATFORM STATE INSPECTOR
# =====================================================================

class PlatformInspector:
    def inspect(
        self,
        platform_path: pathlib.Path,
    ) -> Dict[str, Any]:
        platform_path = validate_platform_path(
            platform_path
        )

        data: Dict[str, Any] = {
            "path": str(
                platform_path
            ),
            "exists": platform_path.exists(),
            "is_directory": platform_path.is_dir(),
            "captured_at": utc_now(),
            "git": False,
            "python": False,
            "node": False,
            "docker": False,
            "systemd_units": [],
            "files": [],
        }

        if not platform_path.exists():
            return data

        if not platform_path.is_dir():
            return data

        data["git"] = (
            platform_path /
            ".git"
        ).exists()

        data["python"] = any(
            (
                platform_path /
                name
            ).exists()
            for name in (
                "requirements.txt",
                "pyproject.toml",
                "setup.py",
            )
        )

        data["node"] = (
            platform_path /
            "package.json"
        ).exists()

        data["docker"] = any(
            (
                platform_path /
                name
            ).exists()
            for name in (
                "Dockerfile",
                "docker-compose.yml",
                "compose.yaml",
            )
        )

        files: List[
            Dict[str, Any]
        ] = []

        try:
            for item in sorted(
                platform_path.iterdir(),
                key=lambda p: p.name.lower(),
            )[:500]:
                info = {
                    "name": item.name,
                    "type": (
                        "dir"
                        if item.is_dir()
                        else "file"
                    ),
                }

                if item.is_file():
                    with contextlib.suppress(
                        OSError
                    ):
                        info["size"] = (
                            item.stat().st_size
                        )

                files.append(
                    info
                )

        except PermissionError:
            pass

        data["files"] = files

        return data


# =====================================================================
# BACKUP ENGINE
# =====================================================================

class BackupEngine:
    def __init__(
        self,
        db: ExecutorDatabase,
        runner: CommandRunner,
    ):
        self.db = db
        self.runner = runner

    def backup_path(
        self,
        request_id: str,
        source: pathlib.Path,
    ) -> BackupRecord:
        source = validate_platform_path(
            source
        )

        if not source.exists():
            raise FileNotFoundError(
                source
            )

        stamp = dt.datetime.now().strftime(
            "%Y%m%d-%H%M%S"
        )

        safe_name = re.sub(
            r"[^A-Za-z0-9_.-]+",
            "_",
            source.name,
        )

        backup_id = str(
            uuid.uuid4()
        )

        if source.is_file():
            if (
                source.stat().st_size
                > MAX_BACKUP_FILE_BYTES
            ):
                raise RuntimeError(
                    "Backup source file exceeds configured safety limit."
                )

            destination = (
                BACKUP_DIR /
                f"{stamp}-{backup_id}-{safe_name}"
            )

            shutil.copy2(
                source,
                destination,
            )

            digest = sha256_file(
                destination
            )

            kind = "FILE"

        else:
            destination = (
                BACKUP_DIR /
                f"{stamp}-{backup_id}-{safe_name}.tar.gz"
            )

            with tarfile.open(
                destination,
                "w:gz",
            ) as archive:
                archive.add(
                    source,
                    arcname=source.name,
                    recursive=True,
                )

            digest = sha256_file(
                destination
            )

            kind = "DIRECTORY"

        record = BackupRecord(
            backup_id=backup_id,
            request_id=request_id,
            source_path=str(
                source
            ),
            backup_path=str(
                destination
            ),
            kind=kind,
            sha256=digest,
            created_at=utc_now(),
        )

        self.db.conn.execute(
            """
            INSERT INTO backups(
                backup_id,
                request_id,
                source_path,
                backup_path,
                kind,
                sha256,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.backup_id,
                record.request_id,
                record.source_path,
                record.backup_path,
                record.kind,
                record.sha256,
                record.created_at,
            ),
        )

        self.db.conn.commit()

        return record

    def create_git_rollback_point(
        self,
        execution_id: str,
        request_id: str,
        platform_path: pathlib.Path,
    ) -> Optional[
        Dict[str, Any]
    ]:
        if not (
            platform_path /
            ".git"
        ).exists():
            return None

        head = self.runner.run(
            execution_id,
            [
                "git",
                "rev-parse",
                "HEAD",
            ],
            cwd=platform_path,
        )

        status = self.runner.run(
            execution_id,
            [
                "git",
                "status",
                "--porcelain",
            ],
            cwd=platform_path,
        )

        if not head.success:
            return None

        rollback = {
            "commit": head.stdout.strip(),
            "dirty": bool(
                status.stdout.strip()
            ),
            "status": status.stdout,
            "platform": str(
                platform_path
            ),
            "created_at": utc_now(),
        }

        rollback_id = str(
            uuid.uuid4()
        )

        self.db.conn.execute(
            """
            INSERT INTO rollback_points(
                rollback_id,
                request_id,
                platform_path,
                metadata_json,
                created_at,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                rollback_id,
                request_id,
                str(
                    platform_path
                ),
                json_dumps(
                    rollback
                ),
                utc_now(),
                "AVAILABLE",
            ),
        )

        self.db.conn.commit()

        return {
            "rollback_id": rollback_id,
            **rollback,
        }


# =====================================================================
# EVIDENCE ENGINE
# =====================================================================

class EvidenceEngine:
    def __init__(
        self,
        db: ExecutorDatabase,
    ):
        self.db = db

    def write(
        self,
        request_id: str,
        evidence_type: str,
        target: str,
        payload: Dict[str, Any],
    ) -> str:
        evidence_id = str(
            uuid.uuid4()
        )

        sanitized = redact(
            payload
        )

        canonical = json.dumps(
            sanitized,
            ensure_ascii=False,
            sort_keys=True,
            separators=(
                ",",
                ":",
            ),
            default=str,
        ).encode(
            "utf-8"
        )

        digest = sha256_bytes(
            canonical
        )

        envelope = {
            "evidence_id": evidence_id,
            "request_id": request_id,
            "evidence_type": evidence_type,
            "target": target,
            "digest": digest,
            "payload": sanitized,
            "created_at": utc_now(),
        }

        path = (
            EVIDENCE_DIR /
            f"{evidence_id}.json"
        )

        atomic_write_json(
            path,
            envelope,
        )

        self.db.conn.execute(
            """
            INSERT INTO evidence(
                evidence_id,
                request_id,
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
                request_id,
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
# GIT ENGINE
# =====================================================================

class GitEngine:
    def __init__(
        self,
        runner: CommandRunner,
    ):
        self.runner = runner

    def is_repo(
        self,
        path: pathlib.Path,
    ) -> bool:
        return (
            path /
            ".git"
        ).exists()

    def status(
        self,
        execution_id: str,
        path: pathlib.Path,
    ) -> CommandResult:
        return self.runner.run(
            execution_id,
            [
                "git",
                "status",
                "--short",
            ],
            cwd=path,
        )

    def branch(
        self,
        execution_id: str,
        path: pathlib.Path,
    ) -> str:
        result = self.runner.run(
            execution_id,
            [
                "git",
                "branch",
                "--show-current",
            ],
            cwd=path,
        )

        return (
            result.stdout.strip()
            if result.success
            else ""
        )

    def head(
        self,
        execution_id: str,
        path: pathlib.Path,
    ) -> str:
        result = self.runner.run(
            execution_id,
            [
                "git",
                "rev-parse",
                "HEAD",
            ],
            cwd=path,
        )

        return (
            result.stdout.strip()
            if result.success
            else ""
        )

    def fetch(
        self,
        execution_id: str,
        path: pathlib.Path,
    ) -> CommandResult:
        return self.runner.run(
            execution_id,
            [
                "git",
                "fetch",
                "--all",
                "--prune",
            ],
            cwd=path,
            timeout=DEFAULT_TIMEOUT,
        )

    def diff_check(
        self,
        execution_id: str,
        path: pathlib.Path,
    ) -> CommandResult:
        return self.runner.run(
            execution_id,
            [
                "git",
                "diff",
                "--check",
            ],
            cwd=path,
        )

    def commit_all(
        self,
        execution_id: str,
        path: pathlib.Path,
        message: str,
    ) -> Dict[str, Any]:
        check = self.diff_check(
            execution_id,
            path,
        )

        if not check.success:
            raise RuntimeError(
                "Git diff integrity check failed."
            )

        status = self.status(
            execution_id,
            path,
        )

        if not status.stdout.strip():
            return {
                "changed": False,
                "reason": "NO_GIT_CHANGES",
            }

        self.runner.run(
            execution_id,
            [
                "git",
                "add",
                "--all",
            ],
            cwd=path,
            check=True,
        )

        commit = self.runner.run(
            execution_id,
            [
                "git",
                "commit",
                "-m",
                message,
            ],
            cwd=path,
        )

        if not commit.success:
            raise RuntimeError(
                "Git commit failed:\n"
                + commit.stderr
            )

        return {
            "changed": True,
            "commit_output": (
                commit.stdout
                or commit.stderr
            ),
            "head": self.head(
                execution_id,
                path,
            ),
        }


# =====================================================================
# PYTHON ENGINE
# =====================================================================

class PythonEngine:
    def __init__(
        self,
        runner: CommandRunner,
    ):
        self.runner = runner

    def discover_files(
        self,
        root: pathlib.Path,
    ) -> List[
        pathlib.Path
    ]:
        files: List[
            pathlib.Path
        ] = []

        for path in root.rglob(
            "*.py"
        ):
            if any(
                part in {
                    ".git",
                    ".venv",
                    "venv",
                    "__pycache__",
                    "node_modules",
                }
                for part in path.parts
            ):
                continue

            files.append(
                path
            )

        return files

    def syntax_check(
        self,
        execution_id: str,
        root: pathlib.Path,
    ) -> Dict[str, Any]:
        files = self.discover_files(
            root
        )

        failures = []

        for file_path in files:
            result = self.runner.run(
                execution_id,
                [
                    sys.executable,
                    "-m",
                    "py_compile",
                    str(file_path),
                ],
                cwd=root,
                timeout=120,
            )

            if not result.success:
                failures.append(
                    {
                        "file": str(
                            file_path
                        ),
                        "stderr": result.stderr,
                    }
                )

        return {
            "checked": len(
                files
            ),
            "passed": not failures,
            "failures": failures,
        }

    def install_requirements(
        self,
        execution_id: str,
        root: pathlib.Path,
    ) -> Dict[str, Any]:
        requirements = (
            root /
            "requirements.txt"
        )

        if not requirements.exists():
            return {
                "status": "NOT_APPLICABLE"
            }

        result = self.runner.run(
            execution_id,
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                str(
                    requirements
                ),
            ],
            cwd=root,
            timeout=DEFAULT_TIMEOUT,
        )

        return {
            "success": result.success,
            "returncode": (
                result.returncode
            ),
            "stdout": result.stdout,
            "stderr": result.stderr,
        }


# =====================================================================
# NODE ENGINE
# =====================================================================

class NodeEngine:
    def __init__(
        self,
        runner: CommandRunner,
    ):
        self.runner = runner

    def install(
        self,
        execution_id: str,
        root: pathlib.Path,
    ) -> Dict[str, Any]:
        package_json = (
            root /
            "package.json"
        )

        if not package_json.exists():
            return {
                "status": "NOT_APPLICABLE"
            }

        if (
            root /
            "package-lock.json"
        ).exists():
            command = [
                "npm",
                "ci",
            ]
        else:
            command = [
                "npm",
                "install",
            ]

        result = self.runner.run(
            execution_id,
            command,
            cwd=root,
            timeout=DEFAULT_TIMEOUT,
        )

        return {
            "success": result.success,
            "returncode": (
                result.returncode
            ),
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    def build(
        self,
        execution_id: str,
        root: pathlib.Path,
    ) -> Dict[str, Any]:
        package_json = (
            root /
            "package.json"
        )

        if not package_json.exists():
            return {
                "status": "NOT_APPLICABLE"
            }

        try:
            package = load_json(
                package_json
            )
        except Exception as exc:
            return {
                "success": False,
                "error": str(
                    exc
                ),
            }

        scripts = package.get(
            "scripts",
            {},
        )

        if "build" not in scripts:
            return {
                "status": "NO_BUILD_SCRIPT"
            }

        result = self.runner.run(
            execution_id,
            [
                "npm",
                "run",
                "build",
            ],
            cwd=root,
            timeout=DEFAULT_TIMEOUT,
        )

        return {
            "success": result.success,
            "returncode": (
                result.returncode
            ),
            "stdout": result.stdout,
            "stderr": result.stderr,
        }


# =====================================================================
# SYSTEMD ENGINE
# =====================================================================

class SystemdEngine:
    SERVICE_PATTERN = re.compile(
        r"^[A-Za-z0-9_.@:-]+\.service$"
    )

    def __init__(
        self,
        runner: CommandRunner,
    ):
        self.runner = runner

    def validate_service(
        self,
        service: str,
    ) -> str:
        if not self.SERVICE_PATTERN.fullmatch(
            service
        ):
            raise ValueError(
                f"Invalid service name: {service}"
            )

        return service

    def daemon_reload(
        self,
        execution_id: str,
    ) -> CommandResult:
        return self.runner.run(
            execution_id,
            [
                "systemctl",
                "daemon-reload",
            ],
        )

    def restart(
        self,
        execution_id: str,
        service: str,
    ) -> Dict[str, Any]:
        service = self.validate_service(
            service
        )

        restart = self.runner.run(
            execution_id,
            [
                "systemctl",
                "restart",
                service,
            ],
        )

        active = self.runner.run(
            execution_id,
            [
                "systemctl",
                "is-active",
                service,
            ],
        )

        enabled = self.runner.run(
            execution_id,
            [
                "systemctl",
                "is-enabled",
                service,
            ],
        )

        return {
            "restart_success": (
                restart.success
            ),
            "active": (
                active.stdout.strip()
                == "active"
            ),
            "enabled": (
                enabled.stdout.strip()
                in {
                    "enabled",
                    "static",
                    "indirect",
                }
            ),
            "note": (
                "systemd state is infrastructure evidence only; "
                "independent end-to-end workflow verification remains required."
            ),
        }

    def enable_now(
        self,
        execution_id: str,
        service: str,
    ) -> Dict[str, Any]:
        service = self.validate_service(
            service
        )

        result = self.runner.run(
            execution_id,
            [
                "systemctl",
                "enable",
                "--now",
                service,
            ],
        )

        state = self.restart(
            execution_id,
            service,
        )

        state[
            "enable_now_success"
        ] = result.success

        return state


# =====================================================================
# NGINX ENGINE
# =====================================================================

class NginxEngine:
    def __init__(
        self,
        runner: CommandRunner,
    ):
        self.runner = runner

    def syntax_check(
        self,
        execution_id: str,
    ) -> Dict[str, Any]:
        if not command_exists(
            "nginx"
        ):
            return {
                "available": False,
                "passed": False,
                "reason": "NGINX_NOT_INSTALLED",
            }

        result = self.runner.run(
            execution_id,
            [
                "nginx",
                "-t",
            ],
        )

        return {
            "available": True,
            "passed": result.success,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    def safe_reload(
        self,
        execution_id: str,
    ) -> Dict[str, Any]:
        check = self.syntax_check(
            execution_id
        )

        if not check.get(
            "passed"
        ):
            raise RuntimeError(
                "Nginx syntax check failed; reload blocked."
            )

        result = self.runner.run(
            execution_id,
            [
                "systemctl",
                "reload",
                "nginx",
            ],
        )

        return {
            "reloaded": result.success,
            "syntax": check,
        }


# =====================================================================
# SQLITE ENGINE
# =====================================================================

class SQLiteEngine:
    def integrity_check(
        self,
        db_path: pathlib.Path,
    ) -> Dict[str, Any]:
        if not db_path.exists():
            return {
                "exists": False,
                "passed": False,
            }

        conn = sqlite3.connect(
            str(db_path),
            timeout=30,
        )

        try:
            row = conn.execute(
                "PRAGMA integrity_check"
            ).fetchone()

            result = (
                row[0]
                if row
                else "UNKNOWN"
            )

            return {
                "exists": True,
                "passed": result == "ok",
                "result": result,
            }

        finally:
            conn.close()

    def backup(
        self,
        source: pathlib.Path,
        destination: pathlib.Path,
    ) -> Dict[str, Any]:
        source = source.resolve()

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        source_conn = sqlite3.connect(
            str(source),
            timeout=30,
        )

        destination_conn = sqlite3.connect(
            str(destination),
            timeout=30,
        )

        try:
            source_conn.backup(
                destination_conn
            )
        finally:
            destination_conn.close()
            source_conn.close()

        return {
            "source": str(
                source
            ),
            "destination": str(
                destination
            ),
            "sha256": sha256_file(
                destination
            ),
        }


# =====================================================================
# NETWORK / HTTP VERIFICATION
# =====================================================================

class NetworkVerifier:
    def tcp_check(
        self,
        host: str,
        port: int,
        timeout: float = 5.0,
    ) -> Dict[str, Any]:
        started = time.monotonic()

        try:
            with socket.create_connection(
                (
                    host,
                    int(
                        port
                    ),
                ),
                timeout=timeout,
            ):
                elapsed = (
                    time.monotonic()
                    - started
                )

                return {
                    "reachable": True,
                    "host": host,
                    "port": port,
                    "duration_seconds": elapsed,
                }

        except Exception as exc:
            return {
                "reachable": False,
                "host": host,
                "port": port,
                "error": str(
                    exc
                ),
            }

    def http_check(
        self,
        url: str,
        timeout: int = 10,
    ) -> Dict[str, Any]:
        parsed = urllib.parse.urlparse(
            url
        )

        if parsed.scheme not in {
            "http",
            "https",
        }:
            raise ValueError(
                "Unsupported URL scheme."
            )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    f"MAJD-Maintenance-Executor/{VERSION}"
                ),
                "Accept": (
                    "application/json,text/html,*/*;q=0.1"
                ),
            },
        )

        started = time.monotonic()

        try:
            with urllib.request.urlopen(
                request,
                timeout=timeout,
            ) as response:
                body = response.read(
                    256 * 1024
                )

                elapsed = (
                    time.monotonic()
                    - started
                )

                return {
                    "reachable": True,
                    "url": url,
                    "status": response.status,
                    "content_length_sampled": len(
                        body
                    ),
                    "body_sha256": sha256_bytes(
                        body
                    ),
                    "duration_seconds": elapsed,
                }

        except urllib.error.HTTPError as exc:
            return {
                "reachable": True,
                "url": url,
                "status": exc.code,
                "http_error": str(
                    exc
                ),
            }

        except Exception as exc:
            return {
                "reachable": False,
                "url": url,
                "error": str(
                    exc
                ),
            }


# =====================================================================
# CONFIG / ENVIRONMENT ENGINE
# =====================================================================

class ConfigurationEngine:
    def discover_env_keys(
        self,
        root: pathlib.Path,
    ) -> Dict[str, List[str]]:
        results: Dict[
            str,
            List[str]
        ] = {}

        for name in (
            ".env",
            ".env.production",
            ".env.local",
            ".env.example",
        ):
            path = (
                root /
                name
            )

            if not path.exists():
                continue

            keys = []

            try:
                for line in path.read_text(
                    encoding="utf-8",
                    errors="replace",
                ).splitlines():
                    line = line.strip()

                    if not line:
                        continue

                    if line.startswith(
                        "#"
                    ):
                        continue

                    if "=" not in line:
                        continue

                    key = line.split(
                        "=",
                        1,
                    )[0].strip()

                    if re.fullmatch(
                        r"[A-Za-z_][A-Za-z0-9_]*",
                        key,
                    ):
                        keys.append(
                            key
                        )

            except PermissionError:
                continue

            results[
                name
            ] = sorted(
                set(
                    keys
                )
            )

        return results


# =====================================================================
# SECRET PRESENCE CHECK
# =====================================================================

class SecretRequirementsEngine:
    """
    Does NOT read or expose secret values.
    Only determines whether named environment variables exist.
    """

    def check_environment(
        self,
        required_keys: Sequence[
            str
        ],
    ) -> Dict[str, Any]:
        missing = []
        present = []

        for key in required_keys:
            if os.environ.get(
                key
            ):
                present.append(
                    key
                )
            else:
                missing.append(
                    key
                )

        return {
            "required": list(
                required_keys
            ),
            "present": present,
            "missing": missing,
            "ready": not missing,
        }


# =====================================================================
# MAJD-GIT BRIDGE
# =====================================================================

class MajdGitBridge:
    """
    Internal repository integration.

    The executor can work with the locally mounted MAJD-GIT managed
    repository area without assuming external GitHub is permanent.
    """

    def __init__(
        self,
        runner: CommandRunner,
    ):
        self.runner = runner

        self.root = pathlib.Path(
            os.environ.get(
                "MAJD_GIT_ROOT",
                "/root/MAJD-GIT",
            )
        )

        self.managed = (
            self.root /
            "managed"
        )

    def available(
        self,
    ) -> bool:
        return (
            self.root.exists()
            and self.root.is_dir()
        )

    def inventory(
        self,
    ) -> Dict[str, Any]:
        if not self.available():
            return {
                "available": False
            }

        repos = []

        if self.managed.exists():
            for child in sorted(
                self.managed.iterdir(),
                key=lambda p: p.name,
            ):
                if child.is_dir():
                    repos.append(
                        {
                            "name": child.name,
                            "path": str(
                                child
                            ),
                            "git": (
                                child /
                                ".git"
                            ).exists(),
                        }
                    )

        return {
            "available": True,
            "root": str(
                self.root
            ),
            "managed_repositories": repos,
        }


# =====================================================================
# MAJD-IN / N8N BRIDGE
# =====================================================================

class MajdInBridge:
    def __init__(
        self,
        runner: CommandRunner,
    ):
        self.runner = runner

        self.root = pathlib.Path(
            os.environ.get(
                "MAJD_IN_ROOT",
                "/root/MAJD-IN",
            )
        )

        self.n8n_base_url = os.environ.get(
            "MAJD_N8N_BASE_URL",
            "http://127.0.0.1:5678",
        )

    def available(
        self,
    ) -> bool:
        return self.root.exists()

    def status(
        self,
    ) -> Dict[str, Any]:
        return {
            "project_root_exists": self.root.exists(),
            "project_root": str(
                self.root
            ),
            "n8n_base_url": self.n8n_base_url,
            "credential_values_exposed": False,
        }


# =====================================================================
# PAYMENT / EMAIL / EXTERNAL ADAPTER READINESS
# =====================================================================

class ExternalIntegrationReadiness:
    def __init__(
        self,
        secrets: SecretRequirementsEngine,
    ):
        self.secrets = secrets

    def moyasar(
        self,
    ) -> Dict[str, Any]:
        result = self.secrets.check_environment(
            [
                "MOYASAR_SECRET_KEY",
            ]
        )

        result[
            "provider"
        ] = "MOYASAR"

        result[
            "rule"
        ] = (
            "Secret key must remain backend-only. "
            "No live-payment capability is claimed without real provider verification."
        )

        return result

    def smtp(
        self,
    ) -> Dict[str, Any]:
        result = self.secrets.check_environment(
            [
                "SMTP_HOST",
                "SMTP_USERNAME",
                "SMTP_PASSWORD",
            ]
        )

        result[
            "provider"
        ] = "SMTP"

        result[
            "rule"
        ] = (
            "Real send/receive verification remains required before "
            "email is considered operational."
        )

        return result

    def generic_api(
        self,
        required_env: Sequence[
            str
        ],
    ) -> Dict[str, Any]:
        return self.secrets.check_environment(
            required_env
        )


# =====================================================================
# LOCAL TECHNICAL VERIFIER
# =====================================================================

class LocalTechnicalVerifier:
    """
    Performs technical checks after execution.

    IMPORTANT:
    This is NOT the independent verifier of file 03.
    """

    def __init__(
        self,
        runner: CommandRunner,
        python_engine: PythonEngine,
        node_engine: NodeEngine,
        git_engine: GitEngine,
    ):
        self.runner = runner
        self.python = python_engine
        self.node = node_engine
        self.git = git_engine

    def verify_platform(
        self,
        execution_id: str,
        root: pathlib.Path,
    ) -> Dict[str, Any]:
        checks: Dict[
            str,
            Any
        ] = {
            "captured_at": utc_now(),
            "root_exists": root.exists(),
            "python": None,
            "node_build": None,
            "git_diff_check": None,
        }

        if not root.exists():
            checks[
                "passed"
            ] = False

            return checks

        if any(
            (
                root /
                name
            ).exists()
            for name in (
                "requirements.txt",
                "pyproject.toml",
            )
        ):
            checks[
                "python"
            ] = self.python.syntax_check(
                execution_id,
                root,
            )

        if (
            root /
            "package.json"
        ).exists():
            checks[
                "node_build"
            ] = self.node.build(
                execution_id,
                root,
            )

        if (
            root /
            ".git"
        ).exists():
            result = self.git.diff_check(
                execution_id,
                root,
            )

            checks[
                "git_diff_check"
            ] = {
                "passed": result.success,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        passed = True

        python_result = checks.get(
            "python"
        )

        if isinstance(
            python_result,
            dict,
        ):
            if not python_result.get(
                "passed",
                False,
            ):
                passed = False

        node_result = checks.get(
            "node_build"
        )

        if isinstance(
            node_result,
            dict,
        ):
            if (
                "success"
                in node_result
                and not node_result[
                    "success"
                ]
            ):
                passed = False

        git_result = checks.get(
            "git_diff_check"
        )

        if isinstance(
            git_result,
            dict,
        ):
            if not git_result.get(
                "passed",
                False,
            ):
                passed = False

        checks[
            "passed"
        ] = passed

        checks[
            "independent_verification"
        ] = False

        checks[
            "independent_verifier"
        ] = (
            "MAJD-MAINTENANCE-RUNTIME-03.py"
        )

        return checks


# =====================================================================
# GENERIC CODE MODIFICATION ENGINE
# =====================================================================

class CodeModificationEngine:
    """
    Applies explicit file operations that already exist in an approved
    execution request.

    It does not accept arbitrary instructions scraped from external web
    content.
    """

    def write_file(
        self,
        root: pathlib.Path,
        relative_path: str,
        content: str,
        executable: bool = False,
    ) -> Dict[str, Any]:
        if not relative_path:
            raise ValueError(
                "Empty relative_path."
            )

        destination = (
            root /
            relative_path
        ).resolve()

        if not path_within(
            destination,
            root,
        ):
            raise PermissionError(
                "File operation escaped platform root."
            )

        previous_hash = None

        if destination.exists():
            previous_hash = sha256_file(
                destination
            )

        mode = (
            0o755
            if executable
            else 0o644
        )

        atomic_write_text(
            destination,
            content,
            mode=mode,
        )

        return {
            "path": str(
                destination
            ),
            "previous_hash": previous_hash,
            "new_hash": sha256_file(
                destination
            ),
            "bytes": destination.stat().st_size,
        }

    def delete_file(
        self,
        root: pathlib.Path,
        relative_path: str,
    ) -> Dict[str, Any]:
        destination = (
            root /
            relative_path
        ).resolve()

        if not path_within(
            destination,
            root,
        ):
            raise PermissionError(
                "Delete escaped platform root."
            )

        if not destination.exists():
            return {
                "deleted": False,
                "reason": "NOT_FOUND",
            }

        if not destination.is_file():
            raise PermissionError(
                "Only explicit files may be deleted by this method."
            )

        digest = sha256_file(
            destination
        )

        destination.unlink()

        return {
            "deleted": True,
            "path": str(
                destination
            ),
            "sha256_before_delete": digest,
        }


# =====================================================================
# EXECUTION ACTION ROUTER
# =====================================================================

class ActionRouter:
    def __init__(
        self,
        db: ExecutorDatabase,
        master: MasterDatabaseBridge,
        runner: CommandRunner,
        backup: BackupEngine,
        evidence: EvidenceEngine,
    ):
        self.db = db
        self.master = master
        self.runner = runner
        self.backup = backup
        self.evidence = evidence

        self.inspector = PlatformInspector()

        self.git = GitEngine(
            runner
        )

        self.python = PythonEngine(
            runner
        )

        self.node = NodeEngine(
            runner
        )

        self.systemd = SystemdEngine(
            runner
        )

        self.nginx = NginxEngine(
            runner
        )

        self.sqlite = SQLiteEngine()

        self.network = NetworkVerifier()

        self.config = ConfigurationEngine()

        self.secrets = SecretRequirementsEngine()

        self.integrations = ExternalIntegrationReadiness(
            self.secrets
        )

        self.majd_git = MajdGitBridge(
            runner
        )

        self.majd_in = MajdInBridge(
            runner
        )

        self.code = CodeModificationEngine()

        self.local_verifier = LocalTechnicalVerifier(
            runner,
            self.python,
            self.node,
            self.git,
        )

    def platform_path(
        self,
        platform_id: Optional[
            str
        ],
    ) -> Optional[
        pathlib.Path
    ]:
        if not platform_id:
            return None

        row = self.master.get_platform(
            platform_id
        )

        return validate_platform_path(
            pathlib.Path(
                row["root_path"]
            )
        )

    def execute(
        self,
        execution_id: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        action = str(
            payload[
                "action"
            ]
        ).upper()

        platform_id = payload.get(
            "platform_id"
        )

        scope = payload.get(
            "scope"
        ) or {}

        root = self.platform_path(
            platform_id
        )

        if action == "ASSESS_AND_REMEDIATE":
            return self.assess_and_remediate(
                execution_id,
                payload,
                root,
            )

        if action == "WRITE_FILE":
            return self.write_file(
                execution_id,
                payload,
                root,
                scope,
            )

        if action == "PYTHON_DEPENDENCIES":
            return self.python_dependencies(
                execution_id,
                root,
            )

        if action == "NODE_DEPENDENCIES":
            return self.node_dependencies(
                execution_id,
                root,
            )

        if action == "RESTART_SERVICE":
            return self.restart_service(
                execution_id,
                scope,
            )

        if action == "ENABLE_SERVICE":
            return self.enable_service(
                execution_id,
                scope,
            )

        if action == "NGINX_RELOAD":
            return self.nginx_reload(
                execution_id
            )

        if action == "VERIFY_HTTP":
            return self.verify_http(
                scope
            )

        if action == "VERIFY_TCP":
            return self.verify_tcp(
                scope
            )

        if action == "COMMIT_PLATFORM":
            return self.commit_platform(
                execution_id,
                root,
                scope,
            )

        if action == "SQLITE_INTEGRITY":
            return self.sqlite_integrity(
                root,
                scope,
            )

        if action == "MAJD_GIT_INVENTORY":
            return self.majd_git.inventory()

        if action == "MAJD_IN_STATUS":
            return self.majd_in.status()

        if action == "MOYASAR_READINESS":
            return self.integrations.moyasar()

        if action == "SMTP_READINESS":
            return self.integrations.smtp()

        raise ValueError(
            f"Unsupported action: {action}"
        )

    # -----------------------------------------------------------------
    # ASSESS + REMEDIATE
    # -----------------------------------------------------------------

    def assess_and_remediate(
        self,
        execution_id: str,
        payload: Dict[str, Any],
        root: Optional[
            pathlib.Path
        ],
    ) -> Dict[str, Any]:
        if root is None:
            raise ValueError(
                "ASSESS_AND_REMEDIATE requires platform_id."
            )

        before = self.inspector.inspect(
            root
        )

        remediation: Dict[
            str,
            Any
        ] = {
            "dependencies": [],
            "repairs": [],
        }

        if (
            root /
            "requirements.txt"
        ).exists():
            py_install = self.python.install_requirements(
                execution_id,
                root,
            )

            remediation[
                "dependencies"
            ].append(
                {
                    "type": "PYTHON",
                    "result": py_install,
                }
            )

        if (
            root /
            "package.json"
        ).exists():
            node_install = self.node.install(
                execution_id,
                root,
            )

            remediation[
                "dependencies"
            ].append(
                {
                    "type": "NODE",
                    "result": node_install,
                }
            )

        checks = self.local_verifier.verify_platform(
            execution_id,
            root,
        )

        after = self.inspector.inspect(
            root
        )

        changed = False

        if (
            root /
            ".git"
        ).exists():
            status = self.git.status(
                execution_id,
                root,
            )

            changed = bool(
                status.stdout.strip()
            )

        return {
            "before": before,
            "remediation": remediation,
            "local_verification": checks,
            "after": after,
            "changed": changed,
            "truth": (
                "EXECUTED_LOCALLY_PENDING_INDEPENDENT_VERIFICATION"
            ),
        }

    # -----------------------------------------------------------------
    # WRITE FILE
    # -----------------------------------------------------------------

    def write_file(
        self,
        execution_id: str,
        payload: Dict[str, Any],
        root: Optional[
            pathlib.Path
        ],
        scope: Dict[str, Any],
    ) -> Dict[str, Any]:
        if root is None:
            raise ValueError(
                "WRITE_FILE requires platform_id."
            )

        relative_path = scope.get(
            "relative_path"
        )

        content = scope.get(
            "content"
        )

        if not isinstance(
            relative_path,
            str,
        ):
            raise ValueError(
                "Missing relative_path."
            )

        if not isinstance(
            content,
            str,
        ):
            raise ValueError(
                "Missing content."
            )

        target = (
            root /
            relative_path
        )

        backup = None

        if target.exists():
            backup = self.backup.backup_path(
                payload[
                    "request_id"
                ],
                target,
            )

        result = self.code.write_file(
            root,
            relative_path,
            content,
            executable=bool(
                scope.get(
                    "executable",
                    False,
                )
            ),
        )

        local_checks = self.local_verifier.verify_platform(
            execution_id,
            root,
        )

        return {
            "write": result,
            "backup": (
                dataclasses.asdict(
                    backup
                )
                if backup
                else None
            ),
            "local_verification": local_checks,
            "changed": True,
        }

    # -----------------------------------------------------------------
    # DEPENDENCIES
    # -----------------------------------------------------------------

    def python_dependencies(
        self,
        execution_id: str,
        root: Optional[
            pathlib.Path
        ],
    ) -> Dict[str, Any]:
        if root is None:
            raise ValueError(
                "Platform required."
            )

        return self.python.install_requirements(
            execution_id,
            root,
        )

    def node_dependencies(
        self,
        execution_id: str,
        root: Optional[
            pathlib.Path
        ],
    ) -> Dict[str, Any]:
        if root is None:
            raise ValueError(
                "Platform required."
            )

        return self.node.install(
            execution_id,
            root,
        )

    # -----------------------------------------------------------------
    # SYSTEMD
    # -----------------------------------------------------------------

    def restart_service(
        self,
        execution_id: str,
        scope: Dict[str, Any],
    ) -> Dict[str, Any]:
        service = scope.get(
            "service"
        )

        if not isinstance(
            service,
            str,
        ):
            raise ValueError(
                "Missing service."
            )

        return self.systemd.restart(
            execution_id,
            service,
        )

    def enable_service(
        self,
        execution_id: str,
        scope: Dict[str, Any],
    ) -> Dict[str, Any]:
        service = scope.get(
            "service"
        )

        if not isinstance(
            service,
            str,
        ):
            raise ValueError(
                "Missing service."
            )

        return self.systemd.enable_now(
            execution_id,
            service,
        )

    # -----------------------------------------------------------------
    # NGINX
    # -----------------------------------------------------------------

    def nginx_reload(
        self,
        execution_id: str,
    ) -> Dict[str, Any]:
        return self.nginx.safe_reload(
            execution_id
        )

    # -----------------------------------------------------------------
    # HTTP/TCP
    # -----------------------------------------------------------------

    def verify_http(
        self,
        scope: Dict[str, Any],
    ) -> Dict[str, Any]:
        url = scope.get(
            "url"
        )

        if not isinstance(
            url,
            str,
        ):
            raise ValueError(
                "Missing url."
            )

        return self.network.http_check(
            url
        )

    def verify_tcp(
        self,
        scope: Dict[str, Any],
    ) -> Dict[str, Any]:
        host = scope.get(
            "host"
        )

        port = scope.get(
            "port"
        )

        if not isinstance(
            host,
            str,
        ):
            raise ValueError(
                "Missing host."
            )

        if not isinstance(
            port,
            int,
        ):
            raise ValueError(
                "Missing integer port."
            )

        return self.network.tcp_check(
            host,
            port,
        )

    # -----------------------------------------------------------------
    # GIT COMMIT
    # -----------------------------------------------------------------

    def commit_platform(
        self,
        execution_id: str,
        root: Optional[
            pathlib.Path
        ],
        scope: Dict[str, Any],
    ) -> Dict[str, Any]:
        if root is None:
            raise ValueError(
                "Platform required."
            )

        if not self.git.is_repo(
            root
        ):
            raise RuntimeError(
                "Platform is not a Git repository."
            )

        message = scope.get(
            "message"
        ) or (
            "MAJD autonomous maintenance update"
        )

        return self.git.commit_all(
            execution_id,
            root,
            str(
                message
            ),
        )

    # -----------------------------------------------------------------
    # SQLITE
    # -----------------------------------------------------------------

    def sqlite_integrity(
        self,
        root: Optional[
            pathlib.Path
        ],
        scope: Dict[str, Any],
    ) -> Dict[str, Any]:
        if root is None:
            raise ValueError(
                "Platform required."
            )

        relative = scope.get(
            "relative_path"
        )

        if not isinstance(
            relative,
            str,
        ):
            raise ValueError(
                "Missing relative_path."
            )

        path = (
            root /
            relative
        ).resolve()

        if not path_within(
            path,
            root,
        ):
            raise PermissionError(
                "Database path escaped platform root."
            )

        return self.sqlite.integrity_check(
            path
        )


# =====================================================================
# MAIN EXECUTOR
# =====================================================================

class MajdMaintenanceExecutor:
    def __init__(
        self,
    ):
        self.db = ExecutorDatabase(
            EXECUTOR_DB_PATH
        )

        self.master = MasterDatabaseBridge(
            MASTER_DB_PATH
        )

        self.runner = CommandRunner(
            self.db
        )

        self.validator = ExecutionRequestValidator()

        self.backup = BackupEngine(
            self.db,
            self.runner,
        )

        self.evidence = EvidenceEngine(
            self.db
        )

        self.router = ActionRouter(
            self.db,
            self.master,
            self.runner,
            self.backup,
            self.evidence,
        )

    # -----------------------------------------------------------------
    # BOOTSTRAP
    # -----------------------------------------------------------------

    def bootstrap(
        self,
    ) -> Dict[str, Any]:
        capability = {
            "app": APP_NAME,
            "file": FILE_NAME,
            "version": VERSION,
            "authority": SUPREME_AUTHORITY,
            "capabilities": {
                "EXECUTION_REQUEST_VALIDATION": True,
                "FILESYSTEM_EXECUTION": True,
                "CODE_WRITING": True,
                "PYTHON_DEPENDENCIES": True,
                "NODE_DEPENDENCIES": True,
                "PYTHON_SYNTAX_VERIFICATION": True,
                "NODE_BUILD_VERIFICATION": True,
                "GIT_EXECUTION": True,
                "SYSTEMD_EXECUTION": command_exists(
                    "systemctl"
                ),
                "NGINX_EXECUTION": command_exists(
                    "nginx"
                ),
                "SQLITE_EXECUTION": True,
                "MAJD_GIT_BRIDGE": (
                    self.router.majd_git.available()
                ),
                "MAJD_IN_BRIDGE": (
                    self.router.majd_in.available()
                ),
                "BACKUP": True,
                "ROLLBACK_METADATA": True,
                "LOCAL_TECHNICAL_VERIFICATION": True,
                "INDEPENDENT_VERIFICATION": False,
                "CONTINUOUS_RUNTIME": False,
                "SOVEREIGN_CYBER_DEFENSE": False,
            },
            "truth": {
                "executor_operational": True,
                "file_03_required_for_independent_verification": True,
                "file_04_required_for_continuous_cyber_defense": True,
            },
            "timestamp": utc_now(),
        }

        atomic_write_json(
            STATE_DIR /
            "executor-02-capabilities.json",
            capability,
        )

        self.db.audit(
            "BOOTSTRAP",
            APP_NAME,
            capability,
        )

        return capability

    # -----------------------------------------------------------------
    # PLATFORM BACKUP
    # -----------------------------------------------------------------

    def prepare_backup(
        self,
        execution_id: str,
        payload: Dict[str, Any],
    ) -> Tuple[
        List[BackupRecord],
        Optional[Dict[str, Any]],
    ]:
        platform_id = payload.get(
            "platform_id"
        )

        if not platform_id:
            return (
                [],
                None,
            )

        row = self.master.get_platform(
            platform_id
        )

        root = validate_platform_path(
            pathlib.Path(
                row["root_path"]
            )
        )

        backups: List[
            BackupRecord
        ] = []

        if payload.get(
            "backup_required",
            True,
        ):
            backup = self.backup.backup_path(
                payload[
                    "request_id"
                ],
                root,
            )

            backups.append(
                backup
            )

        rollback = self.backup.create_git_rollback_point(
            execution_id,
            payload[
                "request_id"
            ],
            root,
        )

        return (
            backups,
            rollback,
        )

    # -----------------------------------------------------------------
    # PROCESS REQUEST
    # -----------------------------------------------------------------

    def process_request_file(
        self,
        request_path: pathlib.Path,
    ) -> ExecutionResult:
        request_path = request_path.resolve()

        if not path_within(
            request_path,
            REQUEST_DIR,
        ):
            raise PermissionError(
                "Request file outside execution request directory."
            )

        envelope = load_json(
            request_path
        )

        payload = self.validator.validate(
            envelope
        )

        request_id = str(
            payload[
                "request_id"
            ]
        )

        action = str(
            payload[
                "action"
            ]
        )

        platform_id = payload.get(
            "platform_id"
        )

        execution_id = str(
            uuid.uuid4()
        )

        started_at = utc_now()

        result = ExecutionResult(
            request_id=request_id,
            action=action,
            platform_id=platform_id,
            status=ExecutionStatus.VALIDATING.value,
            changed=False,
            local_checks_passed=False,
            independent_verification_required=bool(
                payload.get(
                    "independent_verification_required",
                    True,
                )
            ),
            started_at=started_at,
        )

        with RequestLock(
            request_id
        ):
            self.db.conn.execute(
                """
                INSERT INTO executions(
                    execution_id,
                    request_id,
                    platform_id,
                    action,
                    status,
                    changed,
                    local_checks_passed,
                    independent_verification_required,
                    started_at
                )
                VALUES (?, ?, ?, ?, ?, 0, 0, ?, ?)
                """,
                (
                    execution_id,
                    request_id,
                    platform_id,
                    action,
                    ExecutionStatus.VALIDATING.value,
                    int(
                        result.independent_verification_required
                    ),
                    started_at,
                ),
            )

            self.db.conn.commit()

            try:
                self.master.update_request_status(
                    request_id,
                    ExecutionStatus.VALIDATING.value,
                )

                self.db.audit(
                    "REQUEST_VALIDATED",
                    request_id,
                    {
                        "action": action,
                        "platform_id": platform_id,
                    },
                )

                # -----------------------------------------------------
                # BACKUP
                # -----------------------------------------------------

                self._set_execution_status(
                    execution_id,
                    ExecutionStatus.BACKING_UP.value,
                )

                self.master.update_request_status(
                    request_id,
                    ExecutionStatus.BACKING_UP.value,
                )

                backups, rollback = self.prepare_backup(
                    execution_id,
                    payload,
                )

                result.backup_ids = [
                    x.backup_id
                    for x in backups
                ]

                if rollback:
                    result.messages.append(
                        "Git rollback point created."
                    )

                # -----------------------------------------------------
                # EXECUTE
                # -----------------------------------------------------

                self._set_execution_status(
                    execution_id,
                    ExecutionStatus.EXECUTING.value,
                )

                self.master.update_request_status(
                    request_id,
                    ExecutionStatus.EXECUTING.value,
                )

                action_result = self.router.execute(
                    execution_id,
                    payload,
                )

                changed = bool(
                    action_result.get(
                        "changed",
                        False,
                    )
                )

                result.changed = changed

                # -----------------------------------------------------
                # LOCAL VERIFY
                # -----------------------------------------------------

                self._set_execution_status(
                    execution_id,
                    ExecutionStatus.LOCAL_VERIFYING.value,
                )

                self.master.update_request_status(
                    request_id,
                    ExecutionStatus.LOCAL_VERIFYING.value,
                )

                local_checks_passed = self._derive_local_check_state(
                    action_result
                )

                result.local_checks_passed = (
                    local_checks_passed
                )

                evidence_id = self.evidence.write(
                    request_id=request_id,
                    evidence_type=(
                        "EXECUTION_RESULT"
                    ),
                    target=(
                        platform_id
                        or action
                    ),
                    payload={
                        "execution_id": execution_id,
                        "action_result": action_result,
                        "backups": [
                            dataclasses.asdict(
                                x
                            )
                            for x in backups
                        ],
                        "rollback": rollback,
                        "local_checks_passed": (
                            local_checks_passed
                        ),
                        "independent_verification": False,
                    },
                )

                result.evidence_ids.append(
                    evidence_id
                )

                if not local_checks_passed:
                    raise RuntimeError(
                        "Execution completed but local technical verification failed."
                    )

                # -----------------------------------------------------
                # PENDING INDEPENDENT VERIFIER
                # -----------------------------------------------------

                result.status = (
                    ExecutionStatus
                    .EXECUTED_PENDING_INDEPENDENT_VERIFICATION
                    .value
                )

                result.messages.append(
                    "Real execution completed."
                )

                result.messages.append(
                    "Independent verification by file 03 is still required."
                )

                result.completed_at = utc_now()

                self.db.conn.execute(
                    """
                    UPDATE executions
                    SET status=?,
                        changed=?,
                        local_checks_passed=?,
                        completed_at=?
                    WHERE execution_id=?
                    """,
                    (
                        result.status,
                        int(
                            result.changed
                        ),
                        int(
                            result.local_checks_passed
                        ),
                        result.completed_at,
                        execution_id,
                    ),
                )

                self.db.conn.commit()

                self.master.update_request_status(
                    request_id,
                    result.status,
                )

                destination = (
                    PROCESSED_DIR /
                    request_path.name
                )

                os.replace(
                    request_path,
                    destination,
                )

                self.db.audit(
                    "EXECUTION_COMPLETED",
                    request_id,
                    dataclasses.asdict(
                        result
                    ),
                )

                return result

            except Exception as exc:
                LOG.exception(
                    "EXECUTION_FAILED | request=%s | %s",
                    request_id,
                    exc,
                )

                result.status = (
                    ExecutionStatus.FAILED.value
                )

                result.completed_at = utc_now()

                result.messages.append(
                    str(
                        exc
                    )
                )

                self.db.conn.execute(
                    """
                    UPDATE executions
                    SET status=?,
                        changed=?,
                        local_checks_passed=?,
                        completed_at=?,
                        error=?
                    WHERE execution_id=?
                    """,
                    (
                        result.status,
                        int(
                            result.changed
                        ),
                        int(
                            result.local_checks_passed
                        ),
                        result.completed_at,
                        str(
                            exc
                        ),
                        execution_id,
                    ),
                )

                self.db.conn.commit()

                with contextlib.suppress(
                    Exception
                ):
                    self.master.update_request_status(
                        request_id,
                        result.status,
                    )

                failure_evidence = self.evidence.write(
                    request_id=request_id,
                    evidence_type="EXECUTION_FAILURE",
                    target=(
                        platform_id
                        or action
                    ),
                    payload={
                        "execution_id": execution_id,
                        "error_type": type(
                            exc
                        ).__name__,
                        "error": str(
                            exc
                        ),
                        "traceback": traceback.format_exc(),
                    },
                )

                result.evidence_ids.append(
                    failure_evidence
                )

                if request_path.exists():
                    destination = (
                        FAILED_DIR /
                        request_path.name
                    )

                    os.replace(
                        request_path,
                        destination,
                    )

                self.db.audit(
                    "EXECUTION_FAILED",
                    request_id,
                    {
                        "error": str(
                            exc
                        ),
                    },
                )

                return result

    def _derive_local_check_state(
        self,
        action_result: Dict[str, Any],
    ) -> bool:
        if "local_verification" in action_result:
            verification = action_result[
                "local_verification"
            ]

            if isinstance(
                verification,
                dict,
            ):
                return bool(
                    verification.get(
                        "passed",
                        False,
                    )
                )

        if "success" in action_result:
            return bool(
                action_result[
                    "success"
                ]
            )

        if "passed" in action_result:
            return bool(
                action_result[
                    "passed"
                ]
            )

        if "reachable" in action_result:
            return bool(
                action_result[
                    "reachable"
                ]
            )

        if "restart_success" in action_result:
            return bool(
                action_result[
                    "restart_success"
                ]
            )

        if "reloaded" in action_result:
            return bool(
                action_result[
                    "reloaded"
                ]
            )

        if "changed" in action_result:
            return True

        if action_result.get(
            "available"
        ) is False:
            return False

        return True

    def _set_execution_status(
        self,
        execution_id: str,
        status: str,
    ) -> None:
        self.db.conn.execute(
            """
            UPDATE executions
            SET status=?
            WHERE execution_id=?
            """,
            (
                status,
                execution_id,
            ),
        )

        self.db.conn.commit()

    # -----------------------------------------------------------------
    # PROCESS ALL
    # -----------------------------------------------------------------

    def process_pending(
        self,
        limit: Optional[
            int
        ] = None,
    ) -> List[
        ExecutionResult
    ]:
        files = sorted(
            REQUEST_DIR.glob(
                "*.json"
            ),
            key=lambda p: p.stat().st_mtime,
        )

        if limit is not None:
            files = files[
                :limit
            ]

        results = []

        for request_path in files:
            try:
                results.append(
                    self.process_request_file(
                        request_path
                    )
                )

            except Exception as exc:
                LOG.exception(
                    "REQUEST_FILE_FAILED | %s | %s",
                    request_path,
                    exc,
                )

        return results

    # -----------------------------------------------------------------
    # STATUS
    # -----------------------------------------------------------------

    def status(
        self,
    ) -> Dict[str, Any]:
        pending = len(
            list(
                REQUEST_DIR.glob(
                    "*.json"
                )
            )
        )

        failed = len(
            list(
                FAILED_DIR.glob(
                    "*.json"
                )
            )
        )

        processed = len(
            list(
                PROCESSED_DIR.glob(
                    "*.json"
                )
            )
        )

        execution_count = self.db.conn.execute(
            """
            SELECT COUNT(*) AS n
            FROM executions
            """
        ).fetchone()[
            "n"
        ]

        backup_count = self.db.conn.execute(
            """
            SELECT COUNT(*) AS n
            FROM backups
            """
        ).fetchone()[
            "n"
        ]

        return {
            "app": APP_NAME,
            "file": FILE_NAME,
            "version": VERSION,
            "authority": SUPREME_AUTHORITY,
            "pending_requests": pending,
            "processed_requests": processed,
            "failed_requests": failed,
            "executions": execution_count,
            "backups": backup_count,
            "majd_git": (
                self.router.majd_git.inventory()
            ),
            "majd_in": (
                self.router.majd_in.status()
            ),
            "truth": {
                "executor_available": True,
                "local_execution_supported": True,
                "independent_verifier_03_available": False,
                "continuous_runtime_03_available": False,
                "cyber_defense_04_available": False,
            },
            "timestamp": utc_now(),
        }


# =====================================================================
# CLI
# =====================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=FILE_NAME,
        description=(
            "MAJD Sovereign Real Execution Engine"
        ),
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    sub.add_parser(
        "bootstrap",
        help="Initialize executor state.",
    )

    sub.add_parser(
        "status",
        help="Show truthful executor status.",
    )

    process_one = sub.add_parser(
        "process",
        help="Process one execution request JSON file.",
    )

    process_one.add_argument(
        "request_file",
    )

    process_all = sub.add_parser(
        "process-pending",
        help="Process pending execution requests.",
    )

    process_all.add_argument(
        "--limit",
        type=int,
        default=None,
    )

    inspect_parser = sub.add_parser(
        "inspect-platform",
        help="Inspect a platform by platform_id.",
    )

    inspect_parser.add_argument(
        "platform_id",
    )

    http_parser = sub.add_parser(
        "http-check",
        help="Perform a real HTTP reachability check.",
    )

    http_parser.add_argument(
        "url",
    )

    tcp_parser = sub.add_parser(
        "tcp-check",
        help="Perform a real TCP reachability check.",
    )

    tcp_parser.add_argument(
        "host",
    )

    tcp_parser.add_argument(
        "port",
        type=int,
    )

    service_parser = sub.add_parser(
        "service-status",
        help="Read real systemd service state.",
    )

    service_parser.add_argument(
        "service",
    )

    sub.add_parser(
        "nginx-check",
        help="Run real nginx -t.",
    )

    sub.add_parser(
        "majd-git",
        help="Show MAJD-GIT internal inventory.",
    )

    sub.add_parser(
        "majd-in",
        help="Show MAJD-IN/n8n bridge status.",
    )

    return parser


# =====================================================================
# DIRECT CLI HELPERS
# =====================================================================

def direct_service_status(
    executor: MajdMaintenanceExecutor,
    service: str,
) -> Dict[str, Any]:
    service = executor.router.systemd.validate_service(
        service
    )

    execution_id = str(
        uuid.uuid4()
    )

    active = executor.runner.run(
        execution_id,
        [
            "systemctl",
            "is-active",
            service,
        ],
    )

    enabled = executor.runner.run(
        execution_id,
        [
            "systemctl",
            "is-enabled",
            service,
        ],
    )

    return {
        "service": service,
        "active": (
            active.stdout.strip()
        ),
        "enabled": (
            enabled.stdout.strip()
        ),
        "truth": (
            "systemd state only; end-to-end service workflow "
            "verification is still required."
        ),
    }


# =====================================================================
# MAIN
# =====================================================================

def main() -> int:
    parser = build_parser()

    args = parser.parse_args()

    executor = MajdMaintenanceExecutor()

    try:
        if args.command == "bootstrap":
            print(
                json_dumps(
                    executor.bootstrap()
                )
            )

            return 0

        if args.command == "status":
            print(
                json_dumps(
                    executor.status()
                )
            )

            return 0

        if args.command == "process":
            request_file = pathlib.Path(
                args.request_file
            )

            if not request_file.is_absolute():
                request_file = (
                    REQUEST_DIR /
                    request_file
                )

            result = executor.process_request_file(
                request_file
            )

            print(
                json_dumps(
                    dataclasses.asdict(
                        result
                    )
                )
            )

            return (
                0
                if result.status
                == ExecutionStatus
                .EXECUTED_PENDING_INDEPENDENT_VERIFICATION
                .value
                else 1
            )

        if args.command == "process-pending":
            results = executor.process_pending(
                limit=args.limit
            )

            payload = [
                dataclasses.asdict(
                    result
                )
                for result in results
            ]

            print(
                json_dumps(
                    payload
                )
            )

            failed = any(
                result.status
                == ExecutionStatus.FAILED.value
                for result in results
            )

            return (
                1
                if failed
                else 0
            )

        if args.command == "inspect-platform":
            row = executor.master.get_platform(
                args.platform_id
            )

            path = validate_platform_path(
                pathlib.Path(
                    row[
                        "root_path"
                    ]
                )
            )

            print(
                json_dumps(
                    executor.router.inspector.inspect(
                        path
                    )
                )
            )

            return 0

        if args.command == "http-check":
            print(
                json_dumps(
                    executor.router.network.http_check(
                        args.url
                    )
                )
            )

            return 0

        if args.command == "tcp-check":
            print(
                json_dumps(
                    executor.router.network.tcp_check(
                        args.host,
                        args.port,
                    )
                )
            )

            return 0

        if args.command == "service-status":
            print(
                json_dumps(
                    direct_service_status(
                        executor,
                        args.service,
                    )
                )
            )

            return 0

        if args.command == "nginx-check":
            execution_id = str(
                uuid.uuid4()
            )

            print(
                json_dumps(
                    executor.router.nginx.syntax_check(
                        execution_id
                    )
                )
            )

            return 0

        if args.command == "majd-git":
            print(
                json_dumps(
                    executor.router.majd_git.inventory()
                )
            )

            return 0

        if args.command == "majd-in":
            print(
                json_dumps(
                    executor.router.majd_in.status()
                )
            )

            return 0

        parser.error(
            "Unknown command."
        )

        return 2

    except KeyboardInterrupt:
        LOG.warning(
            "MAJD_EXECUTOR_INTERRUPTED"
        )

        return 130

    except Exception as exc:
        LOG.exception(
            "MAJD_EXECUTOR_FATAL_ERROR | %s",
            exc,
        )

        print(
            json_dumps(
                {
                    "status": "FAILED",
                    "error_type": type(
                        exc
                    ).__name__,
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

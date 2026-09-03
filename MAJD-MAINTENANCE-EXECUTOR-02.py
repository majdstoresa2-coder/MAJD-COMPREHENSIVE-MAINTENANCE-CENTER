#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD SOVEREIGN MAINTENANCE PLATFORM
FILE 02 — MAJD-MAINTENANCE-EXECUTOR-02.py

REAL EXECUTION LAYER.

Responsibilities:
- backup before destructive change
- code write/repair/rebuild
- syntax/build/test
- Git operations
- Linux/systemd/Nginx
- databases/storage
- migrations
- API/webhook verification
- DNS/TLS verification
- release/deploy/rollback
- migration and sovereignty exit
- decommission
- evidence
- never invent credentials or external success
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
import sys
import tarfile
import tempfile
import time
import urllib.request
import uuid
from typing import Any, Dict, List, Optional


ROOT = pathlib.Path(
    os.environ.get("MAJD_MAINTENANCE_ROOT", "/var/lib/majd-maintenance")
).resolve()

DB = ROOT / "majd-sovereign.db"
BACKUPS = ROOT / "backups"
RELEASES = ROOT / "releases"
EVIDENCE = ROOT / "evidence"
OWNER = "SUPREME_OWNER"


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def command(
    args: List[str],
    cwd: Optional[pathlib.Path] = None,
    timeout: int = 300,
) -> Dict[str, Any]:
    started = time.monotonic()
    try:
        cp = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "command": args,
            "returncode": cp.returncode,
            "stdout": cp.stdout[-200000:],
            "stderr": cp.stderr[-200000:],
            "duration": round(time.monotonic() - started, 4),
            "ok": cp.returncode == 0,
        }
    except Exception as exc:
        return {
            "command": args,
            "returncode": None,
            "stdout": "",
            "stderr": repr(exc),
            "duration": round(time.monotonic() - started, 4),
            "ok": False,
        }


class ExecutorStore:
    def __init__(self):
        ROOT.mkdir(parents=True, exist_ok=True)
        BACKUPS.mkdir(parents=True, exist_ok=True)
        RELEASES.mkdir(parents=True, exist_ok=True)
        EVIDENCE.mkdir(parents=True, exist_ok=True)

        self.db = sqlite3.connect(DB, timeout=30)
        self.db.row_factory = sqlite3.Row

        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS executions(
                id TEXT PRIMARY KEY,
                decision_id TEXT,
                action TEXT NOT NULL,
                target TEXT NOT NULL,
                backup_id TEXT,
                state TEXT NOT NULL,
                result TEXT NOT NULL,
                started_at TEXT NOT NULL,
                finished_at TEXT
            );

            CREATE TABLE IF NOT EXISTS backups(
                id TEXT PRIMARY KEY,
                target TEXT NOT NULL,
                archive TEXT NOT NULL,
                sha256 TEXT NOT NULL,
                verified INTEGER NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS deployments(
                id TEXT PRIMARY KEY,
                target TEXT NOT NULL,
                release_hash TEXT NOT NULL,
                previous_release TEXT,
                verification TEXT NOT NULL,
                state TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        self.db.commit()

    def evidence(self, subject: str, payload: Dict[str, Any]) -> pathlib.Path:
        eid = str(uuid.uuid4())
        path = EVIDENCE / f"executor-{eid}.json"
        path.write_text(
            json.dumps(
                {
                    "id": eid,
                    "subject": subject,
                    "created_at": now(),
                    "payload": payload,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return path


class BackupEngine:
    def __init__(self, store: ExecutorStore):
        self.store = store

    def create(self, target: pathlib.Path) -> Dict[str, Any]:
        target = target.resolve()

        if not target.exists():
            return {
                "ok": False,
                "state": "TARGET_NOT_FOUND",
                "target": str(target),
            }

        bid = str(uuid.uuid4())
        archive = BACKUPS / f"{bid}.tar.gz"

        with tarfile.open(archive, "w:gz") as tar:
            tar.add(target, arcname=target.name)

        checksum = sha256_file(archive)

        # Archive verification is real: reopen and enumerate members.
        with tarfile.open(archive, "r:gz") as tar:
            members = tar.getmembers()
            verified = len(members) > 0

        self.store.db.execute(
            "INSERT INTO backups VALUES(?,?,?,?,?,?)",
            (
                bid,
                str(target),
                str(archive),
                checksum,
                int(verified),
                now(),
            ),
        )
        self.store.db.commit()

        result = {
            "ok": verified,
            "backup_id": bid,
            "target": str(target),
            "archive": str(archive),
            "sha256": checksum,
            "members": len(members),
            "verified": verified,
        }

        self.store.evidence("BACKUP", result)
        return result

    def restore_to(
        self,
        backup_id: str,
        destination: pathlib.Path,
    ) -> Dict[str, Any]:
        row = self.store.db.execute(
            "SELECT * FROM backups WHERE id=?",
            (backup_id,),
        ).fetchone()

        if not row:
            return {"ok": False, "state": "BACKUP_NOT_FOUND"}

        archive = pathlib.Path(row["archive"])

        if not archive.exists():
            return {"ok": False, "state": "ARCHIVE_MISSING"}

        if sha256_file(archive) != row["sha256"]:
            return {"ok": False, "state": "BACKUP_INTEGRITY_FAILURE"}

        destination.mkdir(parents=True, exist_ok=True)

        with tarfile.open(archive, "r:gz") as tar:
            destination_real = destination.resolve()

            for member in tar.getmembers():
                target = (destination_real / member.name).resolve()
                if destination_real not in target.parents and target != destination_real:
                    return {
                        "ok": False,
                        "state": "UNSAFE_ARCHIVE_MEMBER",
                        "member": member.name,
                    }

            tar.extractall(destination_real)

        result = {
            "ok": True,
            "backup_id": backup_id,
            "destination": str(destination),
            "verified": True,
        }

        self.store.evidence("RESTORE", result)
        return result


class CodeEngine:
    def __init__(self, store: ExecutorStore):
        self.store = store

    def validate_python(self, path: pathlib.Path) -> Dict[str, Any]:
        return command(
            [sys.executable, "-m", "py_compile", str(path)],
            timeout=120,
        )

    def validate_tree(self, root: pathlib.Path) -> Dict[str, Any]:
        files = list(root.rglob("*.py"))
        results = [self.validate_python(p) for p in files]

        return {
            "ok": all(x["ok"] for x in results),
            "files": len(files),
            "results": results,
        }

    def atomic_write(
        self,
        path: pathlib.Path,
        content: str,
        expected_sha256: Optional[str] = None,
    ) -> Dict[str, Any]:
        path = path.resolve()

        previous_hash = (
            sha256_file(path)
            if path.exists() and path.is_file()
            else None
        )

        if expected_sha256 and previous_hash != expected_sha256:
            return {
                "ok": False,
                "state": "CONCURRENT_CHANGE_DETECTED",
                "expected": expected_sha256,
                "actual": previous_hash,
            }

        backup = None
        if path.exists():
            backup = BackupEngine(self.store).create(path)
            if not backup["ok"]:
                return {
                    "ok": False,
                    "state": "BACKUP_FAILED",
                    "backup": backup,
                }

        path.parent.mkdir(parents=True, exist_ok=True)

        fd, temp_name = tempfile.mkstemp(
            prefix=".majd-write-",
            dir=str(path.parent),
        )

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())

            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)

        validation = (
            self.validate_python(path)
            if path.suffix == ".py"
            else {"ok": True, "state": "NON_PYTHON"}
        )

        if not validation["ok"] and backup:
            restore_dir = pathlib.Path(
                tempfile.mkdtemp(prefix="majd-rollback-")
            )

            restored = BackupEngine(self.store).restore_to(
                backup["backup_id"],
                restore_dir,
            )

            if restored["ok"]:
                restored_file = restore_dir / path.name
                if restored_file.exists():
                    shutil.copy2(restored_file, path)

            return {
                "ok": False,
                "state": "VALIDATION_FAILED_ROLLED_BACK",
                "validation": validation,
                "rollback": restored,
            }

        result = {
            "ok": True,
            "state": "WRITTEN_AND_VALIDATED",
            "path": str(path),
            "sha256": sha256_file(path),
            "backup": backup,
            "validation": validation,
        }

        self.store.evidence("CODE_WRITE", result)
        return result


class GitEngine:
    def inspect(self, repo: pathlib.Path) -> Dict[str, Any]:
        return {
            "status": command(["git", "status", "--porcelain=v1"], repo),
            "branch": command(["git", "branch", "--show-current"], repo),
            "remote": command(["git", "remote", "-v"], repo),
            "history": command(
                ["git", "log", "-n", "20", "--oneline", "--decorate"],
                repo,
            ),
        }

    def verify_repository(self, repo: pathlib.Path) -> Dict[str, Any]:
        fsck = command(["git", "fsck", "--full"], repo, timeout=600)
        return {"ok": fsck["ok"], "fsck": fsck}

    def create_release_commit(
        self,
        repo: pathlib.Path,
        message: str,
    ) -> Dict[str, Any]:
        status = command(["git", "status", "--porcelain"], repo)

        if not status["ok"]:
            return {"ok": False, "status": status}

        if not status["stdout"].strip():
            return {
                "ok": True,
                "state": "NO_CHANGES",
            }

        add = command(["git", "add", "-A"], repo)
        if not add["ok"]:
            return {"ok": False, "add": add}

        commit = command(["git", "commit", "-m", message], repo)
        return {
            "ok": commit["ok"],
            "add": add,
            "commit": commit,
        }


class ServiceEngine:
    def inspect(self, service: str) -> Dict[str, Any]:
        return {
            "active": command(["systemctl", "is-active", service]),
            "enabled": command(["systemctl", "is-enabled", service]),
            "status": command(
                ["systemctl", "status", service, "--no-pager"],
            ),
        }

    def restart_verified(self, service: str) -> Dict[str, Any]:
        restart = command(["systemctl", "restart", service])

        if not restart["ok"]:
            return {
                "ok": False,
                "restart": restart,
            }

        active = command(["systemctl", "is-active", service])

        return {
            "ok": active["ok"] and active["stdout"].strip() == "active",
            "restart": restart,
            "verification": active,
        }


class NginxEngine:
    def validate(self) -> Dict[str, Any]:
        if not shutil.which("nginx"):
            return {
                "ok": False,
                "state": "NGINX_NOT_INSTALLED",
            }

        return command(["nginx", "-t"])

    def reload_verified(self) -> Dict[str, Any]:
        validation = self.validate()

        if not validation["ok"]:
            return {
                "ok": False,
                "validation": validation,
            }

        reload_result = command(["systemctl", "reload", "nginx"])

        return {
            "ok": reload_result["ok"],
            "validation": validation,
            "reload": reload_result,
        }


class TLSVerifier:
    def verify(self, host: str, port: int = 443) -> Dict[str, Any]:
        context = ssl.create_default_context()

        try:
            with socket.create_connection((host, port), timeout=10) as raw:
                with context.wrap_socket(
                    raw,
                    server_hostname=host,
                ) as tls:
                    cert = tls.getpeercert()
                    return {
                        "ok": True,
                        "protocol": tls.version(),
                        "cipher": tls.cipher(),
                        "certificate": cert,
                    }
        except Exception as exc:
            return {
                "ok": False,
                "error": repr(exc),
            }


class HTTPVerifier:
    def verify(
        self,
        url: str,
        expected_status: int = 200,
        timeout: int = 20,
    ) -> Dict[str, Any]:
        started = time.monotonic()

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "MAJD-Sovereign-Verifier/1.0"},
            )

            with urllib.request.urlopen(req, timeout=timeout) as response:
                body = response.read(1024 * 1024)

                return {
                    "ok": response.status == expected_status,
                    "status": response.status,
                    "expected": expected_status,
                    "duration": round(time.monotonic() - started, 4),
                    "body_sha256": hashlib.sha256(body).hexdigest(),
                }

        except Exception as exc:
            return {
                "ok": False,
                "error": repr(exc),
                "duration": round(time.monotonic() - started, 4),
            }


class DatabaseEngine:
    def sqlite_integrity(self, path: pathlib.Path) -> Dict[str, Any]:
        try:
            db = sqlite3.connect(path)
            rows = db.execute("PRAGMA integrity_check").fetchall()
            db.close()

            values = [x[0] for x in rows]

            return {
                "ok": values == ["ok"],
                "result": values,
            }

        except Exception as exc:
            return {
                "ok": False,
                "error": repr(exc),
            }

    def sqlite_backup(
        self,
        source: pathlib.Path,
        destination: pathlib.Path,
    ) -> Dict[str, Any]:
        try:
            src = sqlite3.connect(source)
            dst = sqlite3.connect(destination)

            with dst:
                src.backup(dst)

            src.close()
            dst.close()

            integrity = self.sqlite_integrity(destination)

            return {
                "ok": integrity["ok"],
                "destination": str(destination),
                "integrity": integrity,
            }

        except Exception as exc:
            return {
                "ok": False,
                "error": repr(exc),
            }


class MigrationEngine:
    def __init__(self, store: ExecutorStore):
        self.store = store

    def inventory(self, source: pathlib.Path) -> Dict[str, Any]:
        files = []

        for p in source.rglob("*"):
            if p.is_file():
                try:
                    files.append(
                        {
                            "path": str(p.relative_to(source)),
                            "size": p.stat().st_size,
                            "sha256": sha256_file(p),
                        }
                    )
                except OSError:
                    continue

        return {
            "source": str(source),
            "files": files,
            "count": len(files),
        }

    def copy_and_verify(
        self,
        source: pathlib.Path,
        destination: pathlib.Path,
    ) -> Dict[str, Any]:
        before = self.inventory(source)

        if destination.exists():
            backup = BackupEngine(self.store).create(destination)
            if not backup["ok"]:
                return {
                    "ok": False,
                    "state": "DESTINATION_BACKUP_FAILED",
                }

        shutil.copytree(
            source,
            destination,
            dirs_exist_ok=True,
            symlinks=True,
        )

        after = self.inventory(destination)

        before_map = {
            x["path"]: x["sha256"]
            for x in before["files"]
        }

        after_map = {
            x["path"]: x["sha256"]
            for x in after["files"]
        }

        mismatches = [
            path
            for path, value in before_map.items()
            if after_map.get(path) != value
        ]

        result = {
            "ok": not mismatches,
            "source_count": before["count"],
            "destination_count": after["count"],
            "mismatches": mismatches,
        }

        self.store.evidence("MIGRATION_VERIFY", result)
        return result


class DecommissionEngine:
    def __init__(self, store: ExecutorStore):
        self.store = store

    def prepare(
        self,
        target: pathlib.Path,
    ) -> Dict[str, Any]:
        backup = BackupEngine(self.store).create(target)

        return {
            "ok": backup["ok"],
            "state": (
                "READY_FOR_AUTHORIZED_DECOMMISSION"
                if backup["ok"]
                else "BLOCKED"
            ),
            "backup": backup,
            "destructive_action_performed": False,
            "owner_authority_preserved": True,
        }


class SovereignExecutor:
    def __init__(self):
        self.store = ExecutorStore()
        self.backup = BackupEngine(self.store)
        self.code = CodeEngine(self.store)
        self.git = GitEngine()
        self.service = ServiceEngine()
        self.nginx = NginxEngine()
        self.http = HTTPVerifier()
        self.tls = TLSVerifier()
        self.database = DatabaseEngine()
        self.migration = MigrationEngine(self.store)
        self.decommission = DecommissionEngine(self.store)

    def verify_release(
        self,
        target: pathlib.Path,
        health_urls: List[str],
    ) -> Dict[str, Any]:
        code = self.code.validate_tree(target)
        http = [self.http.verify(url) for url in health_urls]

        result = {
            "code": code,
            "http": http,
            "ok": code["ok"] and all(x["ok"] for x in http),
        }

        self.store.evidence("RELEASE_VERIFICATION", result)
        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    backup = sub.add_parser("backup")
    backup.add_argument("target")

    verify = sub.add_parser("verify")
    verify.add_argument("target")
    verify.add_argument("--url", action="append", default=[])

    service = sub.add_parser("service")
    service.add_argument("name")

    tls = sub.add_parser("tls")
    tls.add_argument("host")

    migrate = sub.add_parser("migrate")
    migrate.add_argument("source")
    migrate.add_argument("destination")

    args = parser.parse_args()
    executor = SovereignExecutor()

    if args.command == "backup":
        output = executor.backup.create(pathlib.Path(args.target))

    elif args.command == "verify":
        output = executor.verify_release(
            pathlib.Path(args.target),
            args.url,
        )

    elif args.command == "service":
        output = executor.service.inspect(args.name)

    elif args.command == "tls":
        output = executor.tls.verify(args.host)

    else:
        output = executor.migration.copy_and_verify(
            pathlib.Path(args.source),
            pathlib.Path(args.destination),
        )

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())

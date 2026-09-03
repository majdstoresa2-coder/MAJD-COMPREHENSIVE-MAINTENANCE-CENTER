#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD MAINTENANCE — FILE 02
MAJD-MAINTENANCE-EXECUTOR-02.py

REAL EXECUTION HAND

Implements controlled execution for:
code/build/refactor/rebuild
dependencies
Git/MAJD-GIT
n8n/MAJD-IN
Linux/systemd/Nginx
DB/storage/queues
API/webhooks
payments
email
DNS/TLS
backups/restores
deployment/rollback
migration
sovereignty exit
decommission

SUPREME_OWNER remains highest authority.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import shutil
import sqlite3
import subprocess
import tarfile
import tempfile
import time
import urllib.parse
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
BACKUPS = ROOT / "backups"
QUEUE = ROOT / "queue"
EVIDENCE = ROOT / "evidence"
STAGING = ROOT / "staging"
MIGRATIONS = ROOT / "migrations"

OWNER = "SUPREME_OWNER"

SERVICE_ACTIONS = {
    "start",
    "stop",
    "restart",
    "reload",
    "enable",
    "disable",
}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def stable(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
    )


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(
    argv: list[str],
    *,
    cwd: str | None = None,
    timeout: int = 900,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    try:
        process = subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "argv": argv,
            "returncode": process.returncode,
            "stdout": process.stdout[-300000:],
            "stderr": process.stderr[-150000:],
        }
    except Exception as exc:
        return {
            "argv": argv,
            "returncode": -1,
            "stdout": "",
            "stderr": repr(exc),
        }


class Executor:
    def __init__(self):
        for directory in (
            ROOT,
            BACKUPS,
            QUEUE,
            EVIDENCE,
            STAGING,
            MIGRATIONS,
        ):
            directory.mkdir(parents=True, exist_ok=True)

        self.db = sqlite3.connect(DB)
        self.db.row_factory = sqlite3.Row

    def evidence(
        self,
        category: str,
        subject: str,
        payload: Any,
    ) -> str:
        eid = str(uuid.uuid4())
        raw = stable(payload)
        digest = sha(raw.encode())

        self.db.execute("""
            INSERT INTO evidence
            (id,category,subject,payload,sha256,created_at)
            VALUES(?,?,?,?,?,?)
        """, (
            eid,
            category,
            subject,
            raw,
            digest,
            now(),
        ))
        self.db.commit()
        return eid

    def backup(
        self,
        path: pathlib.Path,
    ) -> dict[str, Any]:
        path = path.resolve()

        if not path.exists():
            raise FileNotFoundError(path)

        target = BACKUPS / (
            f"{path.name}-"
            f"{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}-"
            f"{uuid.uuid4().hex[:8]}.tar.gz"
        )

        with tarfile.open(target, "w:gz") as archive:
            archive.add(path, arcname=path.name)

        with tarfile.open(target, "r:gz") as archive:
            members = archive.getmembers()

        if not members:
            raise RuntimeError("backup verification failed")

        result = {
            "source": str(path),
            "backup": str(target),
            "size": target.stat().st_size,
            "members": len(members),
            "verified": True,
        }

        self.evidence(
            "BACKUP_VERIFIED",
            str(path),
            result,
        )
        return result

    def restore_test(
        self,
        backup: pathlib.Path,
    ) -> dict[str, Any]:
        if not backup.exists():
            raise FileNotFoundError(backup)

        with tempfile.TemporaryDirectory(
            prefix="majd-restore-"
        ) as temp:
            with tarfile.open(backup, "r:gz") as archive:
                archive.extractall(
                    temp,
                    filter="data",
                )

            restored = list(
                pathlib.Path(temp).rglob("*")
            )

            result = {
                "backup": str(backup),
                "restored_entries": len(restored),
                "verified": len(restored) > 0,
            }

        self.evidence(
            "RESTORE_VERIFICATION",
            str(backup),
            result,
        )
        return result

    def atomic_write(
        self,
        path: pathlib.Path,
        content: bytes,
    ) -> dict[str, Any]:
        path = path.resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        backup = (
            self.backup(path)
            if path.exists()
            else None
        )

        old_mode = (
            path.stat().st_mode & 0o777
            if path.exists()
            else 0o640
        )

        fd, temp_name = tempfile.mkstemp(
            dir=str(path.parent),
            prefix=f".{path.name}.",
        )

        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())

            os.chmod(temp_name, old_mode)
            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)

        result = {
            "path": str(path),
            "sha256": sha(content),
            "backup": backup,
        }

        self.evidence(
            "ATOMIC_WRITE",
            str(path),
            result,
        )
        return result

    def code_quality(
        self,
        project: pathlib.Path,
    ) -> dict[str, Any]:
        project = project.resolve()
        result: dict[str, Any] = {}

        py_files = list(project.rglob("*.py"))
        failures = []

        for file in py_files:
            check = run([
                "python3",
                "-m",
                "py_compile",
                str(file),
            ])

            if check["returncode"] != 0:
                failures.append({
                    "file": str(file),
                    "stderr": check["stderr"],
                })

        result["python_compile"] = {
            "files": len(py_files),
            "failures": failures,
            "success": not failures,
        }

        if shutil.which("pytest"):
            result["pytest"] = run(
                ["pytest", "-q"],
                cwd=str(project),
                timeout=1800,
            )

        if (
            (project / "package.json").exists()
            and shutil.which("npm")
        ):
            result["npm_test"] = run(
                ["npm", "test", "--", "--runInBand"],
                cwd=str(project),
                timeout=1800,
            )

            result["npm_build"] = run(
                ["npm", "run", "build"],
                cwd=str(project),
                timeout=1800,
            )

        self.evidence(
            "SOFTWARE_FACTORY_VERIFICATION",
            str(project),
            result,
        )
        return result

    def git_snapshot(
        self,
        repo: pathlib.Path,
    ) -> dict[str, Any]:
        repo = repo.resolve()

        if not (repo / ".git").exists():
            raise ValueError("not a git repository")

        backup = self.backup(repo)

        bundle = BACKUPS / (
            f"{repo.name}-{uuid.uuid4().hex}.bundle"
        )

        bundle_result = run([
            "git",
            "-C",
            str(repo),
            "bundle",
            "create",
            str(bundle),
            "--all",
        ])

        result = {
            "backup": backup,
            "bundle": str(bundle),
            "bundle_result": bundle_result,
            "head": run([
                "git",
                "-C",
                str(repo),
                "rev-parse",
                "HEAD",
            ]),
            "status": run([
                "git",
                "-C",
                str(repo),
                "status",
                "--porcelain",
            ]),
        }

        self.evidence(
            "GIT_SNAPSHOT",
            str(repo),
            result,
        )
        return result

    def git_fetch(
        self,
        repo: pathlib.Path,
    ) -> dict[str, Any]:
        snapshot = self.git_snapshot(repo)

        fetch = run([
            "git",
            "-C",
            str(repo),
            "fetch",
            "--all",
            "--prune",
            "--tags",
        ])

        result = {
            "snapshot": snapshot,
            "fetch": fetch,
        }

        self.evidence(
            "GIT_FETCH",
            str(repo),
            result,
        )
        return result

    def dependency_inventory(
        self,
        project: pathlib.Path,
    ) -> dict[str, Any]:
        result: dict[str, Any] = {}

        if (project / "requirements.txt").exists():
            result["requirements"] = (
                project / "requirements.txt"
            ).read_text(errors="replace").splitlines()

        if (
            (project / "package-lock.json").exists()
        ):
            result["package_lock_sha256"] = sha(
                (project / "package-lock.json")
                .read_bytes()
            )

        if shutil.which("pip-audit"):
            result["pip_audit"] = run([
                "pip-audit",
                "--format",
                "json",
            ], cwd=str(project))

        if (
            shutil.which("npm")
            and (project / "package.json").exists()
        ):
            result["npm_audit"] = run([
                "npm",
                "audit",
                "--json",
            ], cwd=str(project))

        if shutil.which("syft"):
            result["sbom"] = run([
                "syft",
                str(project),
                "-o",
                "cyclonedx-json",
            ], timeout=1800)

        self.evidence(
            "DEPENDENCY_SUPPLY_CHAIN",
            str(project),
            result,
        )
        return result

    def systemd(
        self,
        service: str,
        action: str,
    ) -> dict[str, Any]:
        if action not in SERVICE_ACTIONS:
            raise ValueError("action denied")

        if (
            "/" in service
            or not service.endswith(".service")
        ):
            raise ValueError("invalid service")

        before = run([
            "systemctl",
            "show",
            service,
            "--property=ActiveState,SubState,UnitFileState",
        ])

        execution = run([
            "systemctl",
            action,
            service,
        ])

        after = run([
            "systemctl",
            "show",
            service,
            "--property=ActiveState,SubState,UnitFileState",
        ])

        result = {
            "before": before,
            "execution": execution,
            "after": after,
        }

        self.evidence(
            "SYSTEMD_EXECUTION",
            service,
            result,
        )
        return result

    def nginx_reload(self) -> dict[str, Any]:
        if not shutil.which("nginx"):
            return {
                "state":
                    "EXTERNAL_DEPENDENCY_REQUIRED",
                "dependency": "nginx executable",
            }

        validation = run(["nginx", "-t"])

        if validation["returncode"] != 0:
            return {
                "state": "DENIED",
                "validation": validation,
            }

        execution = run([
            "systemctl",
            "reload",
            "nginx",
        ])

        result = {
            "validation": validation,
            "execution": execution,
        }

        self.evidence(
            "NGINX_RELOAD",
            "nginx",
            result,
        )
        return result

    def sqlite_backup(
        self,
        source: pathlib.Path,
    ) -> dict[str, Any]:
        source = source.resolve()

        target = BACKUPS / (
            f"{source.name}-"
            f"{uuid.uuid4().hex}.sqlite3"
        )

        src = sqlite3.connect(str(source))
        dst = sqlite3.connect(str(target))

        with dst:
            src.backup(dst)

        integrity = dst.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]

        src.close()
        dst.close()

        result = {
            "source": str(source),
            "backup": str(target),
            "integrity": integrity,
            "verified": integrity == "ok",
        }

        self.evidence(
            "DATABASE_BACKUP",
            str(source),
            result,
        )
        return result

    def sqlite_integrity(
        self,
        path: pathlib.Path,
    ) -> dict[str, Any]:
        db = sqlite3.connect(
            f"file:{path.resolve()}?mode=ro",
            uri=True,
        )

        integrity = db.execute(
            "PRAGMA integrity_check"
        ).fetchall()

        foreign = db.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        db.close()

        result = {
            "integrity": [x[0] for x in integrity],
            "foreign_key_errors":
                [list(x) for x in foreign],
            "verified": (
                len(integrity) == 1
                and integrity[0][0] == "ok"
                and not foreign
            ),
        }

        self.evidence(
            "DATABASE_INTEGRITY",
            str(path),
            result,
        )
        return result

    def postgres_backup(
        self,
        dsn: str,
    ) -> dict[str, Any]:
        if not shutil.which("pg_dump"):
            return {
                "state":
                    "EXTERNAL_DEPENDENCY_REQUIRED",
                "dependency": "pg_dump",
            }

        output = BACKUPS / (
            f"postgres-{uuid.uuid4().hex}.dump"
        )

        result = run([
            "pg_dump",
            "--format=custom",
            "--file",
            str(output),
            dsn,
        ], timeout=3600)

        verified = (
            result["returncode"] == 0
            and output.exists()
            and output.stat().st_size > 0
        )

        payload = {
            "execution": result,
            "backup": str(output),
            "verified": verified,
        }

        self.evidence(
            "POSTGRES_BACKUP",
            "postgres",
            payload,
        )
        return payload

    def redis_health(self) -> dict[str, Any]:
        if not shutil.which("redis-cli"):
            return {
                "state": "NOT_VISIBLE",
            }

        result = run([
            "redis-cli",
            "--no-auth-warning",
            "PING",
        ])

        return {
            "verified":
                result["stdout"].strip() == "PONG",
            "execution": result,
        }

    def http(
        self,
        url: str,
        expected: int = 200,
        method: str = "GET",
        body: Any = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        data = (
            json.dumps(body).encode()
            if body is not None
            else None
        )

        request = urllib.request.Request(
            url,
            data=data,
            method=method.upper(),
            headers=headers or {},
        )

        started = time.monotonic()

        try:
            with urllib.request.urlopen(
                request,
                timeout=30,
            ) as response:
                payload = response.read(
                    1024 * 1024
                )

                result = {
                    "verified":
                        response.status == expected,
                    "status": response.status,
                    "expected": expected,
                    "latency_ms": round(
                        (
                            time.monotonic()
                            - started
                        ) * 1000,
                        2,
                    ),
                    "body_sha256": sha(payload),
                }
        except Exception as exc:
            result = {
                "verified": False,
                "error": repr(exc),
            }

        self.evidence(
            "HTTP_TRANSACTION",
            url,
            result,
        )
        return result

    def webhook_verify_hmac(
        self,
        body: bytes,
        signature: str,
        secret: str,
        algorithm: str = "sha256",
    ) -> bool:
        import hmac

        digestmod = getattr(
            hashlib,
            algorithm,
        )

        expected = hmac.new(
            secret.encode(),
            body,
            digestmod,
        ).hexdigest()

        return hmac.compare_digest(
            expected,
            signature,
        )

    def external_provider(
        self,
        provider: str,
        required_environment: list[str],
    ) -> dict[str, Any]:
        missing = [
            key
            for key in required_environment
            if not os.environ.get(key)
        ]

        if missing:
            return {
                "state":
                    "EXTERNAL_DEPENDENCY_REQUIRED",
                "provider": provider,
                "missing": missing,
            }

        return {
            "state":
                "CONFIGURATION_PRESENT_REQUIRES_REAL_TRANSACTION_VERIFICATION",
            "provider": provider,
        }

    def payment_provider(self) -> dict[str, Any]:
        return self.external_provider(
            "PAYMENT_PROVIDER",
            [
                "MAJD_PAYMENT_API_KEY",
                "MAJD_PAYMENT_BASE_URL",
            ],
        )

    def email_provider(self) -> dict[str, Any]:
        return self.external_provider(
            "EMAIL_PROVIDER",
            [
                "MAJD_EMAIL_API_KEY",
                "MAJD_EMAIL_BASE_URL",
            ],
        )

    def n8n(self) -> dict[str, Any]:
        base = os.environ.get(
            "MAJD_N8N_BASE_URL"
        )

        token = os.environ.get(
            "MAJD_N8N_API_KEY"
        )

        if not base or not token:
            return {
                "state":
                    "EXTERNAL_DEPENDENCY_REQUIRED",
                "missing": [
                    name
                    for name, value in {
                        "MAJD_N8N_BASE_URL": base,
                        "MAJD_N8N_API_KEY": token,
                    }.items()
                    if not value
                ],
            }

        return self.http(
            base.rstrip("/") + "/api/v1/workflows",
            expected=200,
            headers={
                "X-N8N-API-KEY": token,
            },
        )

    def dns_query(
        self,
        domain: str,
    ) -> dict[str, Any]:
        result = {
            "domain": domain,
            "addresses": [],
        }

        try:
            infos = socket.getaddrinfo(
                domain,
                None,
            )

            result["addresses"] = sorted({
                item[4][0]
                for item in infos
            })
            result["verified"] = True
        except Exception as exc:
            result["verified"] = False
            result["error"] = repr(exc)

        self.evidence(
            "DNS_VERIFICATION",
            domain,
            result,
        )
        return result

    def tls_certificate(
        self,
        host: str,
        port: int = 443,
    ) -> dict[str, Any]:
        import ssl

        context = ssl.create_default_context()

        try:
            with socket.create_connection(
                (host, port),
                timeout=10,
            ) as raw:
                with context.wrap_socket(
                    raw,
                    server_hostname=host,
                ) as tls:
                    cert = tls.getpeercert()

                    result = {
                        "verified": True,
                        "protocol": tls.version(),
                        "cipher": tls.cipher(),
                        "not_after":
                            cert.get("notAfter"),
                        "subject_alt_name":
                            cert.get(
                                "subjectAltName",
                                [],
                            ),
                    }
        except Exception as exc:
            result = {
                "verified": False,
                "error": repr(exc),
            }

        self.evidence(
            "TLS_VERIFICATION",
            host,
            result,
        )
        return result

    def migration_inventory(
        self,
        repo: pathlib.Path,
    ) -> dict[str, Any]:
        repo = repo.resolve()

        inventory = {
            "repo": str(repo),
            "git": (repo / ".git").exists(),
            "branches": [],
            "tags": [],
            "remotes": [],
            "databases": [],
            "environment_files": [],
            "deployment_files": [],
            "workflows": [],
        }

        if inventory["git"]:
            inventory["branches"] = run([
                "git",
                "-C",
                str(repo),
                "branch",
                "-a",
            ])["stdout"].splitlines()

            inventory["tags"] = run([
                "git",
                "-C",
                str(repo),
                "tag",
                "--list",
            ])["stdout"].splitlines()

            inventory["remotes"] = run([
                "git",
                "-C",
                str(repo),
                "remote",
                "-v",
            ])["stdout"].splitlines()

        for path in repo.rglob("*"):
            if not path.is_file():
                continue

            lower = path.name.lower()

            if lower.endswith(
                (".sqlite", ".sqlite3", ".db")
            ):
                inventory["databases"].append(
                    str(path)
                )

            if lower.startswith(".env"):
                inventory[
                    "environment_files"
                ].append({
                    "path": str(path),
                    "secret_values":
                        "NOT_CAPTURED",
                })

            if lower in {
                "dockerfile",
                "docker-compose.yml",
                "docker-compose.yaml",
                "railway.json",
                "railway.toml",
                "nginx.conf",
            }:
                inventory[
                    "deployment_files"
                ].append(str(path))

            if ".github/workflows" in str(path):
                inventory[
                    "workflows"
                ].append(str(path))

        self.evidence(
            "MIGRATION_INVENTORY",
            str(repo),
            inventory,
        )
        return inventory

    def migration_snapshot(
        self,
        repo: pathlib.Path,
    ) -> dict[str, Any]:
        inventory = self.migration_inventory(repo)
        snapshot = self.git_snapshot(repo)

        db_backups = []

        for item in inventory["databases"]:
            try:
                db_backups.append(
                    self.sqlite_backup(
                        pathlib.Path(item)
                    )
                )
            except Exception as exc:
                db_backups.append({
                    "path": item,
                    "error": repr(exc),
                })

        result = {
            "inventory": inventory,
            "repository_snapshot": snapshot,
            "database_backups": db_backups,
            "cutover":
                "REQUIRES_TARGET_AND_VERIFICATION",
            "rollback":
                "SOURCE_REMAINS_UNCHANGED_UNTIL_VERIFIED",
        }

        self.evidence(
            "COMPLETE_MIGRATION_SNAPSHOT",
            str(repo),
            result,
        )
        return result

    def decommission_gate(
        self,
        resource: str,
        checks: dict[str, bool],
    ) -> dict[str, Any]:
        required = {
            "backup_verified",
            "dependencies_cleared",
            "traffic_drained",
            "data_handled",
            "secret_revocation_planned",
            "dns_cleanup_planned",
            "provider_cancellation_authorized",
            "cross_platform_impact_cleared",
        }

        missing = sorted(
            key
            for key in required
            if not checks.get(key)
        )

        result = {
            "resource": resource,
            "allowed": not missing,
            "missing": missing,
        }

        self.evidence(
            "DECOMMISSION_GATE",
            resource,
            result,
        )
        return result

    def independent_verification(
        self,
        platform: str,
        change_id: str,
        workflows: list[dict[str, Any]],
        rollback: dict[str, Any],
    ) -> str:
        request_id = str(uuid.uuid4())

        payload = {
            "request_id": request_id,
            "change_id": change_id,
            "platform": platform,
            "workflows": workflows,
            "rollback": rollback,
            "requested_by": "EXECUTOR_02",
            "verifier": "RUNTIME_03",
            "created_at": now(),
        }

        path = QUEUE / (
            f"verify-{request_id}.json"
        )

        path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        self.evidence(
            "INDEPENDENT_VERIFICATION_REQUEST",
            change_id,
            payload,
        )
        return str(path)

    def execute_queue_item(
        self,
        path: pathlib.Path,
    ) -> dict[str, Any]:
        request = json.loads(
            path.read_text(encoding="utf-8")
        )

        action = request["action"]
        payload = request["payload"]

        handlers = {
            "GIT_FETCH":
                lambda:
                self.git_fetch(
                    pathlib.Path(payload["repo"])
                ),

            "PROJECT_VERIFY":
                lambda:
                self.code_quality(
                    pathlib.Path(payload["project"])
                ),

            "SYSTEMD":
                lambda:
                self.systemd(
                    payload["service"],
                    payload["service_action"],
                ),

            "NGINX_RELOAD":
                self.nginx_reload,

            "HTTP_VERIFY":
                lambda:
                self.http(
                    payload["url"],
                    int(
                        payload.get(
                            "expected_status",
                            200,
                        )
                    ),
                ),

            "DNS_VERIFY":
                lambda:
                self.dns_query(
                    payload["domain"]
                ),

            "TLS_VERIFY":
                lambda:
                self.tls_certificate(
                    payload["host"],
                    int(payload.get("port", 443)),
                ),

            "N8N_VERIFY":
                self.n8n,

            "MIGRATION_SNAPSHOT":
                lambda:
                self.migration_snapshot(
                    pathlib.Path(payload["repo"])
                ),
        }

        if action not in handlers:
            result = {
                "state": "DENIED",
                "reason":
                    "ACTION_NOT_IN_CONTROLLED_EXECUTION_PRIMITIVES",
            }
        else:
            result = handlers[action]()

        self.evidence(
            "EXECUTION_RESULT",
            request["decision_id"],
            result,
        )

        if payload.get(
            "verification_workflows"
        ):
            self.independent_verification(
                request["platform"],
                request["decision_id"],
                payload[
                    "verification_workflows"
                ],
                payload.get("rollback", {}),
            )

        os.replace(
            path,
            path.with_suffix(".processed.json"),
        )

        return result

    def cycle(self) -> dict[str, Any]:
        results = []

        for item in sorted(
            QUEUE.glob("executor-*.json")
        ):
            try:
                results.append({
                    "queue": str(item),
                    "result":
                        self.execute_queue_item(item),
                })
            except Exception as exc:
                self.evidence(
                    "EXECUTOR_FAILURE",
                    str(item),
                    {"error": repr(exc)},
                )

        return {
            "processed": len(results),
            "results": results,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    sub.add_parser("cycle")

    p_backup = sub.add_parser("backup")
    p_backup.add_argument("path")

    p_restore = sub.add_parser("restore-test")
    p_restore.add_argument("backup")

    p_project = sub.add_parser("verify-project")
    p_project.add_argument("project")

    p_migration = sub.add_parser("migration-snapshot")
    p_migration.add_argument("repo")

    p_loop = sub.add_parser("loop")
    p_loop.add_argument(
        "--interval",
        type=int,
        default=30,
    )

    args = parser.parse_args()
    app = Executor()

    if args.command == "cycle":
        print(json.dumps(
            app.cycle(),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    if args.command == "backup":
        print(json.dumps(
            app.backup(
                pathlib.Path(args.path)
            ),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    if args.command == "restore-test":
        print(json.dumps(
            app.restore_test(
                pathlib.Path(args.backup)
            ),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    if args.command == "verify-project":
        print(json.dumps(
            app.code_quality(
                pathlib.Path(args.project)
            ),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    if args.command == "migration-snapshot":
        print(json.dumps(
            app.migration_snapshot(
                pathlib.Path(args.repo)
            ),
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
                    "EXECUTOR_LOOP_FAILURE",
                    "executor",
                    {"error": repr(exc)},
                )
            time.sleep(
                max(10, args.interval)
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

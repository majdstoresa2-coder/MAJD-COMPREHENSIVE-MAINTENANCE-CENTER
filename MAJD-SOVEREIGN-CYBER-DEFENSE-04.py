#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD MAINTENANCE — FILE 04
MAJD-SOVEREIGN-CYBER-DEFENSE-04.py

SOVEREIGN DEFENSE LAYER

Defensive implementation:
Zero Trust
Secrets
Identity/session
Network/API
Threat intelligence ingestion
Vulnerability management
Malware/persistence indicators
Supply chain
AI/Agent/Tool defense
Integrity
Containment/quarantine
Hardware/Firmware security
BMC isolation checks
Physical/cyber-physical safety boundary
Secure media lifecycle
Evidence

NO FILE 05.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import hmac
import json
import os
import pathlib
import re
import shutil
import socket
import sqlite3
import stat
import subprocess
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
QUARANTINE = ROOT / "quarantine"

OWNER = "SUPREME_OWNER"

SENSITIVE_PORTS = {
    22: "SSH",
    2375: "DOCKER_UNENCRYPTED",
    3306: "MYSQL",
    5432: "POSTGRES",
    6379: "REDIS",
    11211: "MEMCACHED",
    6443: "KUBERNETES_API",
}

SECRET_PATTERNS = (
    re.compile(
        rb"(?i)(api[_-]?key|secret|token|password)"
        rb"\s*[:=]\s*['\"]?([^'\"\s]{8,})"
    ),
    re.compile(
        rb"-----BEGIN (?:RSA |EC |OPENSSH )?"
        rb"PRIVATE KEY-----"
    ),
)


def now() -> str:
    return dt.datetime.now(
        dt.timezone.utc
    ).isoformat()


def run(
    argv: list[str],
    timeout: int = 300,
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


class Defense:
    def __init__(self):
        ROOT.mkdir(
            parents=True,
            exist_ok=True,
        )
        QUARANTINE.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.db = sqlite3.connect(DB)
        self.db.row_factory = sqlite3.Row

        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS integrity_baseline(
            path TEXT PRIMARY KEY,
            sha256 TEXT NOT NULL,
            mode INTEGER NOT NULL,
            uid INTEGER NOT NULL,
            gid INTEGER NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS security_findings(
            id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            severity TEXT NOT NULL,
            subject TEXT NOT NULL,
            details TEXT NOT NULL,
            remediation TEXT NOT NULL,
            containment TEXT NOT NULL,
            verification TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS threat_indicators(
            id TEXT PRIMARY KEY,
            indicator_type TEXT NOT NULL,
            indicator_hash TEXT NOT NULL,
            source TEXT NOT NULL,
            confidence REAL NOT NULL,
            expires_at TEXT,
            metadata TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(indicator_type,indicator_hash,source)
        );

        CREATE TABLE IF NOT EXISTS media_lifecycle(
            id TEXT PRIMARY KEY,
            device TEXT NOT NULL,
            serial TEXT,
            state TEXT NOT NULL,
            evidence TEXT NOT NULL,
            updated_at TEXT NOT NULL
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

    def finding(
        self,
        category: str,
        severity: str,
        subject: str,
        details: dict[str, Any],
        remediation: dict[str, Any] | None = None,
        containment: dict[str, Any] | None = None,
    ) -> str:
        fid = str(uuid.uuid4())

        self.db.execute("""
            INSERT INTO security_findings
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """, (
            fid,
            category,
            severity,
            subject,
            json.dumps(
                details,
                ensure_ascii=False,
            ),
            json.dumps(
                remediation or {},
                ensure_ascii=False,
            ),
            json.dumps(
                containment or {},
                ensure_ascii=False,
            ),
            json.dumps({}),
            "OPEN",
            now(),
            now(),
        ))
        self.db.commit()
        return fid

    @staticmethod
    def hash_file(
        path: pathlib.Path,
    ) -> str:
        h = hashlib.sha256()

        with path.open("rb") as handle:
            for chunk in iter(
                lambda:
                handle.read(1024 * 1024),
                b"",
            ):
                h.update(chunk)

        return h.hexdigest()

    def baseline(
        self,
        roots: list[pathlib.Path],
    ) -> dict[str, Any]:
        count = 0

        for root in roots:
            root = root.resolve()

            if root.is_file():
                candidates = [root]
            elif root.is_dir():
                candidates = root.rglob("*")
            else:
                continue

            for path in candidates:
                try:
                    if (
                        not path.is_file()
                        or path.is_symlink()
                    ):
                        continue

                    st = path.stat()

                    self.db.execute("""
                        INSERT INTO integrity_baseline
                        VALUES(?,?,?,?,?,?)
                        ON CONFLICT(path) DO UPDATE SET
                            sha256=excluded.sha256,
                            mode=excluded.mode,
                            uid=excluded.uid,
                            gid=excluded.gid,
                            updated_at=excluded.updated_at
                    """, (
                        str(path),
                        self.hash_file(path),
                        stat.S_IMODE(
                            st.st_mode
                        ),
                        st.st_uid,
                        st.st_gid,
                        now(),
                    ))

                    count += 1

                except (
                    PermissionError,
                    FileNotFoundError,
                    OSError,
                ):
                    continue

        self.db.commit()

        result = {
            "baselined": count,
        }

        self.evidence(
            "INTEGRITY_BASELINE",
            "filesystem",
            result,
        )
        return result

    def integrity(self) -> list[dict[str, Any]]:
        findings = []

        for row in self.db.execute(
            "SELECT * FROM integrity_baseline"
        ):
            path = pathlib.Path(
                row["path"]
            )

            if not path.exists():
                item = {
                    "path": str(path),
                    "state": "MISSING",
                }

                findings.append(item)

                self.finding(
                    "INTEGRITY",
                    "HIGH",
                    str(path),
                    item,
                )
                continue

            try:
                current_hash = (
                    self.hash_file(path)
                )

                st = path.stat()

                current_mode = stat.S_IMODE(
                    st.st_mode
                )
            except Exception as exc:
                findings.append({
                    "path": str(path),
                    "state": "UNREADABLE",
                    "error": repr(exc),
                })
                continue

            changes = {}

            if current_hash != row["sha256"]:
                changes["sha256"] = {
                    "expected":
                        row["sha256"],
                    "actual":
                        current_hash,
                }

            if current_mode != row["mode"]:
                changes["mode"] = {
                    "expected":
                        row["mode"],
                    "actual":
                        current_mode,
                }

            if st.st_uid != row["uid"]:
                changes["uid"] = {
                    "expected":
                        row["uid"],
                    "actual":
                        st.st_uid,
                }

            if changes:
                item = {
                    "path": str(path),
                    "state": "CHANGED",
                    "changes": changes,
                }

                findings.append(item)

                self.finding(
                    "INTEGRITY",
                    "HIGH",
                    str(path),
                    item,
                )

        self.evidence(
            "INTEGRITY_CHECK",
            "filesystem",
            findings,
        )
        return findings

    def secrets(
        self,
        roots: list[pathlib.Path],
    ) -> list[dict[str, Any]]:
        findings = []

        ignored = {
            ".git",
            "node_modules",
            ".venv",
            "venv",
            "__pycache__",
            "backups",
            "quarantine",
        }

        for root in roots:
            if not root.exists():
                continue

            candidates = (
                [root]
                if root.is_file()
                else root.rglob("*")
            )

            for path in candidates:
                try:
                    if (
                        not path.is_file()
                        or path.stat().st_size
                        > 5 * 1024 * 1024
                        or any(
                            part in ignored
                            for part in path.parts
                        )
                    ):
                        continue

                    data = path.read_bytes()
                except Exception:
                    continue

                if any(
                    pattern.search(data)
                    for pattern
                    in SECRET_PATTERNS
                ):
                    item = {
                        "path": str(path),
                        "secret":
                            "REDACTED_NOT_CAPTURED",
                    }

                    findings.append(item)

                    self.finding(
                        "SECRET_EXPOSURE",
                        "CRITICAL",
                        str(path),
                        item,
                        remediation={
                            "rotate_if_real":
                                True,
                            "remove_from_history":
                                True,
                            "move_to_secret_store":
                                True,
                        },
                    )

        self.evidence(
            "SECRET_SCAN",
            "projects",
            findings,
        )
        return findings

    def identity(self) -> dict[str, Any]:
        result = {
            "ssh": {},
            "sudo": {},
            "shadow_permissions": {},
        }

        sshd = pathlib.Path(
            "/etc/ssh/sshd_config"
        )

        if sshd.exists():
            result["ssh"] = {
                "path": str(sshd),
                "sha256":
                    self.hash_file(sshd),
                "effective": run([
                    "sshd",
                    "-T",
                ]) if shutil.which(
                    "sshd"
                ) else {},
            }

        sudoers = pathlib.Path(
            "/etc/sudoers"
        )

        if sudoers.exists():
            st = sudoers.stat()

            result["sudo"] = {
                "mode":
                    oct(
                        stat.S_IMODE(
                            st.st_mode
                        )
                    ),
                "sha256":
                    self.hash_file(
                        sudoers
                    ),
            }

        shadow = pathlib.Path(
            "/etc/shadow"
        )

        if shadow.exists():
            st = shadow.stat()

            result[
                "shadow_permissions"
            ] = {
                "mode":
                    oct(
                        stat.S_IMODE(
                            st.st_mode
                        )
                    ),
                "uid": st.st_uid,
                "gid": st.st_gid,
            }

        self.evidence(
            "IDENTITY_DEFENSE",
            "local-host",
            result,
        )
        return result

    def network(self) -> list[dict[str, Any]]:
        if not shutil.which("ss"):
            return []

        listeners = run([
            "ss",
            "-lntupH",
        ])

        findings = []

        for line in listeners[
            "stdout"
        ].splitlines():

            for port, service in (
                SENSITIVE_PORTS.items()
            ):
                pattern = (
                    rf"(?:0\.0\.0\.0|"
                    rf"\[::\]|\*)\:{port}\b"
                )

                if re.search(
                    pattern,
                    line,
                ):
                    item = {
                        "port": port,
                        "service": service,
                        "listener": line,
                        "reason":
                            "SENSITIVE_SERVICE_ON_WILDCARD_ADDRESS",
                    }

                    findings.append(item)

                    self.finding(
                        "NETWORK_EXPOSURE",
                        "HIGH",
                        f"port:{port}",
                        item,
                        remediation={
                            "bind_private":
                                True,
                            "firewall_review":
                                True,
                            "authentication_review":
                                True,
                        },
                    )

        self.evidence(
            "NETWORK_DEFENSE",
            "local-host",
            findings,
        )
        return findings

    def persistence(self) -> dict[str, Any]:
        result = {
            "enabled_units": run([
                "systemctl",
                "list-unit-files",
                "--state=enabled",
                "--no-pager",
            ]) if shutil.which(
                "systemctl"
            ) else {},
            "cron": [],
            "authorized_keys": [],
        }

        for base in (
            pathlib.Path("/etc/cron.d"),
            pathlib.Path("/var/spool/cron"),
        ):
            if not base.exists():
                continue

            for path in base.rglob("*"):
                if path.is_file():
                    try:
                        result["cron"].append({
                            "path": str(path),
                            "sha256":
                                self.hash_file(
                                    path
                                ),
                        })
                    except Exception:
                        continue

        for base in (
            pathlib.Path("/root"),
            pathlib.Path("/home"),
        ):
            if not base.exists():
                continue

            for path in base.rglob(
                "authorized_keys"
            ):
                try:
                    result[
                        "authorized_keys"
                    ].append({
                        "path": str(path),
                        "sha256":
                            self.hash_file(
                                path
                            ),
                        "mode":
                            oct(
                                stat.S_IMODE(
                                    path.stat()
                                    .st_mode
                                )
                            ),
                    })
                except Exception:
                    continue

        self.evidence(
            "PERSISTENCE_DISCOVERY",
            "local-host",
            result,
        )
        return result

    def vulnerability(
        self,
        project: pathlib.Path,
    ) -> dict[str, Any]:
        result: dict[str, Any] = {}

        if shutil.which("pip-audit"):
            result["pip"] = run([
                "pip-audit",
                "--format",
                "json",
            ], timeout=1200)

        if (
            shutil.which("npm")
            and (
                project / "package.json"
            ).exists()
        ):
            result["npm"] = run([
                "npm",
                "audit",
                "--json",
            ], timeout=1200)

        if shutil.which("trivy"):
            result["trivy"] = run([
                "trivy",
                "fs",
                "--format",
                "json",
                str(project),
            ], timeout=1800)

        if shutil.which("osv-scanner"):
            result["osv"] = run([
                "osv-scanner",
                "-r",
                str(project),
            ], timeout=1800)

        if not result:
            result = {
                "visibility":
                    "NOT_VISIBLE",
                "reason":
                    "SUPPORTED_SCANNER_NOT_INSTALLED",
            }

        self.evidence(
            "VULNERABILITY_MANAGEMENT",
            str(project),
            result,
        )
        return result

    def supply_chain(
        self,
        project: pathlib.Path,
    ) -> dict[str, Any]:
        result = {
            "lockfiles": {},
            "sbom": None,
            "git_head": None,
        }

        for name in (
            "package-lock.json",
            "pnpm-lock.yaml",
            "yarn.lock",
            "requirements.txt",
            "poetry.lock",
            "uv.lock",
        ):
            path = project / name

            if path.exists():
                result[
                    "lockfiles"
                ][name] = self.hash_file(
                    path
                )

        if (
            project / ".git"
        ).exists():
            result["git_head"] = run([
                "git",
                "-C",
                str(project),
                "rev-parse",
                "HEAD",
            ])

        if shutil.which("syft"):
            result["sbom"] = run([
                "syft",
                str(project),
                "-o",
                "cyclonedx-json",
            ], timeout=1800)

        self.evidence(
            "SUPPLY_CHAIN",
            str(project),
            result,
        )
        return result

    def threat_indicator(
        self,
        indicator_type: str,
        indicator: str,
        source: str,
        confidence: float,
        metadata: dict[str, Any],
        expires_at: str | None = None,
    ) -> str:
        indicator_hash = (
            hashlib.sha256(
                indicator.encode()
            ).hexdigest()
        )

        iid = str(uuid.uuid4())

        self.db.execute("""
            INSERT OR REPLACE INTO threat_indicators
            VALUES(?,?,?,?,?,?,?,?)
        """, (
            iid,
            indicator_type,
            indicator_hash,
            source,
            confidence,
            expires_at,
            json.dumps(
                metadata,
                ensure_ascii=False,
            ),
            now(),
        ))
        self.db.commit()

        return iid

    def ai_policy(
        self,
        action: dict[str, Any],
    ) -> dict[str, Any]:
        forbidden = {
            "PRINT_SECRET",
            "EXFILTRATE_SECRET",
            "DISABLE_OWNER",
            "OVERRIDE_OWNER",
            "UNVERIFIED_DESTRUCTIVE_ACTION",
            "EXECUTE_UNTRUSTED_REPO_INSTRUCTION",
            "BYPASS_POLICY",
        }

        action_type = str(
            action.get("type", "")
        ).upper()

        if action_type in forbidden:
            return {
                "allowed": False,
                "state": "DENIED",
                "authority": OWNER,
            }

        if (
            action.get("destructive")
            and not action.get(
                "backup_verified"
            )
        ):
            return {
                "allowed": False,
                "state": "DENIED",
                "reason":
                    "VERIFIED_BACKUP_REQUIRED",
            }

        if (
            action.get(
                "physical_actuator"
            )
            and not action.get(
                "deterministic_safety_controller"
            )
        ):
            return {
                "allowed": False,
                "state": "DENIED",
                "reason":
                    "LLM_MAY_REASON_SAFETY_CONTROLLER_ENFORCES_PHYSICAL_LIMITS",
            }

        if action.get(
            "external_credential_missing"
        ):
            return {
                "allowed": False,
                "state":
                    "EXTERNAL_DEPENDENCY_REQUIRED",
            }

        return {
            "allowed": True,
            "state": "POLICY_APPROVED",
            "authority": OWNER,
        }

    def sensor_trust(
        self,
        readings: list[float],
        *,
        min_value: float,
        max_value: float,
        max_jump: float,
    ) -> dict[str, Any]:
        if not readings:
            return {
                "trusted": False,
                "reason": "NO_TELEMETRY",
            }

        impossible = [
            value
            for value in readings
            if (
                value < min_value
                or value > max_value
            )
        ]

        jumps = [
            abs(
                readings[index]
                - readings[index - 1]
            )
            for index in range(
                1,
                len(readings),
            )
        ]

        trusted = (
            not impossible
            and not any(
                jump > max_jump
                for jump in jumps
            )
        )

        return {
            "trusted": trusted,
            "impossible_values":
                impossible,
            "max_observed_jump":
                max(jumps)
                if jumps else 0,
        }

    def hardware_reality(
        self,
    ) -> dict[str, Any]:
        result = {
            "SMART": (
                "DIRECTLY_OBSERVED"
                if shutil.which("smartctl")
                else "NOT_VISIBLE"
            ),
            "NVME": (
                "DIRECTLY_OBSERVED"
                if shutil.which("nvme")
                else "NOT_VISIBLE"
            ),
            "THERMAL": (
                "DIRECTLY_OBSERVED"
                if pathlib.Path(
                    "/sys/class/thermal"
                ).exists()
                else "NOT_VISIBLE"
            ),
            "ECC": (
                "DIRECTLY_OBSERVED"
                if pathlib.Path(
                    "/sys/devices/system/edac"
                ).exists()
                else "NOT_VISIBLE"
            ),
            "BMC": (
                "DIRECTLY_OBSERVED"
                if shutil.which("ipmitool")
                else "NOT_VISIBLE"
            ),
            "UPS": (
                "DIRECTLY_OBSERVED"
                if shutil.which("upsc")
                else "NOT_VISIBLE"
            ),
            "FACILITY_COOLING":
                "NOT_VISIBLE",
            "FACILITY_FIRE":
                "NOT_VISIBLE",
            "FACILITY_HUMIDITY":
                "NOT_VISIBLE",
            "PHYSICAL_ACCESS":
                "NOT_VISIBLE",
        }

        self.evidence(
            "HARDWARE_REALITY",
            "local-host",
            result,
        )
        return result

    def bmc(self) -> dict[str, Any]:
        if not shutil.which(
            "ipmitool"
        ):
            result = {
                "visibility":
                    "NOT_VISIBLE",
                "security_claim":
                    "NONE",
            }

            self.evidence(
                "BMC_SECURITY",
                "local-host",
                result,
            )
            return result

        result = {
            "visibility":
                "DIRECTLY_OBSERVED",
            "local_access":
                run([
                    "ipmitool",
                    "mc",
                    "info",
                ]),
            "network_configuration":
                "NOT_PERSISTED_TO_AVOID_SECRET_OR_MANAGEMENT_DATA_EXPOSURE",
            "public_internet_exposure":
                "REQUIRES_NETWORK_CORRELATION",
        }

        self.evidence(
            "BMC_SECURITY",
            "local-host",
            result,
        )
        return result

    def quarantine(
        self,
        path: pathlib.Path,
        reason: str,
    ) -> dict[str, Any]:
        path = path.resolve()

        if not path.is_file():
            raise ValueError(
                "target must be a file"
            )

        protected = (
            "/bin/",
            "/sbin/",
            "/usr/bin/",
            "/usr/sbin/",
            "/lib/",
            "/lib64/",
        )

        if any(
            str(path).startswith(prefix)
            for prefix in protected
        ):
            return {
                "state":
                    "OWNER_ACTION_REQUIRED",
                "reason":
                    "HIGH_BLAST_RADIUS_SYSTEM_FILE",
            }

        file_hash = self.hash_file(
            path
        )

        destination = QUARANTINE / (
            file_hash[:16]
            + "-"
            + path.name
        )

        os.replace(
            path,
            destination,
        )

        os.chmod(
            destination,
            0,
        )

        result = {
            "state": "QUARANTINED",
            "original": str(path),
            "destination":
                str(destination),
            "sha256": file_hash,
            "reason": reason,
        }

        self.evidence(
            "CONTAINMENT",
            str(path),
            result,
        )
        return result

    def media_state(
        self,
        device: str,
        state: str,
        serial: str | None,
        evidence: dict[str, Any],
    ) -> str:
        allowed = {
            "NEW",
            "ASSIGNED",
            "IN_USE",
            "FAILED",
            "RETIRED",
            "SANITIZED",
            "DESTROYED",
        }

        if state not in allowed:
            raise ValueError(
                "invalid media lifecycle state"
            )

        mid = str(uuid.uuid4())

        self.db.execute("""
            INSERT INTO media_lifecycle
            VALUES(?,?,?,?,?,?)
        """, (
            mid,
            device,
            serial,
            state,
            json.dumps(
                evidence,
                ensure_ascii=False,
            ),
            now(),
        ))
        self.db.commit()

        return mid

    def cycle(
        self,
        projects: list[pathlib.Path],
    ) -> dict[str, Any]:
        result = {
            "integrity":
                self.integrity(),
            "secrets":
                self.secrets(projects),
            "identity":
                self.identity(),
            "network":
                self.network(),
            "persistence":
                self.persistence(),
            "hardware_reality":
                self.hardware_reality(),
            "bmc":
                self.bmc(),
            "projects": {},
        }

        for project in projects:
            if not project.exists():
                continue

            result["projects"][
                str(project)
            ] = {
                "vulnerability":
                    self.vulnerability(
                        project
                    ),
                "supply_chain":
                    self.supply_chain(
                        project
                    ),
            }

        self.evidence(
            "SOVEREIGN_DEFENSE_CYCLE",
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

    p_base = sub.add_parser(
        "baseline"
    )
    p_base.add_argument(
        "paths",
        nargs="+",
    )

    p_cycle = sub.add_parser(
        "cycle"
    )
    p_cycle.add_argument(
        "projects",
        nargs="*",
        default=["/root"],
    )

    p_quarantine = sub.add_parser(
        "quarantine"
    )
    p_quarantine.add_argument(
        "path"
    )
    p_quarantine.add_argument(
        "--reason",
        required=True,
    )

    args = parser.parse_args()
    app = Defense()

    if args.command == "baseline":
        print(json.dumps(
            app.baseline([
                pathlib.Path(path)
                for path in args.paths
            ]),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    if args.command == "cycle":
        print(json.dumps(
            app.cycle([
                pathlib.Path(path)
                for path in args.projects
            ]),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    if args.command == "quarantine":
        print(json.dumps(
            app.quarantine(
                pathlib.Path(
                    args.path
                ),
                args.reason,
            ),
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

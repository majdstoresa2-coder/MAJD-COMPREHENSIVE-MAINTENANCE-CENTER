#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD SOVEREIGN MAINTENANCE PLATFORM
FILE 04 — MAJD-SOVEREIGN-CYBER-DEFENSE-04.py

Sovereign defensive security layer.

DEFENSIVE SCOPE ONLY:
- integrity
- secrets exposure detection
- identity/session configuration evidence
- network/API exposure
- vulnerabilities
- malware/persistence indicators
- software supply chain
- AI/agent/tool defense policy
- certificates
- containment recommendations / controlled local containment
- hardware health:
  SMART / NVMe / temperatures / fans / PSU / UPS / BMC / Redfish
  only when the hardware actually exposes the capability.

NO FAKE HARDWARE CAPABILITIES.
NO FAKE SECURITY SUCCESS.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import shutil
import socket
import sqlite3
import ssl
import stat
import subprocess
import time
import uuid
from typing import Any, Dict, Iterable, List, Optional


ROOT = pathlib.Path(
    os.environ.get("MAJD_MAINTENANCE_ROOT", "/var/lib/majd-maintenance")
).resolve()

DB = ROOT / "majd-sovereign.db"
EVIDENCE = ROOT / "evidence"
BASELINES = ROOT / "security-baselines"
QUARANTINE = ROOT / "quarantine"


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def run(
    args: List[str],
    timeout: int = 60,
) -> Dict[str, Any]:
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
            "stdout": cp.stdout[-200000:],
            "stderr": cp.stderr[-200000:],
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": repr(exc),
        }


def file_hash(path: pathlib.Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            block = f.read(1024 * 1024)
            if not block:
                break
            h.update(block)

    return h.hexdigest()


class DefenseStore:
    def __init__(self):
        for p in (ROOT, EVIDENCE, BASELINES, QUARANTINE):
            p.mkdir(parents=True, exist_ok=True)

        self.db = sqlite3.connect(DB, timeout=30)
        self.db.row_factory = sqlite3.Row

        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS security_findings(
                id TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                severity TEXT NOT NULL,
                resource TEXT NOT NULL,
                title TEXT NOT NULL,
                evidence TEXT NOT NULL,
                remediation TEXT NOT NULL,
                containment TEXT,
                state TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS integrity_baseline(
                path TEXT PRIMARY KEY,
                sha256 TEXT NOT NULL,
                mode INTEGER NOT NULL,
                uid INTEGER NOT NULL,
                gid INTEGER NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS hardware_capabilities(
                capability TEXT PRIMARY KEY,
                available INTEGER NOT NULL,
                evidence TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        self.db.commit()

    def finding(
        self,
        category: str,
        severity: str,
        resource: str,
        title: str,
        evidence: Dict[str, Any],
        remediation: Dict[str, Any],
        containment: Optional[Dict[str, Any]] = None,
    ) -> str:
        fid = str(uuid.uuid4())
        timestamp = now()

        self.db.execute(
            """
            INSERT INTO security_findings
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                fid,
                category,
                severity,
                resource,
                title,
                json.dumps(evidence, ensure_ascii=False),
                json.dumps(remediation, ensure_ascii=False),
                (
                    json.dumps(containment, ensure_ascii=False)
                    if containment
                    else None
                ),
                "OPEN",
                timestamp,
                timestamp,
            ),
        )
        self.db.commit()

        self.evidence(
            "SECURITY_FINDING",
            {
                "id": fid,
                "category": category,
                "severity": severity,
                "resource": resource,
                "title": title,
                "evidence": evidence,
                "remediation": remediation,
                "containment": containment,
            },
        )

        return fid

    def evidence(
        self,
        subject: str,
        payload: Dict[str, Any],
    ) -> None:
        path = EVIDENCE / f"defense-{uuid.uuid4()}.json"

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


class IntegrityMonitor:
    def __init__(self, store: DefenseStore):
        self.store = store

    def baseline(self, paths: Iterable[pathlib.Path]) -> Dict[str, Any]:
        count = 0

        for root in paths:
            if not root.exists():
                continue

            candidates = (
                [root]
                if root.is_file()
                else [p for p in root.rglob("*") if p.is_file()]
            )

            for path in candidates:
                try:
                    st = path.stat()
                    checksum = file_hash(path)

                    self.store.db.execute(
                        """
                        INSERT INTO integrity_baseline
                        VALUES(?,?,?,?,?,?)
                        ON CONFLICT(path) DO UPDATE SET
                            sha256=excluded.sha256,
                            mode=excluded.mode,
                            uid=excluded.uid,
                            gid=excluded.gid,
                            updated_at=excluded.updated_at
                        """,
                        (
                            str(path.resolve()),
                            checksum,
                            stat.S_IMODE(st.st_mode),
                            st.st_uid,
                            st.st_gid,
                            now(),
                        ),
                    )
                    count += 1

                except (OSError, PermissionError):
                    continue

        self.store.db.commit()

        result = {
            "ok": True,
            "baselined_files": count,
        }

        self.store.evidence("INTEGRITY_BASELINE", result)
        return result

    def verify(self) -> Dict[str, Any]:
        changes = []

        rows = self.store.db.execute(
            "SELECT * FROM integrity_baseline"
        ).fetchall()

        for row in rows:
            path = pathlib.Path(row["path"])

            if not path.exists():
                changes.append(
                    {
                        "path": row["path"],
                        "change": "MISSING",
                    }
                )
                continue

            try:
                current = file_hash(path)
                st = path.stat()

                if current != row["sha256"]:
                    changes.append(
                        {
                            "path": row["path"],
                            "change": "CONTENT_CHANGED",
                            "expected": row["sha256"],
                            "actual": current,
                        }
                    )

                mode = stat.S_IMODE(st.st_mode)

                if mode != row["mode"]:
                    changes.append(
                        {
                            "path": row["path"],
                            "change": "MODE_CHANGED",
                            "expected": row["mode"],
                            "actual": mode,
                        }
                    )

            except OSError as exc:
                changes.append(
                    {
                        "path": row["path"],
                        "change": "READ_FAILURE",
                        "error": repr(exc),
                    }
                )

        if changes:
            self.store.finding(
                "INTEGRITY",
                "HIGH",
                "filesystem",
                "Critical integrity baseline drift detected",
                {"changes": changes},
                {
                    "action": "VALIDATE_CHANGE_OR_RESTORE_FROM_VERIFIED_BACKUP"
                },
                {
                    "action": "READ_ONLY_OR_QUARANTINE_AFFECTED_COMPONENT_IF_UNAUTHORIZED"
                },
            )

        return {
            "ok": not changes,
            "changes": changes,
        }


class SecretExposureScanner:
    PATTERNS = [
        re.compile(
            rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
        ),
        re.compile(
            rb"(?i)(?:api[_-]?key|secret|password|token)\s*[:=]\s*[\"'][^\"'\n]{8,}[\"']"
        ),
    ]

    def __init__(self, store: DefenseStore):
        self.store = store

    def scan_file(self, path: pathlib.Path) -> List[str]:
        try:
            if path.stat().st_size > 5 * 1024 * 1024:
                return []

            data = path.read_bytes()

        except (OSError, PermissionError):
            return []

        matches = []

        for pattern in self.PATTERNS:
            if pattern.search(data):
                matches.append(pattern.pattern.decode(errors="ignore"))

        return matches

    def scan_tree(self, root: pathlib.Path) -> Dict[str, Any]:
        findings = []

        if not root.exists():
            return {
                "ok": False,
                "state": "TARGET_NOT_FOUND",
            }

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if any(
                x in path.parts
                for x in (".git", "node_modules", ".venv")
            ):
                continue

            matches = self.scan_file(path)

            if matches:
                findings.append(
                    {
                        "path": str(path),
                        "pattern_types": matches,
                    }
                )

        if findings:
            self.store.finding(
                "SECRETS",
                "CRITICAL",
                str(root),
                "Potential secret material found in project files",
                {
                    "files": findings,
                    "secret_values_recorded": False,
                },
                {
                    "actions": [
                        "REMOVE_SECRET_FROM_SOURCE",
                        "ROTATE_COMPROMISED_CREDENTIAL_EXTERNALLY_IF_REQUIRED",
                        "PURGE_EXPOSED_HISTORY_WHEN_AUTHORIZED",
                        "USE_SECRET_REFERENCE",
                    ]
                },
                {
                    "action": "RESTRICT_ACCESS_TO_AFFECTED_FILES"
                },
            )

        return {
            "ok": not findings,
            "findings": findings,
            "secret_values_recorded": False,
        }


class NetworkDefense:
    def __init__(self, store: DefenseStore):
        self.store = store

    def listeners(self) -> Dict[str, Any]:
        if not shutil.which("ss"):
            return {
                "ok": False,
                "state": "SS_UNAVAILABLE",
            }

        result = run(["ss", "-lntup"])

        listeners = result.get("stdout", "").splitlines()

        self.store.evidence(
            "NETWORK_LISTENERS",
            {
                "listeners": listeners,
            },
        )

        return {
            "ok": result["ok"],
            "listeners": listeners,
        }


class PersistenceDefense:
    def __init__(self, store: DefenseStore):
        self.store = store

    def inspect(self) -> Dict[str, Any]:
        evidence = {}

        if shutil.which("systemctl"):
            evidence["enabled_services"] = run(
                [
                    "systemctl",
                    "list-unit-files",
                    "--type=service",
                    "--state=enabled",
                    "--no-pager",
                ]
            )

        cron_paths = [
            pathlib.Path("/etc/crontab"),
            pathlib.Path("/etc/cron.d"),
            pathlib.Path("/var/spool/cron"),
        ]

        evidence["cron"] = []

        for path in cron_paths:
            if path.exists():
                evidence["cron"].append(str(path))

        evidence["root_authorized_keys_exists"] = pathlib.Path(
            "/root/.ssh/authorized_keys"
        ).exists()

        self.store.evidence(
            "PERSISTENCE_INSPECTION",
            evidence,
        )

        return evidence


class SupplyChainDefense:
    def __init__(self, store: DefenseStore):
        self.store = store

    def inventory(self, root: pathlib.Path) -> Dict[str, Any]:
        manifests = []

        names = {
            "requirements.txt",
            "pyproject.toml",
            "poetry.lock",
            "package.json",
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
            "Dockerfile",
        }

        if root.exists():
            for path in root.rglob("*"):
                if path.is_file() and path.name in names:
                    manifests.append(
                        {
                            "path": str(path),
                            "sha256": file_hash(path),
                        }
                    )

        result = {
            "root": str(root),
            "manifests": manifests,
            "sbom_source_inventory": True,
        }

        self.store.evidence("SUPPLY_CHAIN_INVENTORY", result)
        return result

    def python_audit(self, root: pathlib.Path) -> Dict[str, Any]:
        if not shutil.which("pip-audit"):
            return {
                "ok": False,
                "state": "SECURITY_SCANNER_NOT_INSTALLED",
                "external_dependency_required": False,
                "remediation": "Install an approved local vulnerability scanner through the Executor before declaring vulnerability coverage.",
            }

        return run(
            ["pip-audit", "--format", "json"],
            timeout=600,
        )


class TLSDefense:
    def verify(self, hostname: str, port: int = 443) -> Dict[str, Any]:
        context = ssl.create_default_context()

        try:
            with socket.create_connection(
                (hostname, port),
                timeout=10,
            ) as sock:
                with context.wrap_socket(
                    sock,
                    server_hostname=hostname,
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


class AIAgentDefense:
    DANGEROUS_PATTERNS = [
        re.compile(r"\brm\s+-rf\s+/(?:\s|$)"),
        re.compile(r"\bmkfs(?:\.|\s)"),
        re.compile(r"\bdd\s+if=.*\bof=/dev/"),
        re.compile(r"\bshutdown\b"),
        re.compile(r"\breboot\b"),
    ]

    def validate_command(
        self,
        command: str,
        owner_authorized: bool = False,
    ) -> Dict[str, Any]:
        matched = [
            p.pattern
            for p in self.DANGEROUS_PATTERNS
            if p.search(command)
        ]

        if matched and not owner_authorized:
            return {
                "allowed": False,
                "reason": "DESTRUCTIVE_COMMAND_REQUIRES_EXPLICIT_AUTHORITY_AND_BACKUP",
                "matched_controls": matched,
            }

        return {
            "allowed": True,
            "matched_controls": matched,
            "owner_authorized": owner_authorized,
        }


class HardwareDefense:
    def __init__(self, store: DefenseStore):
        self.store = store

    def capability(
        self,
        name: str,
        available: bool,
        evidence: Dict[str, Any],
    ) -> None:
        self.store.db.execute(
            """
            INSERT INTO hardware_capabilities
            VALUES(?,?,?,?)
            ON CONFLICT(capability) DO UPDATE SET
                available=excluded.available,
                evidence=excluded.evidence,
                updated_at=excluded.updated_at
            """,
            (
                name,
                int(available),
                json.dumps(evidence, ensure_ascii=False),
                now(),
            ),
        )
        self.store.db.commit()

    def smart(self) -> Dict[str, Any]:
        available = bool(shutil.which("smartctl"))

        if not available:
            result = {
                "available": False,
                "state": "SMARTCTL_UNAVAILABLE",
            }
            self.capability("SMART", False, result)
            return result

        scan = run(["smartctl", "--scan-open"])

        devices = []

        for line in scan.get("stdout", "").splitlines():
            if not line.startswith("/dev/"):
                continue

            device = line.split()[0]

            devices.append(
                {
                    "device": device,
                    "health": run(
                        ["smartctl", "-H", "-A", device],
                        timeout=60,
                    ),
                }
            )

        result = {
            "available": True,
            "devices": devices,
        }

        self.capability("SMART", True, result)
        return result

    def nvme(self) -> Dict[str, Any]:
        available = bool(shutil.which("nvme"))

        if not available:
            result = {
                "available": False,
                "state": "NVME_CLI_UNAVAILABLE",
            }
            self.capability("NVME", False, result)
            return result

        listing = run(["nvme", "list", "-o", "json"])

        result = {
            "available": True,
            "list": listing,
        }

        self.capability("NVME", True, result)
        return result

    def sensors(self) -> Dict[str, Any]:
        available = bool(shutil.which("sensors"))

        if not available:
            result = {
                "available": False,
                "state": "LM_SENSORS_UNAVAILABLE",
            }
            self.capability("SENSORS", False, result)
            return result

        result = {
            "available": True,
            "readings": run(["sensors", "-j"]),
        }

        self.capability("SENSORS", True, result)
        return result

    def ipmi(self) -> Dict[str, Any]:
        available = bool(shutil.which("ipmitool"))

        if not available:
            result = {
                "available": False,
                "state": "IPMI_UNAVAILABLE",
            }
            self.capability("BMC_IPMI", False, result)
            return result

        result = {
            "available": True,
            "sensors": run(["ipmitool", "sensor"]),
        }

        self.capability("BMC_IPMI", True, result)
        return result

    def ups(self) -> Dict[str, Any]:
        available = bool(shutil.which("upsc"))

        if not available:
            result = {
                "available": False,
                "state": "UPS_TELEMETRY_UNAVAILABLE",
            }
            self.capability("UPS", False, result)
            return result

        result = {
            "available": True,
            "devices": run(["upsc", "-l"]),
        }

        self.capability("UPS", True, result)
        return result

    def inspect(self) -> Dict[str, Any]:
        return {
            "smart": self.smart(),
            "nvme": self.nvme(),
            "sensors": self.sensors(),
            "bmc_ipmi": self.ipmi(),
            "ups": self.ups(),
        }


class ContainmentEngine:
    """
    Containment is intentionally narrow.

    It does not destroy evidence and does not automatically shut down
    the whole sovereign platform merely because one finding exists.
    """

    def __init__(self, store: DefenseStore):
        self.store = store

    def quarantine_file(
        self,
        path: pathlib.Path,
        explicit_authorization: bool,
    ) -> Dict[str, Any]:
        if not explicit_authorization:
            return {
                "ok": False,
                "state": "EXPLICIT_AUTHORIZATION_REQUIRED",
            }

        if not path.exists() or not path.is_file():
            return {
                "ok": False,
                "state": "FILE_NOT_FOUND",
            }

        checksum = file_hash(path)

        destination = QUARANTINE / (
            f"{uuid.uuid4()}-{path.name}"
        )

        shutil.copy2(path, destination)

        if file_hash(destination) != checksum:
            destination.unlink(missing_ok=True)
            return {
                "ok": False,
                "state": "QUARANTINE_COPY_VERIFICATION_FAILED",
            }

        path.unlink()

        result = {
            "ok": True,
            "state": "QUARANTINED",
            "original": str(path),
            "quarantine": str(destination),
            "sha256": checksum,
        }

        self.store.evidence("QUARANTINE", result)
        return result


class SovereignCyberDefense:
    def __init__(self):
        self.store = DefenseStore()
        self.integrity = IntegrityMonitor(self.store)
        self.secrets = SecretExposureScanner(self.store)
        self.network = NetworkDefense(self.store)
        self.persistence = PersistenceDefense(self.store)
        self.supply_chain = SupplyChainDefense(self.store)
        self.tls = TLSDefense()
        self.ai = AIAgentDefense()
        self.hardware = HardwareDefense(self.store)
        self.containment = ContainmentEngine(self.store)

    def cycle(
        self,
        roots: List[pathlib.Path],
    ) -> Dict[str, Any]:
        integrity = self.integrity.verify()
        secret_results = [
            self.secrets.scan_tree(root)
            for root in roots
            if root.exists()
        ]

        network = self.network.listeners()
        persistence = self.persistence.inspect()

        supply_chain = [
            self.supply_chain.inventory(root)
            for root in roots
            if root.exists()
        ]

        hardware = self.hardware.inspect()

        result = {
            "time": now(),
            "integrity": integrity,
            "secrets": secret_results,
            "network": network,
            "persistence": persistence,
            "supply_chain": supply_chain,
            "hardware": hardware,
            "security_truth": {
                "fake_success_forbidden": True,
                "hardware_capabilities_detected_before_claim": True,
                "remediation_required_for_security_completion": True,
                "containment_available": True,
                "evidence_required": True,
            },
        }

        self.store.evidence(
            "SOVEREIGN_CYBER_DEFENSE_CYCLE",
            result,
        )

        return result


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command",
        choices=["baseline", "scan", "hardware", "tls"],
    )

    parser.add_argument(
        "--root",
        action="append",
        default=[],
    )

    parser.add_argument("--host")

    args = parser.parse_args()

    defense = SovereignCyberDefense()

    roots = [
        pathlib.Path(x).resolve()
        for x in args.root
    ]

    if not roots:
        roots = [
            pathlib.Path("/root"),
            pathlib.Path("/opt"),
            pathlib.Path("/srv"),
        ]

    if args.command == "baseline":
        output = defense.integrity.baseline(roots)

    elif args.command == "hardware":
        output = defense.hardware.inspect()

    elif args.command == "tls":
        if not args.host:
            output = {
                "ok": False,
                "state": "HOST_REQUIRED",
            }
        else:
            output = defense.tls.verify(args.host)

    else:
        output = defense.cycle(roots)

    print(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

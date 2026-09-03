#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MAJD SOVEREIGN MAINTENANCE PLATFORM
FILE 01 — MAJD-MAINTENANCE-MASTERMIND-01.py

SUPREME OWNER:
    SUPREME_OWNER

MISSION:
    Sovereign discovery, understanding, knowledge graph, digital twin,
    constitutions, policy-as-code, regulatory/compliance intelligence,
    privacy/data governance, AI governance, architecture reasoning,
    risk/impact analysis and execution decision generation.

FILES:
    01 Mastermind
    02 Executor
    03 Runtime
    04 Sovereign Cyber Defense

NO FILE 05.

EXECUTION LAW:
OBSERVE
→ PREDICT/PREVENT
→ DETECT
→ CORRELATE
→ DIAGNOSE
→ DECIDE
→ BACKUP
→ REPAIR/WRITE REAL CODE
→ BUILD/CONFIGURE
→ REAL EXECUTION
→ INDEPENDENT VERIFY
→ DEPLOY/LAUNCH
→ MONITOR
→ PROTECT
→ LEARN
→ IMPROVE
→ REPEAT

NO FAKE SUCCESS.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import json
import os
import pathlib
import platform
import re
import shutil
import socket
import sqlite3
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Tuple


VERSION = "1.0.0"
OWNER = "SUPREME_OWNER"

ROOT = pathlib.Path(
    os.environ.get("MAJD_MAINTENANCE_ROOT", "/var/lib/majd-maintenance")
).resolve()

DB_PATH = ROOT / "majd-sovereign.db"
EVIDENCE = ROOT / "evidence"
SNAPSHOTS = ROOT / "snapshots"
PLANS = ROOT / "plans"

FILES = {
    "01": "MAJD-MAINTENANCE-MASTERMIND-01.py",
    "02": "MAJD-MAINTENANCE-EXECUTOR-02.py",
    "03": "MAJD-MAINTENANCE-RUNTIME-03.py",
    "04": "MAJD-SOVEREIGN-CYBER-DEFENSE-04.py",
}

EXECUTION_PATH = (
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


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    if not isinstance(value, (bytes, bytearray)):
        value = stable_json(value).encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def ensure_dirs() -> None:
    for p in (ROOT, EVIDENCE, SNAPSHOTS, PLANS):
        p.mkdir(parents=True, exist_ok=True)


def run(
    command: List[str],
    timeout: int = 30,
    cwd: Optional[pathlib.Path] = None,
) -> Dict[str, Any]:
    started = time.monotonic()
    try:
        cp = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "command": command,
            "returncode": cp.returncode,
            "stdout": cp.stdout[-100000:],
            "stderr": cp.stderr[-100000:],
            "duration": round(time.monotonic() - started, 4),
            "ok": cp.returncode == 0,
        }
    except Exception as exc:
        return {
            "command": command,
            "returncode": None,
            "stdout": "",
            "stderr": repr(exc),
            "duration": round(time.monotonic() - started, 4),
            "ok": False,
        }


class Store:
    def __init__(self, path: pathlib.Path = DB_PATH):
        ensure_dirs()
        self.db = sqlite3.connect(path, timeout=30)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA foreign_keys=ON")
        self._schema()

    def _schema(self) -> None:
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS resources(
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                name TEXT NOT NULL,
                locator TEXT,
                state TEXT NOT NULL,
                criticality TEXT NOT NULL,
                metadata TEXT NOT NULL,
                discovered_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_resource_unique
            ON resources(kind,name,locator);

            CREATE TABLE IF NOT EXISTS relations(
                source_id TEXT NOT NULL,
                relation TEXT NOT NULL,
                target_id TEXT NOT NULL,
                metadata TEXT NOT NULL,
                PRIMARY KEY(source_id,relation,target_id)
            );

            CREATE TABLE IF NOT EXISTS policies(
                id TEXT PRIMARY KEY,
                scope TEXT NOT NULL,
                name TEXT NOT NULL,
                version INTEGER NOT NULL,
                mode TEXT NOT NULL,
                rule TEXT NOT NULL,
                enabled INTEGER NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS findings(
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                category TEXT NOT NULL,
                severity TEXT NOT NULL,
                resource_id TEXT,
                title TEXT NOT NULL,
                evidence TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS decisions(
                id TEXT PRIMARY KEY,
                finding_id TEXT,
                action TEXT NOT NULL,
                risk TEXT NOT NULL,
                requires_owner INTEGER NOT NULL,
                external_dependency TEXT,
                payload TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS evidence(
                id TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                subject TEXT NOT NULL,
                sha256 TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS regulatory_rules(
                id TEXT PRIMARY KEY,
                jurisdiction TEXT NOT NULL,
                subject TEXT NOT NULL,
                source TEXT,
                effective_from TEXT,
                deadline TEXT,
                applicability TEXT NOT NULL,
                requirements TEXT NOT NULL,
                last_verified TEXT
            );

            CREATE TABLE IF NOT EXISTS data_assets(
                id TEXT PRIMARY KEY,
                resource_id TEXT,
                name TEXT NOT NULL,
                classification TEXT NOT NULL,
                purpose TEXT,
                lawful_basis TEXT,
                retention TEXT,
                residency TEXT,
                cross_border INTEGER NOT NULL,
                metadata TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ai_assets(
                id TEXT PRIMARY KEY,
                resource_id TEXT,
                name TEXT NOT NULL,
                provider TEXT,
                model TEXT,
                tools TEXT NOT NULL,
                permissions TEXT NOT NULL,
                provenance TEXT,
                risk TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS knowledge(
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS incidents(
                id TEXT PRIMARY KEY,
                severity TEXT NOT NULL,
                state TEXT NOT NULL,
                summary TEXT NOT NULL,
                timeline TEXT NOT NULL,
                root_cause TEXT,
                remediation TEXT,
                verification TEXT,
                opened_at TEXT NOT NULL,
                closed_at TEXT
            );
            """
        )
        self.db.commit()

    def evidence(self, category: str, subject: str, payload: Any) -> str:
        eid = str(uuid.uuid4())
        raw = stable_json(payload)
        self.db.execute(
            "INSERT INTO evidence VALUES(?,?,?,?,?,?)",
            (eid, category, subject, digest(raw.encode()), raw, utcnow()),
        )
        self.db.commit()

        target = EVIDENCE / f"{eid}.json"
        target.write_text(
            stable_json(
                {
                    "id": eid,
                    "category": category,
                    "subject": subject,
                    "sha256": digest(raw.encode()),
                    "created_at": utcnow(),
                    "payload": payload,
                }
            ),
            encoding="utf-8",
        )
        return eid

    def upsert_resource(
        self,
        kind: str,
        name: str,
        locator: str,
        state: str,
        criticality: str,
        metadata: Dict[str, Any],
    ) -> str:
        row = self.db.execute(
            "SELECT id FROM resources WHERE kind=? AND name=? AND locator=?",
            (kind, name, locator),
        ).fetchone()
        now = utcnow()

        if row:
            rid = row["id"]
            self.db.execute(
                """
                UPDATE resources
                SET state=?,criticality=?,metadata=?,updated_at=?
                WHERE id=?
                """,
                (state, criticality, stable_json(metadata), now, rid),
            )
        else:
            rid = str(uuid.uuid4())
            self.db.execute(
                "INSERT INTO resources VALUES(?,?,?,?,?,?,?,?,?)",
                (
                    rid,
                    kind,
                    name,
                    locator,
                    state,
                    criticality,
                    stable_json(metadata),
                    now,
                    now,
                ),
            )
        self.db.commit()
        return rid

    def finding(
        self,
        source: str,
        category: str,
        severity: str,
        resource_id: Optional[str],
        title: str,
        evidence: Dict[str, Any],
    ) -> str:
        fid = str(uuid.uuid4())
        now = utcnow()
        self.db.execute(
            "INSERT INTO findings VALUES(?,?,?,?,?,?,?,?,?,?)",
            (
                fid,
                source,
                category,
                severity,
                resource_id,
                title,
                stable_json(evidence),
                "OPEN",
                now,
                now,
            ),
        )
        self.db.commit()
        self.evidence(category, title, evidence)
        return fid

    def decision(
        self,
        finding_id: Optional[str],
        action: str,
        risk: str,
        payload: Dict[str, Any],
        requires_owner: bool = False,
        external_dependency: Optional[str] = None,
    ) -> str:
        did = str(uuid.uuid4())
        status = (
            "EXTERNAL_DEPENDENCY_REQUIRED"
            if external_dependency
            else "OWNER_APPROVAL_REQUIRED"
            if requires_owner
            else "READY"
        )
        self.db.execute(
            "INSERT INTO decisions VALUES(?,?,?,?,?,?,?,?,?)",
            (
                did,
                finding_id,
                action,
                risk,
                int(requires_owner),
                external_dependency,
                stable_json(payload),
                status,
                utcnow(),
            ),
        )
        self.db.commit()
        return did

    def set_knowledge(self, key: str, value: Any) -> None:
        self.db.execute(
            """
            INSERT INTO knowledge(key,value,updated_at) VALUES(?,?,?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value,
                                           updated_at=excluded.updated_at
            """,
            (key, stable_json(value), utcnow()),
        )
        self.db.commit()


class DiscoveryEngine:
    def __init__(self, store: Store):
        self.store = store

    def filesystem(self, roots: Iterable[str]) -> List[str]:
        discovered = []
        signatures = {
            ".git": "git_repository",
            "package.json": "node_project",
            "pyproject.toml": "python_project",
            "requirements.txt": "python_project",
            "docker-compose.yml": "container_stack",
            "compose.yaml": "container_stack",
        }

        for root_raw in roots:
            root = pathlib.Path(root_raw).expanduser()
            if not root.exists():
                continue

            for base, dirs, files in os.walk(root):
                base_path = pathlib.Path(base)

                if any(
                    x in base_path.parts
                    for x in (".cache", "node_modules", ".venv", "__pycache__")
                ):
                    dirs[:] = []
                    continue

                names = set(dirs) | set(files)
                for marker, kind in signatures.items():
                    if marker not in names:
                        continue

                    rid = self.store.upsert_resource(
                        kind,
                        base_path.name,
                        str(base_path.resolve()),
                        "DISCOVERED",
                        "UNKNOWN",
                        {
                            "marker": marker,
                            "path": str(base_path.resolve()),
                        },
                    )
                    discovered.append(rid)
                    break

        return discovered

    def systemd(self) -> List[str]:
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

        found = []
        for line in result["stdout"].splitlines():
            parts = line.split()
            if not parts:
                continue
            name = parts[0]
            active = parts[2] if len(parts) > 2 else "unknown"
            sub = parts[3] if len(parts) > 3 else "unknown"
            rid = self.store.upsert_resource(
                "systemd_service",
                name,
                name,
                f"{active}/{sub}",
                "UNKNOWN",
                {"raw": line},
            )
            found.append(rid)
        return found

    def network(self) -> List[str]:
        result = run(["ss", "-lntup"]) if shutil.which("ss") else {"stdout": ""}
        rid = self.store.upsert_resource(
            "network_surface",
            socket.gethostname(),
            socket.gethostname(),
            "DISCOVERED",
            "HIGH",
            {"listeners": result["stdout"].splitlines()},
        )
        return [rid]

    def host(self) -> str:
        disk = shutil.disk_usage("/")
        metadata = {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "python": sys.version,
            "cpu_count": os.cpu_count(),
            "disk_total": disk.total,
            "disk_used": disk.used,
            "disk_free": disk.free,
        }
        return self.store.upsert_resource(
            "host",
            socket.gethostname(),
            "/",
            "ACTIVE",
            "CRITICAL",
            metadata,
        )

    def discover(self, roots: Iterable[str]) -> Dict[str, Any]:
        result = {
            "host": self.host(),
            "filesystem": self.filesystem(roots),
            "systemd": self.systemd(),
            "network": self.network(),
            "time": utcnow(),
        }
        self.store.evidence("DISCOVERY", "sovereign-discovery", result)
        return result


class KnowledgeGraph:
    def __init__(self, store: Store):
        self.store = store

    def rebuild(self) -> Dict[str, Any]:
        resources = self.store.db.execute("SELECT * FROM resources").fetchall()
        nodes = []
        edges = []

        for row in resources:
            node = dict(row)
            node["metadata"] = json.loads(node["metadata"])
            nodes.append(node)

        by_locator = {
            r["locator"]: r
            for r in nodes
            if r.get("locator")
        }

        for resource in nodes:
            locator = resource.get("locator") or ""
            if not locator.startswith("/"):
                continue

            path = pathlib.Path(locator)
            for parent in path.parents:
                candidate = by_locator.get(str(parent))
                if candidate:
                    edge = {
                        "source": resource["id"],
                        "relation": "DEPENDS_ON_PARENT",
                        "target": candidate["id"],
                    }
                    edges.append(edge)
                    self.store.db.execute(
                        """
                        INSERT OR IGNORE INTO relations
                        VALUES(?,?,?,?)
                        """,
                        (
                            edge["source"],
                            edge["relation"],
                            edge["target"],
                            "{}",
                        ),
                    )
                    break

        self.store.db.commit()

        graph = {
            "generated_at": utcnow(),
            "nodes": nodes,
            "edges": edges,
            "hash": digest({"nodes": nodes, "edges": edges}),
        }
        self.store.set_knowledge("knowledge_graph", graph)
        self.store.evidence("KNOWLEDGE_GRAPH", "global", graph)
        return graph


class DigitalTwin:
    def __init__(self, store: Store):
        self.store = store

    def build(self) -> Dict[str, Any]:
        resources = [
            dict(r)
            for r in self.store.db.execute(
                "SELECT * FROM resources ORDER BY kind,name"
            )
        ]

        findings = [
            dict(r)
            for r in self.store.db.execute(
                "SELECT * FROM findings WHERE status='OPEN'"
            )
        ]

        twin = {
            "generated_at": utcnow(),
            "owner": OWNER,
            "version": VERSION,
            "resources": resources,
            "open_findings": findings,
            "execution_path": EXECUTION_PATH,
            "state_hash": digest(
                {
                    "resources": resources,
                    "findings": findings,
                }
            ),
        }

        self.store.set_knowledge("digital_twin", twin)
        self.store.evidence("DIGITAL_TWIN", "global", twin)
        return twin


GLOBAL_CONSTITUTION = {
    "supreme_authority": OWNER,
    "no_fake_success": True,
    "backup_before_destructive_change": True,
    "independent_verification_required": True,
    "critical_workflow_verification_required_for_launch": True,
    "external_credentials_cannot_be_invented": True,
    "secrets_must_not_enter_logs_or_evidence": True,
    "least_privilege": True,
    "zero_trust": True,
    "rollback_required_for_high_risk_change": True,
    "evidence_required": True,
    "file_numbers": ["01", "02", "03", "04"],
    "file_05_forbidden": True,
}


class ConstitutionEngine:
    def __init__(self, store: Store):
        self.store = store

    def install(self) -> None:
        self.store.set_knowledge("global_constitution", GLOBAL_CONSTITUTION)

    def platform_constitution(self, resource: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "resource_id": resource["id"],
            "resource_kind": resource["kind"],
            "owner": OWNER,
            "production_truth_required": True,
            "backup_before_destructive_change": True,
            "independent_verification": True,
            "critical_workflows_required": True,
            "secrets": "REFERENCE_ONLY",
            "owner_gate": [
                "LEGAL_SIGNATURE",
                "IDENTITY_VERIFICATION",
                "EXTERNAL_ACCOUNT_CREATION",
                "NON_DELEGABLE_APPROVAL",
            ],
        }


class PolicyEngine:
    def __init__(self, store: Store):
        self.store = store

    def seed(self) -> None:
        rules = [
            (
                "GLOBAL",
                "NO_FAKE_SUCCESS",
                "ENFORCE",
                {"require_evidence": True},
            ),
            (
                "GLOBAL",
                "BACKUP_BEFORE_DESTRUCTIVE_CHANGE",
                "ENFORCE",
                {"backup_required": True},
            ),
            (
                "GLOBAL",
                "INDEPENDENT_VERIFY",
                "ENFORCE",
                {"required": True},
            ),
            (
                "GLOBAL",
                "CRITICAL_WORKFLOW_BEFORE_LAUNCH",
                "ENFORCE",
                {"required": True},
            ),
            (
                "GLOBAL",
                "NO_SECRET_LOGGING",
                "ENFORCE",
                {"redaction_required": True},
            ),
        ]

        for scope, name, mode, rule in rules:
            pid = digest([scope, name])
            self.store.db.execute(
                """
                INSERT INTO policies
                VALUES(?,?,?,?,?,?,?,?)
                ON CONFLICT(id) DO UPDATE SET
                    version=excluded.version,
                    mode=excluded.mode,
                    rule=excluded.rule,
                    enabled=excluded.enabled,
                    updated_at=excluded.updated_at
                """,
                (
                    pid,
                    scope,
                    name,
                    1,
                    mode,
                    stable_json(rule),
                    1,
                    utcnow(),
                ),
            )
        self.store.db.commit()

    def evaluate(self, action: Dict[str, Any]) -> Dict[str, Any]:
        violations = []

        if action.get("destructive") and not action.get("backup"):
            violations.append("BACKUP_REQUIRED")

        if action.get("launch") and not action.get("critical_workflow_verification"):
            violations.append("CRITICAL_WORKFLOW_VERIFICATION_REQUIRED")

        if action.get("declared_success") and not action.get("independent_verification"):
            violations.append("INDEPENDENT_VERIFICATION_REQUIRED")

        if action.get("contains_secret"):
            violations.append("SECRET_MUST_NOT_BE_LOGGED")

        return {
            "allowed": not violations,
            "violations": violations,
            "evaluated_at": utcnow(),
        }


class RegulatoryEngine:
    """
    Regulatory truth is evidence-driven.

    This engine does not invent legal requirements.
    A rule becomes enforceable only after a source and applicability
    record have been stored.
    """

    def __init__(self, store: Store):
        self.store = store

    def register_rule(
        self,
        jurisdiction: str,
        subject: str,
        source: str,
        requirements: Dict[str, Any],
        applicability: Dict[str, Any],
        effective_from: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> str:
        rid = digest(
            [
                jurisdiction,
                subject,
                source,
                effective_from,
                deadline,
                requirements,
            ]
        )

        self.store.db.execute(
            """
            INSERT OR REPLACE INTO regulatory_rules
            VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (
                rid,
                jurisdiction,
                subject,
                source,
                effective_from,
                deadline,
                stable_json(applicability),
                stable_json(requirements),
                utcnow(),
            ),
        )
        self.store.db.commit()
        return rid

    def deadlines(self, days: int = 90) -> List[Dict[str, Any]]:
        now = dt.datetime.now(dt.timezone.utc)
        limit = now + dt.timedelta(days=days)
        output = []

        for row in self.store.db.execute(
            "SELECT * FROM regulatory_rules WHERE deadline IS NOT NULL"
        ):
            try:
                deadline = dt.datetime.fromisoformat(row["deadline"])
                if deadline.tzinfo is None:
                    deadline = deadline.replace(tzinfo=dt.timezone.utc)
                if now <= deadline <= limit:
                    output.append(dict(row))
            except ValueError:
                continue

        return output

    def evidence_matrix(self) -> Dict[str, Any]:
        rules = [
            dict(r)
            for r in self.store.db.execute(
                "SELECT * FROM regulatory_rules"
            )
        ]

        evidence = [
            dict(r)
            for r in self.store.db.execute(
                "SELECT id,category,subject,sha256,created_at FROM evidence"
            )
        ]

        matrix = {
            "generated_at": utcnow(),
            "rules": rules,
            "evidence": evidence,
        }

        self.store.evidence(
            "COMPLIANCE_EVIDENCE_MATRIX",
            "global",
            matrix,
        )
        return matrix


class DataGovernance:
    SECRET_PATTERN = re.compile(
        r"(password|passwd|secret|token|api[_-]?key|private[_-]?key)",
        re.I,
    )

    def __init__(self, store: Store):
        self.store = store

    def inspect_environment_names(self) -> Dict[str, Any]:
        names = sorted(os.environ.keys())
        sensitive = [
            name
            for name in names
            if self.SECRET_PATTERN.search(name)
        ]

        result = {
            "environment_variable_count": len(names),
            "sensitive_variable_names": sensitive,
            "values_collected": False,
        }

        self.store.evidence(
            "DATA_GOVERNANCE",
            "environment-secret-reference-inventory",
            result,
        )
        return result


class AIGovernance:
    def __init__(self, store: Store):
        self.store = store

    def inventory_local_models(self) -> List[Dict[str, Any]]:
        models = []

        if shutil.which("ollama"):
            result = run(["ollama", "list"])
            for line in result["stdout"].splitlines()[1:]:
                parts = line.split()
                if parts:
                    models.append(
                        {
                            "provider": "ollama",
                            "model": parts[0],
                            "source": "local-runtime",
                        }
                    )

        self.store.set_knowledge("ai_bom", models)
        self.store.evidence("AI_BOM", "local-models", models)
        return models


class RiskEngine:
    WEIGHTS = {
        "INFO": 1,
        "LOW": 2,
        "MEDIUM": 4,
        "HIGH": 7,
        "CRITICAL": 10,
    }

    def score(
        self,
        severity: str,
        criticality: str,
        blast_radius: int,
        data_risk: int,
        security_risk: int,
    ) -> int:
        base = self.WEIGHTS.get(severity.upper(), 4)
        critical = 5 if criticality.upper() == "CRITICAL" else 0
        return min(
            100,
            base * 5
            + critical
            + min(blast_radius, 20)
            + min(data_risk, 20)
            + min(security_risk, 20),
        )


class DecisionEngine:
    def __init__(self, store: Store):
        self.store = store
        self.policy = PolicyEngine(store)

    def generate(self) -> List[str]:
        decisions = []

        findings = self.store.db.execute(
            "SELECT * FROM findings WHERE status='OPEN'"
        ).fetchall()

        for finding in findings:
            evidence = json.loads(finding["evidence"])
            action = {
                "finding_id": finding["id"],
                "category": finding["category"],
                "severity": finding["severity"],
                "backup": True,
                "independent_verification": True,
                "critical_workflow_verification": True,
                "destructive": False,
            }

            policy_result = self.policy.evaluate(action)

            if not policy_result["allowed"]:
                continue

            did = self.store.decision(
                finding_id=finding["id"],
                action="REMEDIATE_AND_VERIFY",
                risk=finding["severity"],
                payload={
                    "finding": dict(finding),
                    "evidence": evidence,
                    "required_execution_path": EXECUTION_PATH,
                    "policy_result": policy_result,
                },
            )
            decisions.append(did)

        return decisions


class ProductCompleteness:
    def __init__(self, store: Store):
        self.store = store

    def inspect_repository(self, path: pathlib.Path) -> Dict[str, Any]:
        indicators = {
            "frontend": False,
            "api": False,
            "tests": False,
            "deployment": False,
            "database": False,
            "localization": False,
            "accessibility_signals": False,
        }

        if not path.exists():
            return indicators

        for base, dirs, files in os.walk(path):
            p = pathlib.Path(base)
            if ".git" in p.parts or "node_modules" in p.parts:
                continue

            lower_files = [x.lower() for x in files]

            if any(x in lower_files for x in ("package.json", "vite.config.js")):
                indicators["frontend"] = True

            if any(
                x.endswith(".py") or x.endswith(".js")
                for x in lower_files
            ):
                indicators["api"] = True

            if any("test" in x for x in lower_files):
                indicators["tests"] = True

            if any(
                x in lower_files
                for x in (
                    "dockerfile",
                    "docker-compose.yml",
                    "railway.json",
                )
            ):
                indicators["deployment"] = True

            if any(
                x.endswith((".sqlite", ".db", ".sql"))
                for x in lower_files
            ):
                indicators["database"] = True

            if any(
                x in lower_files
                for x in ("ar.json", "en.json", "i18n.json")
            ):
                indicators["localization"] = True

        return indicators


class Mastermind:
    def __init__(self):
        self.store = Store()
        self.discovery = DiscoveryEngine(self.store)
        self.graph = KnowledgeGraph(self.store)
        self.twin = DigitalTwin(self.store)
        self.constitution = ConstitutionEngine(self.store)
        self.policy = PolicyEngine(self.store)
        self.regulatory = RegulatoryEngine(self.store)
        self.data = DataGovernance(self.store)
        self.ai = AIGovernance(self.store)
        self.decisions = DecisionEngine(self.store)

    def bootstrap(self) -> Dict[str, Any]:
        ensure_dirs()
        self.constitution.install()
        self.policy.seed()

        result = {
            "owner": OWNER,
            "version": VERSION,
            "files": FILES,
            "execution_path": EXECUTION_PATH,
            "root": str(ROOT),
            "database": str(DB_PATH),
            "bootstrapped_at": utcnow(),
        }

        self.store.evidence("BOOTSTRAP", "mastermind", result)
        return result

    def cycle(self, roots: List[str]) -> Dict[str, Any]:
        discovery = self.discovery.discover(roots)
        graph = self.graph.rebuild()
        twin = self.twin.build()
        data = self.data.inspect_environment_names()
        ai = self.ai.inventory_local_models()
        deadlines = self.regulatory.deadlines()
        matrix = self.regulatory.evidence_matrix()
        decisions = self.decisions.generate()

        result = {
            "status": "CYCLE_COMPLETED_WITH_EVIDENCE",
            "time": utcnow(),
            "discovery": discovery,
            "knowledge_graph_hash": graph["hash"],
            "digital_twin_hash": twin["state_hash"],
            "data_governance": data,
            "ai_bom": ai,
            "regulatory_deadlines": deadlines,
            "evidence_matrix_rules": len(matrix["rules"]),
            "decisions": decisions,
        }

        self.store.evidence("MASTERMIND_CYCLE", "global", result)
        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["bootstrap", "discover", "cycle", "twin", "decide"],
    )
    parser.add_argument(
        "--roots",
        nargs="*",
        default=["/root", "/opt", "/srv"],
    )
    args = parser.parse_args()

    mastermind = Mastermind()

    if args.command == "bootstrap":
        output = mastermind.bootstrap()

    elif args.command == "discover":
        mastermind.bootstrap()
        output = mastermind.discovery.discover(args.roots)

    elif args.command == "twin":
        mastermind.bootstrap()
        mastermind.discovery.discover(args.roots)
        mastermind.graph.rebuild()
        output = mastermind.twin.build()

    elif args.command == "decide":
        mastermind.bootstrap()
        output = {"decisions": mastermind.decisions.generate()}

    else:
        mastermind.bootstrap()
        output = mastermind.cycle(args.roots)

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

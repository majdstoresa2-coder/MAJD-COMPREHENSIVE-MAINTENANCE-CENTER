#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
======================================================================
MAJD COMPREHENSIVE MAINTENANCE CENTER
MAJD-MAINTENANCE-MASTERMIND-01.py
======================================================================

FILE 01 — SOVEREIGN GLOBAL MAINTENANCE MASTERMIND

PURPOSE
-------
The sovereign central intelligence, governance, discovery, policy,
regulatory-intelligence, architecture, planning and decision engine for
the MAJD Comprehensive Maintenance Center.

This file DOES NOT pretend that an action was executed merely because
it was planned.

Real execution is delegated to:
    02 — MAJD-MAINTENANCE-EXECUTOR-02.py

Continuous runtime / watchtower:
    03 — MAJD-MAINTENANCE-RUNTIME-03.py

Sovereign cyber defense:
    04 — MAJD-SOVEREIGN-CYBER-DEFENSE-04.py

ABSOLUTE AUTHORITY
------------------
SUPREME_OWNER

CORE PRINCIPLES
---------------
1. OWNER remains the highest authority.
2. No fake success.
3. No mock operational status.
4. Observed != Verified.
5. Verified != Evidenced unless evidence exists.
6. Laws/regulations are applied only after applicability analysis.
7. Legal ambiguity is marked LEGAL_REVIEW_REQUIRED.
8. Official sources have priority.
9. New technology is not automatically installed merely because it is new.
10. Deterministic controls are preferred over LLM decisions where possible.
11. AI agents receive scoped capabilities.
12. Planner != Executor != Verifier != Auditor.
13. Every destructive operation requires recoverability safeguards.
14. Platforms remain logically and operationally separated.
15. Platform data must not silently cross platform boundaries.
16. Continuous research, modernization and improvement are permanent.
17. Physical infrastructure is part of platform reality.
18. The system must understand its own visibility limitations.
19. Unknown external credentials must never be invented.
20. The maintenance center must be capable of protecting itself.

GLOBAL LOOP
-----------
DISCOVER
    -> BASELINE
    -> CLASSIFY
    -> RESEARCH
    -> VERIFY SOURCE
    -> DETERMINE APPLICABILITY
    -> MAP IMPACT
    -> ASSESS RISK
    -> PLAN
    -> REQUEST REAL EXECUTION
    -> INDEPENDENT VERIFY
    -> EVIDENCE
    -> OBSERVE
    -> LEARN
    -> MODERNIZE
    -> REPEAT

PLATFORM STATES
---------------
DISCOVERED
BASELINED
REPAIRING
INTEGRATING
VERIFYING
READY_FOR_LAUNCH
LAUNCHING
HEALTHY
CONTINUOUS_MAINTENANCE
DEGRADED
QUARANTINED
LEGAL_REVIEW_REQUIRED
OWNER_ACTION_REQUIRED
BLOCKED_EXTERNAL_DEPENDENCY

REALITY STATES
--------------
DESIRED_STATE
OBSERVED_STATE
VERIFIED_STATE
EVIDENCED_STATE

GLOBAL INTELLIGENCE DOMAINS
---------------------------
Government
Regulation
Cybersecurity
Privacy
Data Governance
AI Governance
Cloud
Infrastructure
Physical Infrastructure
Hardware
Networking
Software Engineering
Supply Chain
Identity
Payments
Finance
Commerce
Tax
Email
Domains
DNS
TLS
Content
Media
Children
Gaming
Marketplace
Accessibility
Consumer Protection
Contracts
Vendors
Licensing
Intellectual Property
Business Continuity
Disaster Recovery
Observability
Reliability
Performance
Capacity
Cost
Sustainability
Emerging Technology
Standards
APIs
Framework Lifecycle
Cryptography
Post-Quantum Readiness
Trust & Safety

IMPORTANT
---------
This file intentionally separates DECISION from EXECUTION.
It creates auditable plans and structured execution requests for file 02.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import json
import logging
import os
import pathlib
import platform
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


# =====================================================================
# IDENTITY / VERSION
# =====================================================================

APP_NAME = "MAJD COMPREHENSIVE MAINTENANCE CENTER"
FILE_NAME = "MAJD-MAINTENANCE-MASTERMIND-01.py"
VERSION = "1.0.0"
SCHEMA_VERSION = 1

SUPREME_AUTHORITY = "SUPREME_OWNER"

PROJECT_ROOT = pathlib.Path(
    os.environ.get(
        "MAJD_MAINTENANCE_ROOT",
        pathlib.Path(__file__).resolve().parent
    )
).resolve()

STATE_DIR = PROJECT_ROOT / "state"
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"
REQUEST_DIR = PROJECT_ROOT / "execution_requests"
EVIDENCE_DIR = PROJECT_ROOT / "evidence"
POLICY_DIR = PROJECT_ROOT / "policies"
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
BACKUP_META_DIR = PROJECT_ROOT / "backup_metadata"

DB_PATH = DATA_DIR / "majd_maintenance_mastermind.sqlite3"
LOG_PATH = LOG_DIR / "mastermind-01.log"

DEFAULT_DISCOVERY_ROOTS = [
    pathlib.Path("/root"),
    pathlib.Path("/srv"),
    pathlib.Path("/opt"),
]

MAJD_NAME_PATTERN = re.compile(r"^MAJD(?:[-_].+)?$", re.IGNORECASE)

HTTP_TIMEOUT = int(os.environ.get("MAJD_INTELLIGENCE_HTTP_TIMEOUT", "15"))
MAX_SOURCE_BYTES = int(
    os.environ.get("MAJD_INTELLIGENCE_MAX_SOURCE_BYTES", str(2 * 1024 * 1024))
)

USER_AGENT = (
    "MAJD-Comprehensive-Maintenance-Center/"
    f"{VERSION} (+Sovereign-Regulatory-Intelligence)"
)


# =====================================================================
# DIRECTORIES / LOGGING
# =====================================================================

for directory in (
    STATE_DIR,
    DATA_DIR,
    LOG_DIR,
    REQUEST_DIR,
    EVIDENCE_DIR,
    POLICY_DIR,
    KNOWLEDGE_DIR,
    BACKUP_META_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=os.environ.get("MAJD_LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
    ],
)

LOG = logging.getLogger("MAJD-MASTERMIND-01")


# =====================================================================
# ENUMS
# =====================================================================

class PlatformState(str, Enum):
    DISCOVERED = "DISCOVERED"
    BASELINED = "BASELINED"
    REPAIRING = "REPAIRING"
    INTEGRATING = "INTEGRATING"
    VERIFYING = "VERIFYING"
    READY_FOR_LAUNCH = "READY_FOR_LAUNCH"
    LAUNCHING = "LAUNCHING"
    HEALTHY = "HEALTHY"
    CONTINUOUS_MAINTENANCE = "CONTINUOUS_MAINTENANCE"
    DEGRADED = "DEGRADED"
    QUARANTINED = "QUARANTINED"
    LEGAL_REVIEW_REQUIRED = "LEGAL_REVIEW_REQUIRED"
    OWNER_ACTION_REQUIRED = "OWNER_ACTION_REQUIRED"
    BLOCKED_EXTERNAL_DEPENDENCY = "BLOCKED_EXTERNAL_DEPENDENCY"


class RequirementState(str, Enum):
    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    IMPLEMENTED = "IMPLEMENTED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    NOT_VERIFIED = "NOT_VERIFIED"
    LEGAL_REVIEW_REQUIRED = "LEGAL_REVIEW_REQUIRED"


class SourceAuthority(str, Enum):
    GOVERNMENT = "GOVERNMENT"
    REGULATOR = "REGULATOR"
    OFFICIAL_STANDARDS_BODY = "OFFICIAL_STANDARDS_BODY"
    AUTHORITATIVE_FOUNDATION = "AUTHORITATIVE_FOUNDATION"
    PROVIDER_OFFICIAL = "PROVIDER_OFFICIAL"
    SECONDARY = "SECONDARY"


class Visibility(str, Enum):
    DIRECTLY_CONTROLLED = "DIRECTLY_CONTROLLED"
    DIRECTLY_OBSERVED = "DIRECTLY_OBSERVED"
    PROVIDER_REPORTED = "PROVIDER_REPORTED"
    CONTRACTUALLY_ASSURED = "CONTRACTUALLY_ASSURED"
    NOT_VISIBLE = "NOT_VISIBLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class DecisionType(str, Enum):
    OBSERVE_ONLY = "OBSERVE_ONLY"
    PLAN_CHANGE = "PLAN_CHANGE"
    REQUEST_EXECUTION = "REQUEST_EXECUTION"
    REQUIRE_VERIFICATION = "REQUIRE_VERIFICATION"
    REQUIRE_LEGAL_REVIEW = "REQUIRE_LEGAL_REVIEW"
    REQUIRE_OWNER_ACTION = "REQUIRE_OWNER_ACTION"
    QUARANTINE_RECOMMENDED = "QUARANTINE_RECOMMENDED"


# =====================================================================
# DATA MODELS
# =====================================================================

@dataclass
class PlatformRecord:
    platform_id: str
    name: str
    root_path: str
    state: str = PlatformState.DISCOVERED.value
    platform_type: str = "UNKNOWN"
    sector: str = "GENERAL"
    countries: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    data_classes: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    discovered_at: str = ""
    updated_at: str = ""


@dataclass
class IntelligenceSource:
    source_id: str
    name: str
    url: str
    authority: str
    jurisdiction: str
    topic: str
    enabled: bool = True
    last_checked: Optional[str] = None
    last_hash: Optional[str] = None
    effective_date: Optional[str] = None
    notes: str = ""


@dataclass
class Requirement:
    requirement_id: str
    source_id: str
    jurisdiction: str
    sector: str
    topic: str
    title: str
    description: str
    state: str = RequirementState.NOT_VERIFIED.value
    effective_date: Optional[str] = None
    deadline: Optional[str] = None
    evidence_required: bool = True
    legal_review_required: bool = False


@dataclass
class RiskRecord:
    risk_id: str
    platform_id: str
    category: str
    title: str
    description: str
    likelihood: int
    impact: int
    score: int
    level: str
    status: str = "OPEN"
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Decision:
    decision_id: str
    platform_id: Optional[str]
    decision_type: str
    title: str
    rationale: str
    risk_level: str
    reversible: bool
    requires_backup: bool
    requires_independent_verification: bool
    requires_legal_review: bool
    requires_owner_action: bool
    created_at: str


@dataclass
class ExecutionRequest:
    request_id: str
    platform_id: Optional[str]
    action: str
    scope: Dict[str, Any]
    reason: str
    risk_level: str
    backup_required: bool
    rollback_required: bool
    independent_verification_required: bool
    owner_authority: str
    created_at: str
    status: str = "PENDING_EXECUTOR"


# =====================================================================
# UTILITIES
# =====================================================================

def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def stable_id(prefix: str, *parts: str) -> str:
    raw = "::".join(str(x) for x in parts)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]
    return f"{prefix}_{digest}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_dumps(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        default=str,
    )


def safe_json_loads(value: Optional[str], default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except Exception:
        return default


def atomic_write_json(path: pathlib.Path, payload: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json_dumps(payload), encoding="utf-8")
    os.replace(tmp, path)


def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


# =====================================================================
# DATABASE
# =====================================================================

class Database:
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
                root_path TEXT NOT NULL UNIQUE,
                state TEXT NOT NULL,
                platform_type TEXT NOT NULL,
                sector TEXT NOT NULL,
                countries_json TEXT NOT NULL,
                domains_json TEXT NOT NULL,
                technologies_json TEXT NOT NULL,
                data_classes_json TEXT NOT NULL,
                capabilities_json TEXT NOT NULL,
                discovered_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS sources (
                source_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                authority TEXT NOT NULL,
                jurisdiction TEXT NOT NULL,
                topic TEXT NOT NULL,
                enabled INTEGER NOT NULL,
                last_checked TEXT,
                last_hash TEXT,
                effective_date TEXT,
                notes TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS source_snapshots (
                snapshot_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                checked_at TEXT NOT NULL,
                content_length INTEGER NOT NULL,
                changed INTEGER NOT NULL,
                FOREIGN KEY(source_id) REFERENCES sources(source_id)
            );

            CREATE TABLE IF NOT EXISTS requirements (
                requirement_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                jurisdiction TEXT NOT NULL,
                sector TEXT NOT NULL,
                topic TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                state TEXT NOT NULL,
                effective_date TEXT,
                deadline TEXT,
                evidence_required INTEGER NOT NULL,
                legal_review_required INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS applicability (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                requirement_id TEXT NOT NULL,
                platform_id TEXT NOT NULL,
                state TEXT NOT NULL,
                reason TEXT NOT NULL,
                evaluated_at TEXT NOT NULL,
                UNIQUE(requirement_id, platform_id)
            );

            CREATE TABLE IF NOT EXISTS risks (
                risk_id TEXT PRIMARY KEY,
                platform_id TEXT NOT NULL,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                likelihood INTEGER NOT NULL,
                impact INTEGER NOT NULL,
                score INTEGER NOT NULL,
                level TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS decisions (
                decision_id TEXT PRIMARY KEY,
                platform_id TEXT,
                decision_type TEXT NOT NULL,
                title TEXT NOT NULL,
                rationale TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                reversible INTEGER NOT NULL,
                requires_backup INTEGER NOT NULL,
                requires_independent_verification INTEGER NOT NULL,
                requires_legal_review INTEGER NOT NULL,
                requires_owner_action INTEGER NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS execution_requests (
                request_id TEXT PRIMARY KEY,
                platform_id TEXT,
                action TEXT NOT NULL,
                scope_json TEXT NOT NULL,
                reason TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                backup_required INTEGER NOT NULL,
                rollback_required INTEGER NOT NULL,
                independent_verification_required INTEGER NOT NULL,
                owner_authority TEXT NOT NULL,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS evidence (
                evidence_id TEXT PRIMARY KEY,
                platform_id TEXT,
                requirement_id TEXT,
                evidence_type TEXT NOT NULL,
                source TEXT NOT NULL,
                digest TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS knowledge_events (
                event_id TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                subject TEXT NOT NULL,
                source_id TEXT,
                old_hash TEXT,
                new_hash TEXT,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS world_model_edges (
                edge_id TEXT PRIMARY KEY,
                source_type TEXT NOT NULL,
                source_id TEXT NOT NULL,
                relation TEXT NOT NULL,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
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
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
            """,
            (str(SCHEMA_VERSION),),
        )
        self.conn.commit()

    def audit(
        self,
        action: str,
        target: str,
        payload: Optional[Dict[str, Any]] = None,
        actor: str = FILE_NAME,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO audit(
                audit_id, actor, action, target, payload_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid.uuid4()),
                actor,
                action,
                target,
                json_dumps(payload or {}),
                utc_now(),
            ),
        )
        self.conn.commit()


# =====================================================================
# GLOBAL CONSTITUTION
# =====================================================================

GLOBAL_CONSTITUTION: Dict[str, Any] = {
    "authority": {
        "highest": SUPREME_AUTHORITY,
        "ai_cannot_override_owner": True,
    },
    "reality": {
        "fake_success_forbidden": True,
        "service_active_is_not_sufficient_proof": True,
        "independent_verification_required": True,
        "evidence_required_for_assurance_claims": True,
    },
    "automation": {
        "routine_maintenance_autonomous": True,
        "routine_repair_autonomous": True,
        "routine_verification_autonomous": True,
        "routine_monitoring_autonomous": True,
        "destructive_changes_require_recoverability": True,
        "external_credentials_cannot_be_invented": True,
    },
    "engineering": {
        "continuous_development": True,
        "continuous_modernization": True,
        "old_code_not_sacred": True,
        "preserve_required_behavior_and_data": True,
        "deterministic_controls_preferred_when_possible": True,
    },
    "governance": {
        "policy_as_code": True,
        "policy_drift_detection": True,
        "legal_ambiguity_requires_review": True,
        "official_sources_first": True,
    },
    "security": {
        "zero_trust_direction": True,
        "least_privilege": True,
        "separation_of_duties": True,
        "blast_radius_control": True,
        "surgical_containment": True,
        "full_platform_shutdown_last_resort": True,
    },
    "data": {
        "platform_data_separation": True,
        "data_lineage_required_where_applicable": True,
        "cross_border_transfer_analysis": True,
        "retention_governance": True,
    },
    "ai": {
        "agent_permissions_scoped": True,
        "untrusted_content_is_not_instruction": True,
        "model_registry_required": True,
        "prompt_tool_memory_governance": True,
        "kill_switch_required": True,
    },
    "physical": {
        "physical_infrastructure_is_part_of_platform_state": True,
        "visibility_must_be_explicit": True,
        "hardware_health_matters": True,
        "power_cooling_network_storage_are_dependencies": True,
    },
}


# =====================================================================
# OFFICIAL / AUTHORITATIVE SOURCE REGISTRY
# =====================================================================

DEFAULT_SOURCES: Sequence[Tuple[str, str, str, str, str]] = (
    (
        "Saudi NCA",
        "https://nca.gov.sa/",
        SourceAuthority.REGULATOR.value,
        "SA",
        "CYBERSECURITY",
    ),
    (
        "Saudi Data & AI Authority",
        "https://sdaia.gov.sa/",
        SourceAuthority.REGULATOR.value,
        "SA",
        "PRIVACY_AI_DATA",
    ),
    (
        "Saudi Central Bank",
        "https://www.sama.gov.sa/",
        SourceAuthority.REGULATOR.value,
        "SA",
        "FINANCE_PAYMENTS",
    ),
    (
        "Saudi Ministry of Commerce",
        "https://mc.gov.sa/",
        SourceAuthority.GOVERNMENT.value,
        "SA",
        "COMMERCE",
    ),
    (
        "European Commission Digital Strategy",
        "https://digital-strategy.ec.europa.eu/",
        SourceAuthority.GOVERNMENT.value,
        "EU",
        "DIGITAL_AI_DATA",
    ),
    (
        "EUR-Lex",
        "https://eur-lex.europa.eu/",
        SourceAuthority.GOVERNMENT.value,
        "EU",
        "LAW",
    ),
    (
        "ENISA",
        "https://www.enisa.europa.eu/",
        SourceAuthority.REGULATOR.value,
        "EU",
        "CYBERSECURITY",
    ),
    (
        "EDPB",
        "https://www.edpb.europa.eu/",
        SourceAuthority.REGULATOR.value,
        "EU",
        "PRIVACY",
    ),
    (
        "UK ICO",
        "https://ico.org.uk/",
        SourceAuthority.REGULATOR.value,
        "UK",
        "PRIVACY_CHILDREN_AI",
    ),
    (
        "NIST",
        "https://www.nist.gov/",
        SourceAuthority.OFFICIAL_STANDARDS_BODY.value,
        "GLOBAL",
        "CYBERSECURITY_AI_PRIVACY",
    ),
    (
        "CISA",
        "https://www.cisa.gov/",
        SourceAuthority.GOVERNMENT.value,
        "US",
        "CYBERSECURITY",
    ),
    (
        "IETF",
        "https://www.ietf.org/",
        SourceAuthority.OFFICIAL_STANDARDS_BODY.value,
        "GLOBAL",
        "INTERNET_PROTOCOLS",
    ),
    (
        "W3C",
        "https://www.w3.org/",
        SourceAuthority.OFFICIAL_STANDARDS_BODY.value,
        "GLOBAL",
        "WEB_ACCESSIBILITY",
    ),
    (
        "OWASP",
        "https://owasp.org/",
        SourceAuthority.AUTHORITATIVE_FOUNDATION.value,
        "GLOBAL",
        "APPLICATION_AI_SECURITY",
    ),
    (
        "OpenSSF",
        "https://openssf.org/",
        SourceAuthority.AUTHORITATIVE_FOUNDATION.value,
        "GLOBAL",
        "SOFTWARE_SUPPLY_CHAIN",
    ),
    (
        "CNCF",
        "https://www.cncf.io/",
        SourceAuthority.AUTHORITATIVE_FOUNDATION.value,
        "GLOBAL",
        "CLOUD_NATIVE",
    ),
    (
        "OECD AI",
        "https://oecd.ai/",
        SourceAuthority.AUTHORITATIVE_FOUNDATION.value,
        "GLOBAL",
        "AI_GOVERNANCE",
    ),
    (
        "ITU",
        "https://www.itu.int/",
        SourceAuthority.OFFICIAL_STANDARDS_BODY.value,
        "GLOBAL",
        "TELECOMMUNICATIONS_CHILD_SAFETY",
    ),
    (
        "ISO",
        "https://www.iso.org/",
        SourceAuthority.OFFICIAL_STANDARDS_BODY.value,
        "GLOBAL",
        "STANDARDS",
    ),
)


# =====================================================================
# SOURCE TRUST
# =====================================================================

AUTHORITY_WEIGHT = {
    SourceAuthority.GOVERNMENT.value: 100,
    SourceAuthority.REGULATOR.value: 100,
    SourceAuthority.OFFICIAL_STANDARDS_BODY.value: 95,
    SourceAuthority.AUTHORITATIVE_FOUNDATION.value: 85,
    SourceAuthority.PROVIDER_OFFICIAL.value: 75,
    SourceAuthority.SECONDARY.value: 35,
}


class SourceTrust:
    @staticmethod
    def score(authority: str) -> int:
        return AUTHORITY_WEIGHT.get(authority, 0)

    @staticmethod
    def can_drive_automatic_policy(authority: str) -> bool:
        return SourceTrust.score(authority) >= 75


# =====================================================================
# PLATFORM DISCOVERY
# =====================================================================

class PlatformDiscovery:
    def __init__(self, db: Database):
        self.db = db

    def discover(
        self,
        roots: Optional[Iterable[pathlib.Path]] = None,
    ) -> List[PlatformRecord]:
        roots = list(roots or DEFAULT_DISCOVERY_ROOTS)
        discovered: List[PlatformRecord] = []

        for root in roots:
            if not root.exists() or not root.is_dir():
                continue

            try:
                children = list(root.iterdir())
            except PermissionError:
                continue

            for child in children:
                if not child.is_dir():
                    continue

                if not MAJD_NAME_PATTERN.match(child.name):
                    continue

                if child.resolve() == PROJECT_ROOT:
                    continue

                record = self._inspect_platform(child)
                self._upsert(record)
                discovered.append(record)

        self.db.audit(
            "PLATFORM_DISCOVERY",
            "LOCAL_FILESYSTEM",
            {"count": len(discovered)},
        )
        return discovered

    def _inspect_platform(self, path: pathlib.Path) -> PlatformRecord:
        technologies: List[str] = []
        capabilities: List[str] = []

        indicators = {
            "requirements.txt": "PYTHON",
            "pyproject.toml": "PYTHON",
            "package.json": "NODEJS",
            "Dockerfile": "CONTAINER",
            "docker-compose.yml": "DOCKER_COMPOSE",
            "compose.yaml": "DOCKER_COMPOSE",
            ".git": "GIT",
        }

        for filename, technology in indicators.items():
            if (path / filename).exists():
                technologies.append(technology)

        file_names: List[str] = []
        try:
            file_names = [x.name.lower() for x in path.iterdir()][:1000]
        except Exception:
            pass

        joined = " ".join(file_names)

        capability_words = {
            "email": "EMAIL",
            "mail": "EMAIL",
            "payment": "PAYMENTS",
            "moyasar": "PAYMENTS",
            "domain": "DOMAINS",
            "dns": "DNS",
            "game": "GAMING",
            "kids": "CHILDREN",
            "delivery": "DELIVERY",
            "n8n": "AUTOMATION",
            "ai": "AI",
        }

        for word, capability in capability_words.items():
            if word in joined or word in path.name.lower():
                capabilities.append(capability)

        now = utc_now()
        platform_id = stable_id("platform", str(path.resolve()))

        return PlatformRecord(
            platform_id=platform_id,
            name=path.name,
            root_path=str(path.resolve()),
            technologies=sorted(set(technologies)),
            capabilities=sorted(set(capabilities)),
            discovered_at=now,
            updated_at=now,
        )

    def _upsert(self, p: PlatformRecord) -> None:
        existing = self.db.conn.execute(
            "SELECT discovered_at FROM platforms WHERE platform_id=?",
            (p.platform_id,),
        ).fetchone()

        discovered_at = (
            existing["discovered_at"] if existing else p.discovered_at
        )

        self.db.conn.execute(
            """
            INSERT INTO platforms(
                platform_id, name, root_path, state, platform_type, sector,
                countries_json, domains_json, technologies_json,
                data_classes_json, capabilities_json,
                discovered_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(platform_id) DO UPDATE SET
                name=excluded.name,
                root_path=excluded.root_path,
                technologies_json=excluded.technologies_json,
                capabilities_json=excluded.capabilities_json,
                updated_at=excluded.updated_at
            """,
            (
                p.platform_id,
                p.name,
                p.root_path,
                p.state,
                p.platform_type,
                p.sector,
                json_dumps(p.countries),
                json_dumps(p.domains),
                json_dumps(p.technologies),
                json_dumps(p.data_classes),
                json_dumps(p.capabilities),
                discovered_at,
                p.updated_at,
            ),
        )
        self.db.conn.commit()


# =====================================================================
# PLATFORM CLASSIFICATION
# =====================================================================

class PlatformClassifier:
    RULES = {
        "KIDS": ("CHILDREN", ["KIDS", "CHILD"]),
        "GAME": ("GAMING", ["GAME"]),
        "DELIVERY": ("DELIVERY", ["DELIVERY"]),
        "EMAIL": ("COMMUNICATIONS", ["EMAIL", "MAIL"]),
        "DMAIL": ("DOMAIN_EMAIL", ["DMAIL"]),
        "GIT": ("DEVELOPER_INFRASTRUCTURE", ["GIT"]),
        "IN": ("AUTOMATION", ["N8N", "AUTOMATION"]),
        "SERVER": ("INFRASTRUCTURE", ["SERVER"]),
    }

    def __init__(self, db: Database):
        self.db = db

    def classify_all(self) -> int:
        rows = self.db.conn.execute(
            "SELECT * FROM platforms"
        ).fetchall()

        count = 0

        for row in rows:
            name_upper = row["name"].upper()
            platform_type = "GENERAL_DIGITAL_PLATFORM"
            sector = "GENERAL"

            for marker, (ptype, aliases) in self.RULES.items():
                if marker in name_upper or any(x in name_upper for x in aliases):
                    platform_type = ptype
                    sector = ptype
                    break

            self.db.conn.execute(
                """
                UPDATE platforms
                SET platform_type=?, sector=?, updated_at=?
                WHERE platform_id=?
                """,
                (
                    platform_type,
                    sector,
                    utc_now(),
                    row["platform_id"],
                ),
            )
            count += 1

        self.db.conn.commit()
        self.db.audit("PLATFORM_CLASSIFICATION", "ALL", {"count": count})
        return count


# =====================================================================
# WORLD MODEL
# =====================================================================

class WorldModel:
    def __init__(self, db: Database):
        self.db = db

    def link(
        self,
        source_type: str,
        source_id: str,
        relation: str,
        target_type: str,
        target_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        edge_id = stable_id(
            "edge",
            source_type,
            source_id,
            relation,
            target_type,
            target_id,
        )

        self.db.conn.execute(
            """
            INSERT INTO world_model_edges(
                edge_id, source_type, source_id, relation,
                target_type, target_id, metadata_json, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(edge_id) DO UPDATE SET
                metadata_json=excluded.metadata_json,
                updated_at=excluded.updated_at
            """,
            (
                edge_id,
                source_type,
                source_id,
                relation,
                target_type,
                target_id,
                json_dumps(metadata or {}),
                utc_now(),
            ),
        )
        self.db.conn.commit()
        return edge_id

    def rebuild_basic_graph(self) -> int:
        count = 0

        rows = self.db.conn.execute(
            "SELECT * FROM platforms"
        ).fetchall()

        for row in rows:
            platform_id = row["platform_id"]

            for tech in safe_json_loads(row["technologies_json"], []):
                self.link(
                    "PLATFORM",
                    platform_id,
                    "USES_TECHNOLOGY",
                    "TECHNOLOGY",
                    tech,
                )
                count += 1

            for capability in safe_json_loads(
                row["capabilities_json"], []
            ):
                self.link(
                    "PLATFORM",
                    platform_id,
                    "HAS_CAPABILITY",
                    "CAPABILITY",
                    capability,
                )
                count += 1

            for country in safe_json_loads(row["countries_json"], []):
                self.link(
                    "PLATFORM",
                    platform_id,
                    "OPERATES_IN",
                    "JURISDICTION",
                    country,
                )
                count += 1

        return count


# =====================================================================
# INTELLIGENCE REGISTRY
# =====================================================================

class IntelligenceRegistry:
    def __init__(self, db: Database):
        self.db = db

    def seed_defaults(self) -> int:
        count = 0

        for name, url, authority, jurisdiction, topic in DEFAULT_SOURCES:
            source_id = stable_id("source", url)

            self.db.conn.execute(
                """
                INSERT INTO sources(
                    source_id, name, url, authority,
                    jurisdiction, topic, enabled, notes
                )
                VALUES (?, ?, ?, ?, ?, ?, 1, '')
                ON CONFLICT(url) DO NOTHING
                """,
                (
                    source_id,
                    name,
                    url,
                    authority,
                    jurisdiction,
                    topic,
                ),
            )
            count += 1

        self.db.conn.commit()
        return count

    def add_source(
        self,
        name: str,
        url: str,
        authority: str,
        jurisdiction: str,
        topic: str,
        notes: str = "",
    ) -> str:
        parsed = urllib.parse.urlparse(url)

        if parsed.scheme != "https":
            raise ValueError("Intelligence sources must use HTTPS.")

        source_id = stable_id("source", url)

        self.db.conn.execute(
            """
            INSERT INTO sources(
                source_id, name, url, authority,
                jurisdiction, topic, enabled, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, 1, ?)
            ON CONFLICT(url) DO UPDATE SET
                name=excluded.name,
                authority=excluded.authority,
                jurisdiction=excluded.jurisdiction,
                topic=excluded.topic,
                notes=excluded.notes
            """,
            (
                source_id,
                name,
                url,
                authority,
                jurisdiction,
                topic,
                notes,
            ),
        )
        self.db.conn.commit()
        return source_id


# =====================================================================
# SAFE INTELLIGENCE FETCHER
# =====================================================================

class IntelligenceFetcher:
    """
    Fetches configured official/authoritative HTTPS sources.

    SECURITY:
    - Web content is treated strictly as UNTRUSTED DATA.
    - Retrieved content is NEVER executed.
    - Retrieved content is NEVER interpreted as a shell command.
    - No source may directly authorize an infrastructure change.
    """

    def __init__(self, db: Database):
        self.db = db

    def fetch_all(self) -> Dict[str, int]:
        stats = {
            "checked": 0,
            "changed": 0,
            "failed": 0,
        }

        rows = self.db.conn.execute(
            "SELECT * FROM sources WHERE enabled=1"
        ).fetchall()

        for row in rows:
            try:
                changed = self._fetch_one(row)
                stats["checked"] += 1
                if changed:
                    stats["changed"] += 1
            except Exception as exc:
                stats["failed"] += 1
                LOG.warning(
                    "INTELLIGENCE_FETCH_FAILED | %s | %s",
                    row["name"],
                    exc,
                )

        self.db.audit(
            "GLOBAL_INTELLIGENCE_REFRESH",
            "SOURCE_REGISTRY",
            stats,
        )
        return stats

    def _fetch_one(self, row: sqlite3.Row) -> bool:
        url = row["url"]
        parsed = urllib.parse.urlparse(url)

        if parsed.scheme != "https":
            raise ValueError("Non-HTTPS source rejected.")

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": (
                    "text/html,application/xhtml+xml,"
                    "application/json,text/plain;q=0.9,*/*;q=0.1"
                ),
            },
        )

        with urllib.request.urlopen(
            req,
            timeout=HTTP_TIMEOUT,
        ) as response:
            final_url = response.geturl()
            final_parsed = urllib.parse.urlparse(final_url)

            if final_parsed.scheme != "https":
                raise ValueError("Redirected to non-HTTPS destination.")

            data = response.read(MAX_SOURCE_BYTES + 1)

            if len(data) > MAX_SOURCE_BYTES:
                raise ValueError("Source exceeded configured size limit.")

        digest = sha256_bytes(data)
        old_hash = row["last_hash"]
        changed = bool(old_hash and old_hash != digest)

        snapshot_id = str(uuid.uuid4())
        checked_at = utc_now()

        self.db.conn.execute(
            """
            INSERT INTO source_snapshots(
                snapshot_id, source_id, content_hash,
                checked_at, content_length, changed
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                snapshot_id,
                row["source_id"],
                digest,
                checked_at,
                len(data),
                1 if changed else 0,
            ),
        )

        self.db.conn.execute(
            """
            UPDATE sources
            SET last_checked=?, last_hash=?
            WHERE source_id=?
            """,
            (
                checked_at,
                digest,
                row["source_id"],
            ),
        )

        if changed:
            self.db.conn.execute(
                """
                INSERT INTO knowledge_events(
                    event_id, category, subject, source_id,
                    old_hash, new_hash, payload_json, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid.uuid4()),
                    "SOURCE_CHANGED",
                    row["name"],
                    row["source_id"],
                    old_hash,
                    digest,
                    json_dumps(
                        {
                            "url": url,
                            "authority": row["authority"],
                            "jurisdiction": row["jurisdiction"],
                            "topic": row["topic"],
                            "note": (
                                "Content changed. Change requires "
                                "structured analysis before policy action."
                            ),
                        }
                    ),
                    checked_at,
                ),
            )

        self.db.conn.commit()
        return changed


# =====================================================================
# REGULATORY APPLICABILITY
# =====================================================================

class ApplicabilityEngine:
    """
    Conservative applicability evaluator.

    It deliberately avoids pretending to be a lawyer.
    """

    def __init__(self, db: Database):
        self.db = db

    def evaluate_all(self) -> int:
        requirements = self.db.conn.execute(
            "SELECT * FROM requirements"
        ).fetchall()

        platforms = self.db.conn.execute(
            "SELECT * FROM platforms"
        ).fetchall()

        count = 0

        for req in requirements:
            for platform_row in platforms:
                state, reason = self._evaluate(req, platform_row)

                self.db.conn.execute(
                    """
                    INSERT INTO applicability(
                        requirement_id, platform_id,
                        state, reason, evaluated_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(requirement_id, platform_id)
                    DO UPDATE SET
                        state=excluded.state,
                        reason=excluded.reason,
                        evaluated_at=excluded.evaluated_at
                    """,
                    (
                        req["requirement_id"],
                        platform_row["platform_id"],
                        state,
                        reason,
                        utc_now(),
                    ),
                )
                count += 1

        self.db.conn.commit()
        return count

    def _evaluate(
        self,
        req: sqlite3.Row,
        platform_row: sqlite3.Row,
    ) -> Tuple[str, str]:
        if bool(req["legal_review_required"]):
            return (
                RequirementState.LEGAL_REVIEW_REQUIRED.value,
                "Requirement explicitly requires legal review.",
            )

        req_jurisdiction = req["jurisdiction"].upper()
        platform_countries = [
            str(x).upper()
            for x in safe_json_loads(
                platform_row["countries_json"],
                [],
            )
        ]

        if req_jurisdiction == "GLOBAL":
            return (
                RequirementState.APPLICABLE.value,
                "Global requirement candidate.",
            )

        if not platform_countries:
            return (
                RequirementState.NOT_VERIFIED.value,
                "Platform jurisdictions are not yet established.",
            )

        if req_jurisdiction in platform_countries:
            return (
                RequirementState.APPLICABLE.value,
                "Platform operates in matching jurisdiction.",
            )

        return (
            RequirementState.NOT_APPLICABLE.value,
            "No current jurisdiction match.",
        )


# =====================================================================
# RISK ENGINE
# =====================================================================

class RiskEngine:
    @staticmethod
    def level(score: int) -> str:
        if score >= 20:
            return RiskLevel.CRITICAL.value
        if score >= 12:
            return RiskLevel.HIGH.value
        if score >= 6:
            return RiskLevel.MEDIUM.value
        return RiskLevel.LOW.value

    def __init__(self, db: Database):
        self.db = db

    def register(
        self,
        platform_id: str,
        category: str,
        title: str,
        description: str,
        likelihood: int,
        impact: int,
    ) -> RiskRecord:
        likelihood = clamp(likelihood, 1, 5)
        impact = clamp(impact, 1, 5)
        score = likelihood * impact
        now = utc_now()

        risk_id = stable_id(
            "risk",
            platform_id,
            category,
            title,
        )

        record = RiskRecord(
            risk_id=risk_id,
            platform_id=platform_id,
            category=category,
            title=title,
            description=description,
            likelihood=likelihood,
            impact=impact,
            score=score,
            level=self.level(score),
            created_at=now,
            updated_at=now,
        )

        self.db.conn.execute(
            """
            INSERT INTO risks(
                risk_id, platform_id, category, title,
                description, likelihood, impact, score,
                level, status, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(risk_id) DO UPDATE SET
                description=excluded.description,
                likelihood=excluded.likelihood,
                impact=excluded.impact,
                score=excluded.score,
                level=excluded.level,
                updated_at=excluded.updated_at
            """,
            (
                record.risk_id,
                record.platform_id,
                record.category,
                record.title,
                record.description,
                record.likelihood,
                record.impact,
                record.score,
                record.level,
                record.status,
                record.created_at,
                record.updated_at,
            ),
        )
        self.db.conn.commit()
        return record


# =====================================================================
# POLICY ENGINE
# =====================================================================

class PolicyEngine:
    def __init__(self, db: Database):
        self.db = db

    def write_global_constitution(self) -> pathlib.Path:
        path = POLICY_DIR / "MAJD-GLOBAL-CONSTITUTION.json"

        payload = {
            "name": "MAJD GLOBAL CONSTITUTION",
            "version": VERSION,
            "authority": SUPREME_AUTHORITY,
            "generated_at": utc_now(),
            "constitution": GLOBAL_CONSTITUTION,
        }

        atomic_write_json(path, payload)

        self.db.audit(
            "POLICY_WRITE",
            str(path),
            {"type": "GLOBAL_CONSTITUTION"},
        )
        return path

    def generate_platform_constitutions(self) -> int:
        rows = self.db.conn.execute(
            "SELECT * FROM platforms"
        ).fetchall()

        count = 0

        for row in rows:
            payload = {
                "platform_id": row["platform_id"],
                "platform_name": row["name"],
                "inherits": "MAJD GLOBAL CONSTITUTION",
                "authority": SUPREME_AUTHORITY,
                "platform_type": row["platform_type"],
                "sector": row["sector"],
                "jurisdictions": safe_json_loads(
                    row["countries_json"], []
                ),
                "capabilities": safe_json_loads(
                    row["capabilities_json"], []
                ),
                "rules": {
                    "fake_success_forbidden": True,
                    "independent_verification_required": True,
                    "platform_data_separation": True,
                    "continuous_maintenance": True,
                    "continuous_security": True,
                    "continuous_modernization": True,
                    "legal_ambiguity_requires_review": True,
                },
                "generated_at": utc_now(),
            }

            safe_name = re.sub(
                r"[^A-Za-z0-9_.-]+",
                "_",
                row["name"],
            )

            path = POLICY_DIR / f"{safe_name}.constitution.json"
            atomic_write_json(path, payload)
            count += 1

        return count


# =====================================================================
# PHYSICAL / CYBER-PHYSICAL MODEL
# =====================================================================

class PhysicalInfrastructureModel:
    """
    Records what the system can actually observe.

    It never claims facility-level visibility if no telemetry/provider
    integration exists.
    """

    COMPONENTS = (
        "POWER",
        "UPS",
        "BATTERY",
        "COOLING",
        "TEMPERATURE",
        "HUMIDITY",
        "FIRE",
        "WATER_LEAK",
        "PHYSICAL_ACCESS",
        "CPU",
        "GPU",
        "MEMORY",
        "DISK",
        "NVME",
        "RAID",
        "NIC",
        "NETWORK_LINK",
        "FIRMWARE",
        "BMC",
        "CLOCK",
        "FACILITY",
    )

    def snapshot_local_host(self) -> Dict[str, Any]:
        return {
            "captured_at": utc_now(),
            "hostname": platform.node(),
            "os": platform.platform(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "visibility": {
                component: (
                    Visibility.NOT_VISIBLE.value
                    if component in {
                        "UPS",
                        "BATTERY",
                        "COOLING",
                        "HUMIDITY",
                        "FIRE",
                        "WATER_LEAK",
                        "PHYSICAL_ACCESS",
                        "FACILITY",
                    }
                    else Visibility.DIRECTLY_OBSERVED.value
                )
                for component in self.COMPONENTS
            },
            "note": (
                "Visibility is conservative. Actual sensor/provider "
                "adapters are added by the execution/runtime layers."
            ),
        }


# =====================================================================
# ARCHITECTURE / MODERNIZATION
# =====================================================================

class ModernizationEngine:
    """
    Produces modernization candidates.
    It does NOT automatically install newest versions.
    """

    def __init__(self, db: Database):
        self.db = db

    def assess_platform(self, row: sqlite3.Row) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        root = pathlib.Path(row["root_path"])

        if not root.exists():
            findings.append(
                {
                    "type": "MISSING_PLATFORM_ROOT",
                    "severity": "CRITICAL",
                    "detail": str(root),
                }
            )
            return findings

        if not (root / ".git").exists():
            findings.append(
                {
                    "type": "NO_LOCAL_GIT_METADATA",
                    "severity": "MEDIUM",
                    "detail": (
                        "No .git directory observed at platform root."
                    ),
                }
            )

        if (root / "requirements.txt").exists():
            findings.append(
                {
                    "type": "PYTHON_DEPENDENCY_REVIEW_REQUIRED",
                    "severity": "LOW",
                    "detail": (
                        "Dependency lifecycle and vulnerability review "
                        "should be performed by the execution pipeline."
                    ),
                }
            )

        if (root / "package.json").exists():
            findings.append(
                {
                    "type": "NODE_DEPENDENCY_REVIEW_REQUIRED",
                    "severity": "LOW",
                    "detail": (
                        "Node dependency lifecycle and supply-chain "
                        "review required."
                    ),
                }
            )

        return findings


# =====================================================================
# DECISION ENGINE
# =====================================================================

class DecisionEngine:
    def __init__(self, db: Database):
        self.db = db

    def create(
        self,
        platform_id: Optional[str],
        decision_type: str,
        title: str,
        rationale: str,
        risk_level: str = RiskLevel.MEDIUM.value,
        reversible: bool = True,
        requires_backup: bool = True,
        requires_independent_verification: bool = True,
        requires_legal_review: bool = False,
        requires_owner_action: bool = False,
    ) -> Decision:
        decision = Decision(
            decision_id=str(uuid.uuid4()),
            platform_id=platform_id,
            decision_type=decision_type,
            title=title,
            rationale=rationale,
            risk_level=risk_level,
            reversible=reversible,
            requires_backup=requires_backup,
            requires_independent_verification=(
                requires_independent_verification
            ),
            requires_legal_review=requires_legal_review,
            requires_owner_action=requires_owner_action,
            created_at=utc_now(),
        )

        self.db.conn.execute(
            """
            INSERT INTO decisions(
                decision_id, platform_id, decision_type,
                title, rationale, risk_level, reversible,
                requires_backup, requires_independent_verification,
                requires_legal_review, requires_owner_action,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                decision.decision_id,
                decision.platform_id,
                decision.decision_type,
                decision.title,
                decision.rationale,
                decision.risk_level,
                int(decision.reversible),
                int(decision.requires_backup),
                int(decision.requires_independent_verification),
                int(decision.requires_legal_review),
                int(decision.requires_owner_action),
                decision.created_at,
            ),
        )
        self.db.conn.commit()
        return decision


# =====================================================================
# EXECUTION REQUEST BRIDGE
# =====================================================================

class ExecutionBridge:
    """
    Creates signed-by-hash structured requests for file 02.

    It does not execute shell commands itself.
    """

    def __init__(self, db: Database):
        self.db = db

    def request(
        self,
        platform_id: Optional[str],
        action: str,
        scope: Dict[str, Any],
        reason: str,
        risk_level: str = RiskLevel.MEDIUM.value,
        backup_required: bool = True,
        rollback_required: bool = True,
        independent_verification_required: bool = True,
    ) -> ExecutionRequest:
        request = ExecutionRequest(
            request_id=str(uuid.uuid4()),
            platform_id=platform_id,
            action=action,
            scope=scope,
            reason=reason,
            risk_level=risk_level,
            backup_required=backup_required,
            rollback_required=rollback_required,
            independent_verification_required=(
                independent_verification_required
            ),
            owner_authority=SUPREME_AUTHORITY,
            created_at=utc_now(),
        )

        payload = dataclasses.asdict(request)
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

        request_path = REQUEST_DIR / f"{request.request_id}.json"
        atomic_write_json(request_path, envelope)

        self.db.conn.execute(
            """
            INSERT INTO execution_requests(
                request_id, platform_id, action, scope_json,
                reason, risk_level, backup_required,
                rollback_required,
                independent_verification_required,
                owner_authority, created_at, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request.request_id,
                request.platform_id,
                request.action,
                json_dumps(request.scope),
                request.reason,
                request.risk_level,
                int(request.backup_required),
                int(request.rollback_required),
                int(request.independent_verification_required),
                request.owner_authority,
                request.created_at,
                request.status,
            ),
        )
        self.db.conn.commit()

        self.db.audit(
            "EXECUTION_REQUEST_CREATED",
            request.request_id,
            {
                "action": action,
                "platform_id": platform_id,
                "risk": risk_level,
            },
        )

        return request


# =====================================================================
# ASSURANCE ENGINE
# =====================================================================

class AssuranceEngine:
    def __init__(self, db: Database):
        self.db = db

    def platform_assurance(self, platform_id: str) -> Dict[str, Any]:
        platform_row = self.db.conn.execute(
            "SELECT * FROM platforms WHERE platform_id=?",
            (platform_id,),
        ).fetchone()

        if not platform_row:
            raise KeyError(platform_id)

        risks = self.db.conn.execute(
            """
            SELECT level, COUNT(*) AS n
            FROM risks
            WHERE platform_id=? AND status='OPEN'
            GROUP BY level
            """,
            (platform_id,),
        ).fetchall()

        applicability = self.db.conn.execute(
            """
            SELECT state, COUNT(*) AS n
            FROM applicability
            WHERE platform_id=?
            GROUP BY state
            """,
            (platform_id,),
        ).fetchall()

        critical_risks = sum(
            row["n"]
            for row in risks
            if row["level"] == RiskLevel.CRITICAL.value
        )

        legal_reviews = sum(
            row["n"]
            for row in applicability
            if row["state"]
            == RequirementState.LEGAL_REVIEW_REQUIRED.value
        )

        return {
            "platform_id": platform_id,
            "platform_name": platform_row["name"],
            "observed_state": platform_row["state"],
            "critical_open_risks": critical_risks,
            "legal_reviews_required": legal_reviews,
            "ready_for_launch": False,
            "reason": (
                "Launch readiness is never inferred by file 01 alone. "
                "Executor + independent verifier + evidence are required."
            ),
            "generated_at": utc_now(),
        }


# =====================================================================
# CAPABILITY REGISTRY
# =====================================================================

class CapabilityRegistry:
    CORE_CAPABILITIES = {
        "GLOBAL_DISCOVERY": True,
        "PLATFORM_CLASSIFICATION": True,
        "WORLD_MODEL": True,
        "POLICY_AS_CODE": True,
        "REGULATORY_SOURCE_REGISTRY": True,
        "REGULATORY_CHANGE_DETECTION": True,
        "APPLICABILITY_ENGINE": True,
        "RISK_ENGINE": True,
        "DECISION_ENGINE": True,
        "EXECUTION_REQUEST_GENERATION": True,
        "PHYSICAL_VISIBILITY_MODEL": True,
        "MODERNIZATION_PLANNING": True,

        # Owned by later files:
        "REAL_CODE_EXECUTION": False,
        "REAL_INFRASTRUCTURE_EXECUTION": False,
        "CONTINUOUS_WATCHTOWER": False,
        "INDEPENDENT_RUNTIME_VERIFIER": False,
        "SOVEREIGN_CYBER_DEFENSE": False,
    }

    @classmethod
    def snapshot(cls) -> Dict[str, Any]:
        return {
            "generated_at": utc_now(),
            "capabilities": dict(cls.CORE_CAPABILITIES),
            "rule": (
                "False means not provided by file 01 and must not be "
                "reported as operational until its real component is "
                "installed and independently verified."
            ),
        }


# =====================================================================
# GLOBAL MASTERMIND
# =====================================================================

class MajdMaintenanceMastermind:
    def __init__(self):
        self.db = Database(DB_PATH)

        self.discovery = PlatformDiscovery(self.db)
        self.classifier = PlatformClassifier(self.db)
        self.world = WorldModel(self.db)

        self.registry = IntelligenceRegistry(self.db)
        self.fetcher = IntelligenceFetcher(self.db)
        self.applicability = ApplicabilityEngine(self.db)

        self.risks = RiskEngine(self.db)
        self.policy = PolicyEngine(self.db)
        self.physical = PhysicalInfrastructureModel()
        self.modernization = ModernizationEngine(self.db)

        self.decisions = DecisionEngine(self.db)
        self.executor_bridge = ExecutionBridge(self.db)
        self.assurance = AssuranceEngine(self.db)

    # -----------------------------------------------------------------
    # BOOTSTRAP
    # -----------------------------------------------------------------

    def bootstrap(self) -> Dict[str, Any]:
        LOG.info("MAJD_MASTERMIND_BOOTSTRAP_STARTED")

        source_count = self.registry.seed_defaults()
        constitution_path = self.policy.write_global_constitution()

        capability_path = STATE_DIR / "capabilities.json"
        atomic_write_json(
            capability_path,
            CapabilityRegistry.snapshot(),
        )

        physical_path = STATE_DIR / "physical-visibility.json"
        atomic_write_json(
            physical_path,
            self.physical.snapshot_local_host(),
        )

        result = {
            "app": APP_NAME,
            "file": FILE_NAME,
            "version": VERSION,
            "authority": SUPREME_AUTHORITY,
            "database": str(DB_PATH),
            "sources_seeded": source_count,
            "constitution": str(constitution_path),
            "capabilities": str(capability_path),
            "physical_visibility": str(physical_path),
            "status": "BOOTSTRAPPED",
            "real_execution_status": (
                "NOT_PROVIDED_BY_FILE_01"
            ),
            "timestamp": utc_now(),
        }

        self.db.audit("BOOTSTRAP", APP_NAME, result)
        LOG.info("MAJD_MASTERMIND_BOOTSTRAP_COMPLETED")
        return result

    # -----------------------------------------------------------------
    # DISCOVER
    # -----------------------------------------------------------------

    def discover(self) -> Dict[str, Any]:
        platforms = self.discovery.discover()
        classified = self.classifier.classify_all()
        edges = self.world.rebuild_basic_graph()
        constitutions = self.policy.generate_platform_constitutions()

        return {
            "platforms_discovered": len(platforms),
            "platforms_classified": classified,
            "world_model_edges_updated": edges,
            "platform_constitutions_generated": constitutions,
            "timestamp": utc_now(),
        }

    # -----------------------------------------------------------------
    # RESEARCH
    # -----------------------------------------------------------------

    def research(self) -> Dict[str, Any]:
        """
        Performs safe change detection against configured sources.

        It does not execute content from the web.
        """
        result = self.fetcher.fetch_all()

        return {
            "intelligence": result,
            "security_boundary": (
                "REMOTE_CONTENT_TREATED_AS_UNTRUSTED_DATA"
            ),
            "timestamp": utc_now(),
        }

    # -----------------------------------------------------------------
    # ANALYZE
    # -----------------------------------------------------------------

    def analyze(self) -> Dict[str, Any]:
        applicability_count = self.applicability.evaluate_all()

        platforms = self.db.conn.execute(
            "SELECT * FROM platforms"
        ).fetchall()

        modernization_findings = 0

        for row in platforms:
            findings = self.modernization.assess_platform(row)
            modernization_findings += len(findings)

            for finding in findings:
                severity = finding["severity"]

                likelihood = {
                    "LOW": 2,
                    "MEDIUM": 3,
                    "HIGH": 4,
                    "CRITICAL": 5,
                }.get(severity, 2)

                impact = {
                    "LOW": 2,
                    "MEDIUM": 3,
                    "HIGH": 4,
                    "CRITICAL": 5,
                }.get(severity, 2)

                self.risks.register(
                    platform_id=row["platform_id"],
                    category="MODERNIZATION",
                    title=finding["type"],
                    description=finding["detail"],
                    likelihood=likelihood,
                    impact=impact,
                )

        return {
            "applicability_evaluations": applicability_count,
            "modernization_findings": modernization_findings,
            "timestamp": utc_now(),
        }

    # -----------------------------------------------------------------
    # PLAN
    # -----------------------------------------------------------------

    def plan(self) -> Dict[str, Any]:
        rows = self.db.conn.execute(
            """
            SELECT *
            FROM risks
            WHERE status='OPEN'
            ORDER BY score DESC, created_at ASC
            """
        ).fetchall()

        created = 0

        for row in rows:
            existing = self.db.conn.execute(
                """
                SELECT 1
                FROM decisions
                WHERE platform_id=?
                  AND title=?
                LIMIT 1
                """,
                (
                    row["platform_id"],
                    f"Resolve risk: {row['title']}",
                ),
            ).fetchone()

            if existing:
                continue

            requires_owner = row["level"] == RiskLevel.CRITICAL.value

            self.decisions.create(
                platform_id=row["platform_id"],
                decision_type=DecisionType.PLAN_CHANGE.value,
                title=f"Resolve risk: {row['title']}",
                rationale=row["description"],
                risk_level=row["level"],
                reversible=True,
                requires_backup=True,
                requires_independent_verification=True,
                requires_owner_action=requires_owner,
            )
            created += 1

        return {
            "decisions_created": created,
            "timestamp": utc_now(),
        }

    # -----------------------------------------------------------------
    # BUILD EXECUTION REQUESTS
    # -----------------------------------------------------------------

    def build_execution_requests(self) -> Dict[str, Any]:
        decisions = self.db.conn.execute(
            """
            SELECT d.*
            FROM decisions d
            LEFT JOIN execution_requests r
              ON r.platform_id=d.platform_id
             AND r.reason=d.rationale
            WHERE r.request_id IS NULL
              AND d.requires_legal_review=0
            """
        ).fetchall()

        created = 0

        for decision in decisions:
            if bool(decision["requires_owner_action"]):
                continue

            self.executor_bridge.request(
                platform_id=decision["platform_id"],
                action="ASSESS_AND_REMEDIATE",
                scope={
                    "decision_id": decision["decision_id"],
                    "title": decision["title"],
                    "constraints": {
                        "preserve_required_behavior": True,
                        "preserve_required_data": True,
                        "backup_before_destructive_change": True,
                        "rollback_required": True,
                        "no_fake_success": True,
                        "independent_verification": True,
                    },
                },
                reason=decision["rationale"],
                risk_level=decision["risk_level"],
                backup_required=bool(decision["requires_backup"]),
                rollback_required=True,
                independent_verification_required=bool(
                    decision[
                        "requires_independent_verification"
                    ]
                ),
            )
            created += 1

        return {
            "execution_requests_created": created,
            "executor": (
                "MAJD-MAINTENANCE-EXECUTOR-02.py"
            ),
            "timestamp": utc_now(),
        }

    # -----------------------------------------------------------------
    # STATUS
    # -----------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        platform_count = self.db.conn.execute(
            "SELECT COUNT(*) AS n FROM platforms"
        ).fetchone()["n"]

        source_count = self.db.conn.execute(
            "SELECT COUNT(*) AS n FROM sources WHERE enabled=1"
        ).fetchone()["n"]

        open_risks = self.db.conn.execute(
            """
            SELECT COUNT(*) AS n
            FROM risks
            WHERE status='OPEN'
            """
        ).fetchone()["n"]

        pending_requests = self.db.conn.execute(
            """
            SELECT COUNT(*) AS n
            FROM execution_requests
            WHERE status='PENDING_EXECUTOR'
            """
        ).fetchone()["n"]

        source_changes = self.db.conn.execute(
            """
            SELECT COUNT(*) AS n
            FROM knowledge_events
            WHERE category='SOURCE_CHANGED'
            """
        ).fetchone()["n"]

        return {
            "name": APP_NAME,
            "version": VERSION,
            "authority": SUPREME_AUTHORITY,
            "platforms": platform_count,
            "enabled_intelligence_sources": source_count,
            "observed_source_changes": source_changes,
            "open_risks": open_risks,
            "pending_execution_requests": pending_requests,
            "capabilities": CapabilityRegistry.snapshot(),
            "truth": {
                "mastermind_operational": True,
                "executor_02_verified": False,
                "runtime_03_verified": False,
                "cyber_defense_04_verified": False,
                "continuous_operation_verified": False,
            },
            "timestamp": utc_now(),
        }

    # -----------------------------------------------------------------
    # FULL INTELLIGENCE CYCLE
    # -----------------------------------------------------------------

    def cycle(
        self,
        include_network_research: bool = False,
    ) -> Dict[str, Any]:
        cycle_id = str(uuid.uuid4())
        started = utc_now()

        LOG.info(
            "MAJD_GLOBAL_MAINTENANCE_CYCLE_STARTED | %s",
            cycle_id,
        )

        results: Dict[str, Any] = {
            "cycle_id": cycle_id,
            "started_at": started,
            "bootstrap": self.bootstrap(),
            "discover": self.discover(),
        }

        if include_network_research:
            results["research"] = self.research()
        else:
            results["research"] = {
                "status": "SKIPPED",
                "reason": (
                    "Network research was not requested for this cycle."
                ),
            }

        results["analyze"] = self.analyze()
        results["plan"] = self.plan()
        results["execution_requests"] = (
            self.build_execution_requests()
        )
        results["status"] = self.status()
        results["completed_at"] = utc_now()

        report_path = (
            STATE_DIR /
            f"cycle-{cycle_id}.json"
        )
        atomic_write_json(report_path, results)

        self.db.audit(
            "MAINTENANCE_CYCLE",
            cycle_id,
            {
                "report": str(report_path),
                "network_research": include_network_research,
            },
        )

        LOG.info(
            "MAJD_GLOBAL_MAINTENANCE_CYCLE_COMPLETED | %s",
            cycle_id,
        )

        return results


# =====================================================================
# REPORTING
# =====================================================================

def print_result(payload: Any) -> None:
    print(json_dumps(payload))


# =====================================================================
# CLI
# =====================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=FILE_NAME,
        description=(
            "MAJD sovereign global maintenance mastermind."
        ),
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    sub.add_parser(
        "bootstrap",
        help="Initialize sovereign mastermind state.",
    )

    sub.add_parser(
        "discover",
        help="Discover and classify MAJD platforms.",
    )

    sub.add_parser(
        "research",
        help=(
            "Refresh configured official/authoritative intelligence "
            "sources and detect changes."
        ),
    )

    sub.add_parser(
        "analyze",
        help="Evaluate applicability and platform risks.",
    )

    sub.add_parser(
        "plan",
        help="Create auditable maintenance decisions.",
    )

    sub.add_parser(
        "build-requests",
        help="Create structured requests for executor 02.",
    )

    sub.add_parser(
        "status",
        help="Show truthful mastermind status.",
    )

    cycle_parser = sub.add_parser(
        "cycle",
        help="Run one complete mastermind cycle.",
    )

    cycle_parser.add_argument(
        "--research",
        action="store_true",
        help=(
            "Include HTTPS refresh of configured "
            "official intelligence sources."
        ),
    )

    source_parser = sub.add_parser(
        "add-source",
        help="Add an official/authoritative intelligence source.",
    )

    source_parser.add_argument("--name", required=True)
    source_parser.add_argument("--url", required=True)
    source_parser.add_argument(
        "--authority",
        required=True,
        choices=[x.value for x in SourceAuthority],
    )
    source_parser.add_argument(
        "--jurisdiction",
        required=True,
    )
    source_parser.add_argument(
        "--topic",
        required=True,
    )
    source_parser.add_argument(
        "--notes",
        default="",
    )

    return parser


# =====================================================================
# MAIN
# =====================================================================

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    mastermind = MajdMaintenanceMastermind()

    try:
        if args.command == "bootstrap":
            print_result(mastermind.bootstrap())
            return 0

        if args.command == "discover":
            print_result(mastermind.discover())
            return 0

        if args.command == "research":
            print_result(mastermind.research())
            return 0

        if args.command == "analyze":
            print_result(mastermind.analyze())
            return 0

        if args.command == "plan":
            print_result(mastermind.plan())
            return 0

        if args.command == "build-requests":
            print_result(
                mastermind.build_execution_requests()
            )
            return 0

        if args.command == "status":
            print_result(mastermind.status())
            return 0

        if args.command == "cycle":
            print_result(
                mastermind.cycle(
                    include_network_research=args.research
                )
            )
            return 0

        if args.command == "add-source":
            source_id = mastermind.registry.add_source(
                name=args.name,
                url=args.url,
                authority=args.authority,
                jurisdiction=args.jurisdiction,
                topic=args.topic,
                notes=args.notes,
            )

            print_result(
                {
                    "status": "SOURCE_REGISTERED",
                    "source_id": source_id,
                    "name": args.name,
                    "url": args.url,
                    "timestamp": utc_now(),
                }
            )
            return 0

        parser.error("Unknown command.")
        return 2

    except KeyboardInterrupt:
        LOG.warning("MAJD_MASTERMIND_INTERRUPTED")
        return 130

    except Exception as exc:
        LOG.exception(
            "MAJD_MASTERMIND_FATAL_ERROR | %s",
            exc,
        )

        print_result(
            {
                "status": "FAILED",
                "error_type": type(exc).__name__,
                "error": str(exc),
                "timestamp": utc_now(),
            }
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

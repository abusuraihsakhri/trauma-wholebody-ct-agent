"""
Clinical Data Models & Enums for TraumaScan Sentinel: Pan-Scan Whole-Body CT Injury Severity Scoring Agent.
Domain: Emergency Radiology
Standard: AAST Organ Injury Scaling (OIS) 2018
"""
import datetime
import json
import math

from agents.base import PHIGuard
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class UrgencyLevel(str, Enum):
    ROUTINE = "ROUTINE"
    ADVISORY = "ADVISORY"
    WARNING = "WARNING"
    STAT_CRITICAL = "STAT_CRITICAL"


class ClinicalIntegrityStatus(str, Enum):
    CONCORDANT_NORMAL = "CONCORDANT_NORMAL"
    DISCORDANCE_DETECTED = "DISCORDANCE_DETECTED"
    CRITICAL_ACTION_REQUIRED = "CRITICAL_ACTION_REQUIRED"


@dataclass
class ClinicalCasePayload:
    case_id: str
    patient_synthetic_id: str
    primary_metric: float
    secondary_metric: float
    status_flag: str
    is_stat: bool = False
    clinical_notes: str = ""
    biomarkers: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def __post_init__(self):
        for name in ("primary_metric", "secondary_metric"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or abs(value) > 1e9:
                raise ValueError(f"{name} must be a finite numeric value within safe demonstration bounds")
        PHIGuard.assert_no_phi(json.dumps({
            "case_id": self.case_id,
            "patient_synthetic_id": self.patient_synthetic_id,
            "status_flag": self.status_flag,
            "clinical_notes": self.clinical_notes,
            "biomarkers": self.biomarkers,
        }, default=str))


@dataclass
class AgentAlert:
    alert_id: str
    sub_agent: str
    urgency: UrgencyLevel
    title: str
    clinical_finding: str
    actionable_recommendation: str
    guideline_citation: str = "Synthetic demonstration rules, not an AAST OIS assessment"
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "sub_agent": self.sub_agent,
            "urgency": self.urgency.value,
            "title": self.title,
            "clinical_finding": self.clinical_finding,
            "actionable_recommendation": self.actionable_recommendation,
            "guideline_citation": self.guideline_citation,
            "timestamp": self.timestamp,
        }

"""
Pydantic v2 schemas and data definitions for Trauma Wholebody Ct Agent.
Domain: Radiology & Neuroimaging Systems
Standard: ACR RADS / Fleischner Society / ASPECTS Guidelines
"""
import datetime
import math
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator


class UrgencyLevel(str, Enum):
    ROUTINE = "ROUTINE"
    ELEVATED = "ELEVATED_RISK"
    CRITICAL_STAT = "CRITICAL_STAT_PANIC"


class SystemIntegrityStatus(str, Enum):
    VALIDATED = "VALIDATED_OPTIMAL"
    DISCORDANT = "DISCORDANT_ANOMALY"
    RECALIBRATION_REQUIRED = "RECALIBRATION_REQUIRED"


def _validate_finite_float(value: float, field_name: str) -> float:
    """Ensure metric values are finite numbers within safe bounds."""
    if not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number")
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"{field_name} must be a finite number, got {value}")
    # Clamp to reasonable bounds to prevent overflow in downstream calculations
    if abs(value) > 1e9:
        raise ValueError(f"{field_name} exceeds safe bounds (|value| > 1e9)")
    return float(value)


class SystemTaskPayload(BaseModel):
    task_id: str = Field(..., min_length=1, max_length=128, description="Synthetic task identifier only")
    target_identifier: str = Field(..., min_length=1, max_length=128, description="Synthetic test target identifier only")
    primary_metric: float = Field(..., description="Primary domain measurement or score")
    secondary_metric: float = Field(default=0.0, description="Secondary kinetic or confidence score")
    status_descriptor: str = Field(default="NOMINAL", max_length=256, description="Synthetic status descriptor")
    is_critical_flag: bool = Field(default=False, description="Emergency escalation or high priority trigger")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Metadata key-value pairs")
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    @field_validator("primary_metric")
    @classmethod
    def validate_primary_metric(cls, v):
        return _validate_finite_float(v, "primary_metric")

    @field_validator("secondary_metric")
    @classmethod
    def validate_secondary_metric(cls, v):
        return _validate_finite_float(v, "secondary_metric")


class AgentAlert(BaseModel):
    alert_id: str
    origin_worker: str
    urgency: UrgencyLevel
    summary: str
    technical_details: str
    actionable_remediation: str
    standard_reference: str = "Synthetic demonstration thresholds; no validated clinical standard"
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class ConsensusDossier(BaseModel):
    dossier_id: str
    system_slug: str = "trauma-wholebody-ct-agent"
    domain: str = "Radiology & Neuroimaging Systems"
    task_id: str
    target_identifier: str
    overall_urgency: UrgencyLevel
    integrity_status: SystemIntegrityStatus
    total_alerts: int
    critical_alerts_count: int
    alerts: List[AgentAlert]
    standard_reference: str = "Synthetic demonstration thresholds; no validated clinical standard"
    consensus_summary: str
    audit_hash: str
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

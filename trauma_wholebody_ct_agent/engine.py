"""
Clinical Algorithmic Engine & Guideline Rules for TraumaScan Sentinel: Pan-Scan Whole-Body CT Injury Severity Scoring Agent.
Domain: Emergency Radiology
The numeric limits below are synthetic test values, not AAST OIS criteria.
"""
import math
from typing import Dict, Any, List, Optional
from .models import ClinicalCasePayload, AgentAlert, UrgencyLevel, ClinicalIntegrityStatus


class ClinicalDomainEngine:
    GUIDELINE = "Synthetic threshold demonstrator (not clinical AAST grading)"
    PRIMARY_BASELINE_LIMIT = 20.0
    SECONDARY_ALERT_LIMIT = 10.0

    @classmethod
    def evaluate_primary_index(cls, value: float) -> Optional[Dict[str, Any]]:
        if value > cls.PRIMARY_BASELINE_LIMIT:
            return {
                "title": "Primary Metric Threshold Exceeded",
                "finding": f"Observed value ({value:.2f}) exceeds the synthetic demonstration threshold ({cls.PRIMARY_BASELINE_LIMIT:.1f}).",
                "recommendation": "Review synthetic input values and the demonstration threshold.",
            }
        return None

    @classmethod
    def evaluate_secondary_kinetics(cls, value: float, is_stat: bool) -> Optional[Dict[str, Any]]:
        if value > cls.SECONDARY_ALERT_LIMIT or is_stat:
            return {
                "title": "Synthetic Priority Triggered",
                "finding": f"Kinetic parameter ({value:.2f}) with STAT={is_stat} matches a demonstration priority rule.",
                "recommendation": "Review the synthetic critical flag; this software does not notify clinicians.",
            }
        return None

    @classmethod
    def evaluate_biomarker_concordance(cls, status_flag: str, biomarkers: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        status_upper = str(status_flag).upper()
        if "DISCORDANT" in status_upper or "EQUIVOCAL" in status_upper or "MUTANT" in status_upper:
            return {
                "title": "Synthetic Descriptor Keyword Matched",
                "finding": f"Status flag '{status_flag}' matches a demonstration keyword pattern.",
                "recommendation": f"Review the synthetic descriptor; no clinical test is recommended.",
            }
        return None

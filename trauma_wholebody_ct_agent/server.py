"""
FastAPI REST Application & Webhooks for TraumaScan Sentinel: Pan-Scan Whole-Body CT Injury Severity Scoring Agent.
"""
from typing import Dict, Any, Optional
from .models import ClinicalCasePayload
from .agents import TraumaCoordinator
from agents.base import SecurityException

coordinator = TraumaCoordinator()

def create_app():
    try:
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel

        app = FastAPI(
            title="TraumaScan Sentinel: Pan-Scan Whole-Body CT Injury Severity Scoring Agent",
            description="Synthetic rule-based demonstration only; does not process CT images or score injuries.",
            version="2.0.0-PRO",
        )

        class AuditRequest(BaseModel):
            case_id: str = "CASE-2026-001"
            patient_synthetic_id: str = "SYNTH-PT-881"
            primary_metric: float = 24.5
            secondary_metric: float = 14.0
            status_flag: str = "DISCORDANT"
            is_stat: bool = True
            clinical_notes: str = ""
            biomarkers: Dict[str, Any] = {}

        class ChatRequest(BaseModel):
            query: str

        @app.get("/health")
        def health():
            return {"status": "HEALTHY", "system": "trauma-wholebody-ct-agent", "domain": "Emergency Radiology", "version": "2.0.0-PRO"}

        @app.post("/api/audit")
        def api_audit(req: AuditRequest):
            try:
                payload = ClinicalCasePayload(
                    case_id=req.case_id,
                    patient_synthetic_id=req.patient_synthetic_id,
                    primary_metric=req.primary_metric,
                    secondary_metric=req.secondary_metric,
                    status_flag=req.status_flag,
                    is_stat=req.is_stat,
                    clinical_notes=req.clinical_notes,
                    biomarkers=req.biomarkers,
                )
            except (ValueError, SecurityException):
                raise HTTPException(status_code=422, detail="Invalid synthetic demonstration payload")
            return coordinator.process_case(payload)

        @app.post("/api/chat")
        def api_chat(req: ChatRequest):
            return {"response": coordinator.query_supervisory_chat(req.query)}

        return app
    except ImportError:
        return None

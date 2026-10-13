"""Regression tests for synthetic demo safeguards, audit integrity and CSV handling."""
import csv
import json

import pytest
from fastapi.testclient import TestClient

from agents.base import AuditTrail, SecurityException
from agents.models import SystemTaskPayload, UrgencyLevel
from agents.supervisor import SystemSupervisor
from agents.api import app
from cli import main as system_cli
from trauma_wholebody_ct_agent.cli import main as clinical_cli
from trauma_scan_sentinel import TraumaCoordinator as LegacyCoordinator


def test_audit_verifies_entry_hmac_not_only_previous_hash():
    ledger = AuditTrail(secret_key="test-key-not-for-production")
    ledger.log("tester", "test", "EVENT", {"task_id": "T-001"})
    assert ledger.verify_integrity()
    ledger.logs[0]["event_type"] = "REWRITTEN"
    assert not ledger.verify_integrity()


def test_audit_read_does_not_expose_mutable_internal_records():
    ledger = AuditTrail(secret_key="test-key-not-for-production")
    ledger.log("tester", "test", "EVENT", {"task_id": "T-002"})
    exported = ledger.get_trail()
    exported[0]["event_type"] = "REWRITTEN"
    assert ledger.verify_integrity()
    assert ledger.get_trail()[0]["event_type"] == "EVENT"


def test_supervisor_rejects_phi_hidden_in_attributes():
    supervisor = SystemSupervisor()
    payload = SystemTaskPayload(
        task_id="TEST-003", target_identifier="SYNTH-003", primary_metric=1.0,
        attributes={"nested": {"email": "patient@example.com"}}
    )
    with pytest.raises(SecurityException):
        supervisor.process_task(payload)
    assert len(supervisor.dossier_registry) == 0


def test_api_rejects_phi_without_exposing_content():
    client = TestClient(app)
    data = {
        "task_id": "TEST-004", "target_identifier": "SYNTH-004",
        "primary_metric": 1.0, "attributes": {"person": "person@example.com"}
    }
    res = client.post("/api/audit", json=data)
    assert res.status_code == 422
    assert "person@example.com" not in res.text


def test_api_valid_synthetic_audit():
    client = TestClient(app)
    res = client.post("/api/audit", json={
        "task_id": "TEST-005", "target_identifier": "SYNTH-005",
        "primary_metric": 26, "secondary_metric": 0,
        "is_critical_flag": False, "status_descriptor": "NOMINAL"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["total_alerts"] == 1
    assert data["overall_urgency"] == UrgencyLevel.ELEVATED.value


def test_system_batch_false_is_not_critical(tmp_path):
    source = tmp_path / "input.csv"
    dest = tmp_path / "output.csv"
    source.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "DEMO-1,TEST-1,1,1,False,NOMINAL\n"
        "DEMO-2,TEST-2,1,1,True,NOMINAL\n", encoding="utf-8"
    )
    assert system_cli(["batch", "-i", str(source), "-o", str(dest)]) == 0
    with dest.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["overall_urgency"] == "ROUTINE"
    assert rows[1]["overall_urgency"] == "CRITICAL_STAT_PANIC"


def test_clinical_batch_false_is_not_stat(tmp_path):
    source = tmp_path / "input.csv"
    dest = tmp_path / "output.csv"
    source.write_text(
        "case_id,primary_metric,secondary_metric,status_flag,is_stat\n"
        "DEMO-1,1,1,NORMAL,False\n"
        "DEMO-2,1,1,NORMAL,True\n", encoding="utf-8"
    )
    assert clinical_cli(["batch", "-i", str(source), "-o", str(dest)]) == 0
    with dest.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["stat_critical_alerts"] == "0"
    assert rows[1]["stat_critical_alerts"] == "1"


def test_legacy_dict_false_does_not_trigger_critical_alert():
    result = LegacyCoordinator().audit_case({
        "case_id": "DEMO-3", "metric_primary": 1.0,
        "metric_secondary": 1.0, "critical_flag": "False",
    })
    assert result["critical_count"] == 0

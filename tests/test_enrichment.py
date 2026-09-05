"""
Automated Pytest for trauma-wholebody-ct-agent Enrichment Modules.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from enrichment import (
    OverviewEngine,
    AutomatedOrganInjuryScoringEngine,
    CtProtocolOptimizationEngine,
    HemorrhageDetectionAndQuantificationEngine,
    VascularInjuryAssessmentEngine,
    SurgicalPlanningSupportEngine,
    LongitudinalTraumaFollowupEngine,
    PediatricTraumaAdaptationsEngine,
    TraumawholebodyctagentEnrichmentSuite,
    enrichment_suite,
    BaseEnrichmentEngine,
    EnrichmentResult,
)

def test_enrichment_suite_execution():
    suite = TraumawholebodyctagentEnrichmentSuite()
    res = suite.execute_all(primary_val=0.5, secondary_val=0.2)
    assert len(res) >= 1
    for k, v in res.items():
        assert v.status in ["OPTIMAL", "WARNING", "CRITICAL_ALERT"]
        assert isinstance(v.recommendations, list)

def test_enrichment_threshold_escalation():
    suite = TraumawholebodyctagentEnrichmentSuite()
    res = suite.execute_all(primary_val=10.0, secondary_val=5.0)
    for k, v in res.items():
        assert v.status in ["WARNING", "CRITICAL_ALERT"]
        assert len(v.alerts) > 0


def test_base_enrichment_engine_optimal():
    """Test base engine returns OPTIMAL for values below threshold."""
    engine = BaseEnrichmentEngine(threshold=1.0)
    engine.FEATURE_NAME = "TestEngine"
    result = engine.evaluate(primary_value=0.5, secondary_value=0.1)
    assert result.status == "OPTIMAL"
    assert result.score == 0.5
    assert len(result.alerts) == 0


def test_base_enrichment_engine_warning():
    """Test base engine returns WARNING for values above threshold but below critical."""
    engine = BaseEnrichmentEngine(threshold=1.0)
    engine.FEATURE_NAME = "TestEngine"
    result = engine.evaluate(primary_value=1.5, secondary_value=0.5)
    assert result.status == "WARNING"
    assert len(result.alerts) == 1


def test_base_enrichment_engine_critical():
    """Test base engine returns CRITICAL_ALERT for values above 2x threshold."""
    engine = BaseEnrichmentEngine(threshold=1.0)
    engine.FEATURE_NAME = "TestEngine"
    result = engine.evaluate(primary_value=3.0, secondary_value=1.0)
    assert result.status == "CRITICAL_ALERT"
    assert len(result.alerts) == 1


def test_enrichment_result_dataclass():
    """Test EnrichmentResult dataclass defaults."""
    result = EnrichmentResult()
    assert result.feature_name == "Enrichment"
    assert result.status == "OPTIMAL"
    assert result.score == 0.0
    assert isinstance(result.metrics, dict)
    assert isinstance(result.alerts, list)
    assert isinstance(result.recommendations, list)


def test_enrichment_engine_history():
    """Test that engine history is properly maintained."""
    engine = OverviewEngine(threshold=1.0)
    assert len(engine.history) == 0
    engine.evaluate(primary_value=0.5)
    engine.evaluate(primary_value=3.0)
    assert len(engine.history) == 2
    assert engine.history[0].status == "OPTIMAL"
    assert engine.history[1].status == "CRITICAL_ALERT"

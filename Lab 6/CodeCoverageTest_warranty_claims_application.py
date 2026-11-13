"""
Lab 6 - Stage 1: CODE (line) coverage tests for warranty_claims.py

Goal: execute every line of warranty_claims.py at least once (>= 90% line coverage).

Run:
    coverage run -m pytest CodeCoverageTest_warranty_claims_application.py
    coverage report -m
"""
import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# --------------------------------------------------------------------------
# out_of_warranty_charge
# --------------------------------------------------------------------------

# Starter test: product is still inside its warranty period -> no charge
def test_within_warranty():
    assert out_of_warranty_charge("standard", 20, "defect", False) == 0


# Plan is not one of basic / standard / premium
def test_unknown_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("gold", 10, "defect", False)


# Negative age is invalid
def test_negative_age_raises():
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


# Registered, non-premium plan gets +6 months extra cover:
# basic (12) + 6 = 18 covered, age 20 -> 2 months excess * 100 = 200
def test_registered_basic_gets_extra_cover():
    assert out_of_warranty_charge("basic", 20, "defect", True) == 200


# Accidental claim, more than 12 months out of warranty:
# premium covers 36, age 60 -> excess 24; rate 200 + 50 + 25 = 275 -> 6600
def test_accidental_long_out_of_warranty():
    assert out_of_warranty_charge("premium", 60, "accidental", False) == 6600


# --------------------------------------------------------------------------
# claim_allowed
# --------------------------------------------------------------------------

# Starter test: 60 days since last claim, 1 claim filed, not a recall
def test_claim_allowed():
    assert claim_allowed(60, 1, False) is True


# Recall claims are allowed up to 5 claims filed
def test_recall_claim_allowed():
    assert claim_allowed(0, 3, True) is True


# Last claim was less than 30 days ago -> rejected
def test_claim_rejected_too_soon():
    assert claim_allowed(10, 1, False) is False


# --------------------------------------------------------------------------
# sla_status
# --------------------------------------------------------------------------

# Hardware, not priority: cutoff 48, 100 hours left -> on_track
def test_sla_on_track():
    assert sla_status(100, True, False) == "on_track"


# Software, priority: cutoff 24 + 24 = 48; 40 >= 36 but < 48 -> at_risk
def test_sla_at_risk():
    assert sla_status(40, False, True) == "at_risk"


# Software, priority: cutoff 48; 5 hours left -> critical
def test_sla_critical():
    assert sla_status(5, False, True) == "critical"


# Software, not priority: cutoff 24 (covers the non-hardware / non-priority path)
def test_sla_software_standard():
    assert sla_status(30, False, False) == "on_track"

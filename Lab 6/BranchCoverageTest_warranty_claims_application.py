"""
Lab 6 - Stage 2: BRANCH coverage tests for warranty_claims.py

Goal: make every decision (if / elif / else) evaluate to BOTH True and False
(>= 90% branch coverage; this file reaches 100%). It also tests the boundary
values (the exact numbers where each condition flips) and each part of the
compound condition `is_registered and plan != "premium"`.

Run:
    coverage run --branch -m pytest BranchCoverageTest_warranty_claims_application.py
    coverage report -m
"""
import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# ==========================================================================
# out_of_warranty_charge
# ==========================================================================

# ---- Starter tests -------------------------------------------------------
def test_within_warranty():
    assert out_of_warranty_charge("standard", 20, "defect", False) == 0


def test_claim_allowed():
    assert claim_allowed(60, 1, False) is True


# ---- Decision: plan not in COVERED_MONTHS (True / False) -----------------
def test_unknown_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("gold", 10, "defect", False)


def test_empty_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("", 10, "defect", False)


@pytest.mark.parametrize("plan", ["basic", "standard", "premium"])
def test_known_plans_accepted(plan):
    # False branch of the plan check: no exception for any valid plan
    assert out_of_warranty_charge(plan, 0, "defect", False) == 0


# ---- Decision: age_months < 0 (True / False) -----------------------------
def test_negative_age_raises():
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_zero_age_is_valid():
    # Boundary: 0 is NOT < 0, so no exception
    assert out_of_warranty_charge("basic", 0, "defect", False) == 0


# ---- Decision: is_registered and plan != "premium" -----------------------
# registered=True,  premium=False -> +6 months cover
# registered=True,  premium=True  -> no bonus
# registered=False, premium=False -> no bonus
# registered=False, premium=True  -> no bonus
def test_registered_standard_gets_bonus_boundary():
    # standard 24 + 6 = 30 covered
    assert out_of_warranty_charge("standard", 30, "defect", True) == 0
    assert out_of_warranty_charge("standard", 31, "defect", True) == 100


def test_registered_basic_gets_bonus():
    # basic 12 + 6 = 18 covered: age 18 free, age 19 -> 1 month * 100
    assert out_of_warranty_charge("basic", 18, "defect", True) == 0
    assert out_of_warranty_charge("basic", 19, "defect", True) == 100


def test_registered_premium_gets_no_bonus():
    # premium stays at 36 covered even when registered
    assert out_of_warranty_charge("premium", 36, "defect", True) == 0
    assert out_of_warranty_charge("premium", 37, "defect", True) == 100


def test_unregistered_basic_gets_no_bonus():
    # basic stays at 12 covered: age 18 -> 6 months excess * 100
    assert out_of_warranty_charge("basic", 18, "defect", False) == 600


def test_unregistered_premium_gets_no_bonus():
    assert out_of_warranty_charge("premium", 36, "defect", False) == 0
    assert out_of_warranty_charge("premium", 37, "defect", False) == 100


# ---- Decision: excess <= 0 (True / False) --------------------------------
def test_excess_exactly_zero_returns_zero():
    assert out_of_warranty_charge("standard", 24, "defect", False) == 0


def test_excess_one_is_charged():
    assert out_of_warranty_charge("standard", 25, "defect", False) == 100


def test_age_below_coverage_returns_zero():
    assert out_of_warranty_charge("premium", 10, "accidental", False) == 0


# ---- Decision: claim_type == "accidental" (rate selection) ---------------
def test_defect_claim_base_rate():
    # basic: 13 months old -> excess 1 * rate 100
    assert out_of_warranty_charge("basic", 13, "defect", False) == 100


def test_accidental_claim_base_rate():
    # excess 1 * rate 200
    assert out_of_warranty_charge("basic", 13, "accidental", False) == 200


def test_other_claim_type_uses_default_rate():
    # any claim_type other than "accidental" takes the else branch (rate 100)
    assert out_of_warranty_charge("basic", 13, "water_damage", False) == 100


# ---- Decision: excess > 12 (surcharge) and nested accidental check -------
def test_excess_exactly_12_has_no_surcharge_defect():
    # basic 12 covered, age 24 -> excess 12 (NOT > 12) -> 12 * 100
    assert out_of_warranty_charge("basic", 24, "defect", False) == 1200


def test_excess_exactly_12_has_no_surcharge_accidental():
    # excess 12 (NOT > 12) -> 12 * 200
    assert out_of_warranty_charge("basic", 24, "accidental", False) == 2400


def test_excess_13_defect_gets_surcharge_only():
    # excess 13 > 12 -> rate 100 + 50 = 150; nested accidental check is False
    assert out_of_warranty_charge("basic", 25, "defect", False) == 13 * 150


def test_excess_13_accidental_gets_both_surcharges():
    # excess 13 > 12 -> rate 200 + 50 + 25 = 275
    assert out_of_warranty_charge("basic", 25, "accidental", False) == 13 * 275


def test_large_excess_premium_defect():
    # premium 36 covered, age 60 -> excess 24 * 150
    assert out_of_warranty_charge("premium", 60, "defect", False) == 3600


def test_large_excess_premium_accidental():
    # premium 36 covered, age 60 -> excess 24 * 275
    assert out_of_warranty_charge("premium", 60, "accidental", False) == 6600


# ==========================================================================
# claim_allowed
# ==========================================================================

# ---- Decision: is_recall (True / False) ----------------------------------
@pytest.mark.parametrize(
    "days, filed, expected",
    [
        (0, 0, True),    # recall ignores the 30-day rule
        (0, 5, True),    # boundary: 5 claims is still allowed
        (100, 6, False), # boundary: 6 claims is over the recall limit
    ],
)
def test_recall_claims(days, filed, expected):
    assert claim_allowed(days, filed, True) is expected


# ---- Decision: days_since_last_claim < 30 (True / False) -----------------
@pytest.mark.parametrize(
    "days, filed, expected",
    [
        (0, 0, False),   # same day
        (29, 0, False),  # boundary: 29 < 30 -> rejected even with no claims
        (29, 1, False),
        (30, 0, True),   # boundary: 30 is NOT < 30
        (60, 1, True),   # starter case
    ],
)
def test_non_recall_waiting_period(days, filed, expected):
    assert claim_allowed(days, filed, False) is expected


# ---- Final decision: claims_filed <= 2 (True / False) --------------------
@pytest.mark.parametrize(
    "days, filed, expected",
    [
        (30, 2, True),    # boundary: 2 claims allowed
        (30, 3, False),   # boundary: 3 claims not allowed
        (365, 10, False),
    ],
)
def test_non_recall_claim_limit(days, filed, expected):
    assert claim_allowed(days, filed, False) is expected


# ==========================================================================
# sla_status
# ==========================================================================

# cutoff = 48 (hardware) or 24 (software); +24 if priority.
# on_track : hours_left >= cutoff
# at_risk  : cutoff - 12 <= hours_left < cutoff
# critical : hours_left < cutoff - 12

# ---- hardware, not priority  (cutoff 48) ---------------------------------
@pytest.mark.parametrize(
    "hours, expected",
    [
        (48, "on_track"),   # boundary
        (47, "at_risk"),
        (36, "at_risk"),    # boundary: cutoff - 12
        (35, "critical"),
    ],
)
def test_sla_hardware_normal(hours, expected):
    assert sla_status(hours, True, False) == expected


# ---- software, not priority  (cutoff 24) ---------------------------------
@pytest.mark.parametrize(
    "hours, expected",
    [
        (24, "on_track"),
        (23, "at_risk"),
        (12, "at_risk"),
        (11, "critical"),
        (0, "critical"),
    ],
)
def test_sla_software_normal(hours, expected):
    assert sla_status(hours, False, False) == expected


# ---- software, priority  (cutoff 48) -------------------------------------
@pytest.mark.parametrize(
    "hours, expected",
    [
        (48, "on_track"),
        (47, "at_risk"),
        (36, "at_risk"),
        (35, "critical"),
    ],
)
def test_sla_software_priority(hours, expected):
    assert sla_status(hours, False, True) == expected


# ---- hardware, priority  (cutoff 72) -------------------------------------
@pytest.mark.parametrize(
    "hours, expected",
    [
        (72, "on_track"),
        (71, "at_risk"),
        (60, "at_risk"),
        (59, "critical"),
    ],
)
def test_sla_hardware_priority(hours, expected):
    assert sla_status(hours, True, True) == expected

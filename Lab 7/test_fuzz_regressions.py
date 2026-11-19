"""Regression tests for the crashes found by Hypothesis fuzzing (see FUZZING.md).

Each input below crashed the original warranty_claims.py.
After the fixes, every one returns a safe default instead.
"""
import pytest

from warranty_claims import parse_claim, age_average, payable_charge


@pytest.mark.parametrize("bad_input", [None, "", "abc", "a:b:c", "gold:xyz"])
def test_parse_claim_bad_input_returns_default(bad_input):
    assert parse_claim(bad_input) == ("", 0.0)


@pytest.mark.parametrize("bad_input", [None, "", "a,b", ",,"])
def test_age_average_bad_input_returns_zero(bad_input):
    assert age_average(bad_input) == 0


def test_age_average_skips_empty_values():
    assert age_average("12,,24") == 18


def test_age_average_is_exact_mean():
    assert age_average("12,13") == 12.5


@pytest.mark.parametrize("bad_input", [None, "", "100", "x|y", "1|2|3"])
def test_payable_charge_bad_input_returns_zero(bad_input):
    assert payable_charge(bad_input) == 0


def test_payable_charge_never_negative():
    assert payable_charge("100|500") == 0

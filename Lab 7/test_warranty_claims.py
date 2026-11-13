
import runpy

from hypothesis import given, strategies as st

from warranty_claims import (
    parse_claim,
    age_average,
    payable_charge
)


# Original Hypothesis fuzz tests

@given(st.text() | st.none())
def test_parse_claim_no_crash(s):
    parse_claim(s)


@given(st.text() | st.none())
def test_age_average_no_crash(s):
    age_average(s)


@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
    payable_charge(s)


# Tests for valid inputs

def test_age_average_valid():
    assert age_average("12,24,36") == 24


def test_payable_charge_valid():
    assert payable_charge("1500|200") == 1570


def test_parse_claim_valid():
    assert parse_claim("standard:30") == ("Standard", 30.0)


# Test main function and user interaction

def test_main_execution(monkeypatch, capsys):
    inputs = iter([
        "standard:30",
        "12,24,36",
        "1500|200"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    runpy.run_module("warranty_claims", run_name="__main__")

    output = capsys.readouterr().out

    assert "Plan and Age:" in output
    assert "Average Age:" in output
    assert "Payable Charge:" in output



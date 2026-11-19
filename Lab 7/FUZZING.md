# Lab 7 – Fuzz Testing: Bugs Identified & Fixed

**Student:** Srijan Kumar | **SRN:** PES1UG24CS467  
**Module under test:** `warranty_claims.py`  
**Fuzzing tool:** Hypothesis 6.170.15 with pytest

## 1. Fuzz Test Cases

| Test | Strategy | Function |
|---|---|---|
| `test_parse_claim_no_crash` | `st.text() \| st.none()` | `parse_claim` |
| `test_age_average_no_crash` | `st.text() \| st.none()` | `age_average` |
| `test_payable_charge_no_crash` | `st.text() \| st.none()` | `payable_charge` |

Hypothesis generates random strings (empty, unicode, symbols, very long) and `None`, then shrinks any failure down to the smallest input that still crashes.

Valid-input tests (`test_*_valid`) and `test_main_execution` confirm that correct inputs still give the right answers after the fixes. `test_fuzz_regressions.py` locks in every crash found below so it cannot come back.

## 2. Bugs Identified

All of the following inputs crashed the **original** code. Each was reproduced by running it against the original version of the file.

| # | Function | Failing input | Exception (original code) | Root cause |
|---|---|---|---|---|
| 1 | `parse_claim` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` | No type check before `.split()` |
| 2 | `parse_claim` | `""`, `"abc"` | `ValueError: not enough values to unpack (expected 2, got 1)` | Assumes exactly one `:` |
| 3 | `parse_claim` | `"a:b:c"` | `ValueError: too many values to unpack (expected 2)` | Assumes exactly one `:` |
| 4 | `parse_claim` | `"gold:xyz"` | `ValueError: could not convert string to float: 'xyz'` | Months not validated as a number |
| 5 | `age_average` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` | No type check |
| 6 | `age_average` | `""`, `"12,,24"` | `ValueError: invalid literal for int() with base 10: ''` | Empty CSV values not skipped |
| 7 | `age_average` | `"a,b"` | `ValueError: invalid literal for int() with base 10: 'a'` | Non-numeric ages not handled |
| 8 | `age_average` | empty list after filtering | `ZeroDivisionError` (latent) | `len(values)` can be 0 |
| 9 | `payable_charge` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` | No type check |
| 10 | `payable_charge` | `""`, `"100"` | `ValueError: not enough values to unpack (expected 2, got 1)` | Assumes exactly one `\|` |
| 11 | `payable_charge` | `"1\|2\|3"` | `ValueError: too many values to unpack (expected 2)` | Assumes exactly one `\|` |
| 12 | `payable_charge` | `"x\|y"` | `ValueError: could not convert string to float: 'x'` | Amounts not validated |

## 3. Fixes Applied

| Function | Fix | Safe default |
|---|---|---|
| `parse_claim` | `isinstance(text, str)` check; require exactly 2 parts after `split(":")`; catch `ValueError`/`TypeError` | `("", 0.0)` |
| `age_average` | Type check; strip and skip empty values; return 0 if no values remain (removes divide-by-zero); catch `ValueError`/`TypeError` | `0` |
| `payable_charge` | Type check; require exactly 2 parts after `split("\|")`; catch `ValueError`/`TypeError`; result still clamped with `max(total, 0)` | `0` |

**Behaviour change to note:** `age_average` now uses `/` instead of `//`, so it returns the exact mean (e.g. `"12,13"` → `12.5` instead of `12`). Inputs that divide evenly, like `"12,24,36"` → `24`, are unchanged.

## 4. Results

- **Before the fixes:** all 3 fuzz tests failed within a few generated examples.
- **After the fixes:** all fuzz, valid-input, main-execution and regression tests pass.
- **Coverage:** 100% statement coverage of `warranty_claims.py` (see `screenshots/coverage_report.png` and `screenshots/html_coverage.png`).

## 5. How to Run

```bash
pip install pytest hypothesis coverage
coverage run -m pytest -v
coverage report -m warranty_claims.py
```

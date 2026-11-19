# Lab 7 – Fuzz Testing (Warranty Claims)

**Student:** Srijan Kumar | **SRN:** PES1UG24CS467

A small Python module that parses warranty claims, averages product ages and works out the payable repair charge after a discount. Hypothesis fuzz tests were used to find input-validation bugs, which were then fixed.

## Files

| File | Description |
|---|---|
| `warranty_claims.py` | Module under test, with input-validation fixes |
| `test_warranty_claims.py` | Hypothesis fuzz tests, valid-input tests and a `main()` test |
| `test_fuzz_regressions.py` | Regression tests for every crash found by fuzzing |
| `FUZZING.md` | Bugs identified, root causes, fixes and results |
| `screenshots/` | Test run, coverage report and HTML coverage |

## Summary

- **Fuzz test cases:** 3 Hypothesis tests using `st.text() | st.none()`
- **Bugs identified & fixed:** 12 crashing inputs across all 3 functions (`AttributeError`, `ValueError`, `ZeroDivisionError`)
- **Coverage:** 100% statement coverage of `warranty_claims.py`

## Run

```bash
pip install pytest hypothesis coverage
coverage run -m pytest -v
coverage report -m warranty_claims.py
```

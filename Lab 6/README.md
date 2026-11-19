# Lab 6 – Code and Branch Coverage (Warranty Claims)

**Student:** Srijan Kumar | **SRN:** PES1UG24CS467

A small Python module that works out out-of-warranty repair charges by plan, product age and claim type, checks whether a claim can be filed, and reports how close a claim is to missing its service deadline.

## Files

| File | Description |
|---|---|
| `warranty_claims.py` | Module under test |
| `test_warranty_claims.py` | Starter test file (2 example tests) |
| `CodeCoverageTest_warranty_claims_application.py` | Stage 1: 12 tests for statement coverage |
| `BranchCoverageTest_warranty_claims_application.py` | Stage 2: 54 tests for branch coverage, including boundary values and both sides of the compound condition |
| `screenshots/code_coverage.png` | Statement coverage report |
| `screenshots/branch_coverage.png` | Branch coverage report |

## Results

| Report | Tests | Statements | Branches | Coverage |
|---|---|---|---|---|
| Code (statement) coverage | 12 passed | 37 / 37 | – | **100%** |
| Branch coverage | 54 passed | 37 / 37 | 26 / 26 (0 partial) | **100%** |

The target was 90–100%. Both reports reached 100%.

## What the Branch Tests Cover

- **`out_of_warranty_charge`:** unknown plan, negative age, each plan's warranty limit, the registration bonus (`is_registered and plan != "premium"` tested with each part true and false), within vs. out of warranty, accidental vs. defect rates, and the `excess > 12` surcharge on both sides of the boundary.
- **`claim_allowed`:** recall vs. non-recall, the 30-day boundary (29 / 30 days), and the claim-count limits (2 / 3 and 5 / 6).
- **`sla_status`:** hardware vs. software, priority vs. normal, and the exact cut-off values for `on_track`, `at_risk` and `critical`.

## Run

```bash
pip install pytest coverage
coverage erase
coverage run -m pytest CodeCoverageTest_warranty_claims_application.py
coverage report -m warranty_claims.py

coverage erase
coverage run --branch -m pytest BranchCoverageTest_warranty_claims_application.py
coverage report -m warranty_claims.py
```

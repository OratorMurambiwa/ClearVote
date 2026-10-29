# ClearVote Backend

The backend currently contains text preprocessing and its unit tests. There is no API server to start yet. `POST /analyze` is defined in the [API contract](../docs/api-contract.md), but is not implemented as an HTTP endpoint.

## Prerequisites

- Python 3 (the test command below has been verified with Python 3.12).
- A local clone of this repository (see the [root setup guide](../README.md#getting-started)).

The current code uses only the Python standard library. No package installation, virtual environment, API keys, or environment variables are required to run these tests.

## Run the Tests

From the repository root (the directory containing `backend/`), run:

```bash
python3 -m unittest backend.tests.TestAnalyzeRequestPreprocessor
```

Expected output includes `Ran 7 tests` and `OK`. The tests cover valid input, whitespace normalization, empty and non-string input rejection, and the 5,000-character limit.

If your Python 3 executable is named `python` (common on Windows), substitute `python` for `python3`. If the command cannot import `backend`, check that your terminal is in the repository root rather than inside `backend/`.

## Current Behavior

`AnalyzeRequestPreprocessor.preprocess_text()` collapses whitespace, rejects empty or non-string input, and rejects text longer than 5,000 characters after normalization. Invalid input raises `ValueError`.

These tests verify preprocessing only. Claim detection, evidence retrieval, HTTP error responses, and extension-to-backend integration remain future work.

# ClearVote Backend

FastAPI backend for the ClearVote browser extension and results page.

## Requirements

- Python 3.11+
- pip

## Install Dependencies

From the project root:

```powershell
pip install -r backend\requirements.txt
```

## Run the Backend

From the project root:

```powershell
python -m uvicorn backend.app.main:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

## Health Check

With the backend running, open:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "environment": "development"
}
```

## Run Preprocessing Tests

From the project root:

```powershell
python -m unittest backend.tests.TestAnalyzeRequestPreprocessor
```

Expected output includes:

```text
Ran 7 tests
OK
```

The preprocessing tests cover:

- valid text input
- whitespace normalization
- empty input rejection
- non-string input rejection
- the 5,000-character request limit

## Environment Configuration

`backend/.env.example` documents the environment variables used by the backend.

Current configuration includes:

```text
CLEARVOTE_ENV=development
CLEARVOTE_ALLOWED_ORIGIN=*
```

A local `.env` file can be added later when environment-specific configuration or secrets are required.

Do not commit `.env` files, API keys, or other secrets.

## Current Backend Features

The backend currently includes:

- FastAPI application setup
- `/health` endpoint
- application configuration
- request text preprocessing
- whitespace normalization
- input validation
- 5,000-character request limit

The full `/analyze` endpoint, claim detection, evidence retrieval, and verification pipeline will be implemented in later tasks.
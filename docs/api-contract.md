# ClearVote Analyze API Contract
## Purpose
This document defines how the ClearVote browser extension, results page, backend, and AI pipeline communicate.
The frontend sends text for analysis. The backend returns a structured result with the identified claim, result status, explanation, and evidence sources.
This contract should stay stable even if internal AI models, APIs, or retrieval tools change.
## Endpoint
### `POST /analyze`
Analyzes a piece of text for a political or check-worthy claim.
### Request
```json
{
  "text": "The unemployment rate doubled last year."
}
```
### Request Fields
| Field | Type | Required | Description |
|---|---|---|---|
| `text` | string | Yes | The smallest relevant passage or claim to analyze. |
### Request Rules
- `text` cannot be empty.
- Send only the text needed for analysis.
- Avoid sending an entire webpage when a smaller passage is enough.
- Do not include passwords, cookies, tokens, form values, or unnecessary private information.
- The backend may reject requests that exceed the allowed size.
## Successful Response
```json
{
  "claim": "The unemployment rate doubled last year.",
  "status": "CONFLICTING_EVIDENCE",
  "assessment": "Available evidence does not fully support this claim.",
  "explanation": "Reliable sources report different figures for the period referenced in the claim.",
  "sources": [
    {
      "title": "Employment Situation Report",
      "publisher": "Example Publisher",
      "url": "https://example.com/report",
      "published_date": "2026-10-10",
      "snippet": "Relevant evidence from the source."
    }
  ]
}
```
## Response Fields
| Field | Type | Description |
|---|---|---|
| `claim` | string or null | Main factual claim identified from the submitted text. |
| `status` | string | Evidence-based result state. |
| `assessment` | string | Short user-facing summary. |
| `explanation` | string | Clear explanation of what the evidence shows. |
| `sources` | array | Sources used in the analysis. |
## Result States
- `RELEVANT_FACT_CHECK` — a fact check directly matching the claim was found.
- `RELATED_FACT_CHECK` — a related fact check was found, but it is not an exact match.
- `SUPPORTING_EVIDENCE` — reliable evidence supports the claim.
- `CONFLICTING_EVIDENCE` — reliable evidence conflicts with the claim or reliable sources disagree.
- `NOT_ENOUGH_EVIDENCE` — there is not enough reliable evidence to make a useful assessment.
- `NO_CHECKABLE_CLAIM` — the submitted text does not contain a clear factual claim that can be verified.
- `VERIFICATION_UNAVAILABLE` — the system could not complete verification because a required service or model was unavailable.
ClearVote should avoid simple true/false labels and should return uncertainty when the evidence does not support a definitive conclusion.

## Source Object
```json
{
  "title": "Source title",
  "publisher": "Publisher name",
  "url": "https://example.com",
  "published_date": "2026-10-10",
  "snippet": "Relevant evidence from the source."
}
```

### Source Fields
| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string or null | No | Source title. |
| `publisher` | string or null | No | Organization or publisher. |
| `url` | string | Yes | Link to the original source. |
| `published_date` | string or null | No | Publication date when available. |
| `snippet` | string or null | No | Short relevant evidence excerpt. |
Optional fields may be `null` when a provider does not supply them.

## Example: Not Enough Evidence
```json
{
  "claim": "Example claim.",
  "status": "NOT_ENOUGH_EVIDENCE",
  "assessment": "ClearVote could not find enough reliable evidence to assess this claim.",
  "explanation": "The available sources did not directly address the claim.",
  "sources": []
}
```

## Example: No Checkable Claim
```json
{
  "claim": null,
  "status": "NO_CHECKABLE_CLAIM",
  "assessment": "No clear factual claim was identified.",
  "explanation": "The submitted text does not contain a claim that can be directly verified.",
  "sources": []
}
```

## Error Response
```json
{
  "error": "INVALID_REQUEST",
  "message": "Text is required."
}
```

Supported error types:
- `INVALID_REQUEST`
- `TEXT_TOO_LONG`
- `ANALYSIS_FAILED`
- `SERVICE_UNAVAILABLE`
## Privacy Requirements
### Frontend
- Send only the minimum text required for analysis.
- Avoid hidden page content and unnecessary private-page data.
- Never send passwords, cookies, authentication tokens, or form values.
- Avoid sending precise location, health, financial, private email, or message content.
### Backend
- Keep API keys and credentials server-side.
- Avoid permanently storing full webpage content or browsing history.
- Avoid creating political-affiliation profiles.
- Keep logs minimal.
- Avoid putting sensitive webpage text in URLs.
- Use HTTPS in production.
## Frontend Expectations
The frontend should handle every supported result state and should not assume every analysis will produce a definitive answer.
The popup and results page should display the claim, result status, short assessment, explanation, and sources.

## Backend Expectations
The backend should:
1. Validate the request.
2. Identify a political or check-worthy claim.
3. Retrieve relevant fact checks or evidence.
4. Match evidence to the claim.
5. Verify the claim using the selected pipeline.
6. Generate an evidence-grounded explanation.
7. Normalize source data.
8. Return the response using this contract.
The exact models and providers may change after benchmarking.

## MVP Principle
The frontend should not depend on a specific AI model, retrieval API, or LLM.
ClearVote should be able to replace internal tools without changing the API contract.
The system should communicate what the available evidence shows and return uncertainty when evidence is insufficient, conflicting, or unavailable.

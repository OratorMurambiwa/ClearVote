# ClearVote MVP — APIs, Models, and Datasets Research
**Research period:** September–October 2026

## 1. MVP Direction
ClearVote should use an evidence-based pipeline instead of one model deciding whether political content is true or false.

```text
Webpage text → political/civic detection → claim detection → fact-check search
→ current evidence retrieval → claim/evidence matching → verification
→ explanation + sources + uncertainty
```

A ClearVote warning should mean **review the evidence**, not automatically **this is false**.

## 2. Fact-Check and Retrieval APIs

### Google Fact Check API
**Use:** Search for existing fact checks.
- Strengths: purpose-built; can return publisher, reviewed claim, rating, date, and source link.
- Limitations: claims may have no match; results may be old or partial; no result does not mean true.
- **MVP priority:** High. Test as the first lookup.

### GDELT
**Use:** Find recent reporting and multiple sources related to a claim.
- Strengths: broad coverage, public API, useful when no direct fact check exists.
- Limitations: results do not prove a claim; relevance/source quality still need filtering; rate limits matter.
- **MVP priority:** High retrieval candidate.

### Tavily
**Use:** Retrieve current web evidence.
- Strengths: designed for AI retrieval workflows and current information.
- Limitations: relevance, pricing, and request limits need testing.
- **MVP priority:** Benchmark against GDELT.

### Other Retrieval Options
- **Brave Search API:** broader web search; useful for official and primary sources.
- **Exa:** semantic search when keyword matching is weak.
- **NewsAPI:** easy REST API, but free access is limited and not ideal for production.
- **Google Custom Search JSON API:** not recommended as a new core dependency.

## 3. Political Content Detection
Candidates:
- BART-large-MNLI
- DeBERTa-v3 zero-shot models
- nli-deberta-v3-base

Purpose: decide whether a page contains political/civic content before running the full pipeline. This stage should not decide truth.

## 4. Check-Worthy Claim Detection
Candidates:
- spaCy + rules
- BERT ClaimBuster
- mDeBERTa ClaimBuster
- LLM claim extraction

**Sprint 2 comparison:** ClaimBuster vs mDeBERTa vs LLM. Measure extraction quality, false positives, latency, and cost.

## 5. Claim Matching
Candidate embedding models:
- all-MiniLM-L6-v2
- E5-small-v2
- BGE-small-en-v1.5

Purpose: determine whether a retrieved article or fact check matches the exact claim, not merely the same topic.

## 6. Evidence Verification
Candidates:
- DeBERTa-v3-base-MNLI-FEVER-ANLI
- nli-deberta-v3-base
- RoBERTa-large-MNLI
- LLM using retrieved evidence

Possible outputs: **SUPPORTED, REFUTED, NOT ENOUGH INFORMATION, CONFLICTING EVIDENCE**.

**Sprint 2 comparison:** DeBERTa vs RoBERTa vs evidence-grounded LLM.

## 7. LLM Use
Candidates:
- Gemini Flash
- GPT-4.1 mini
- Claude Haiku

Useful for claim extraction, splitting compound claims, search-query generation, evidence summaries, structured JSON, and user-facing explanations.

LLMs should not be treated as the source of truth. Explanations must be grounded in retrieved evidence.

## 8. Datasets
- **AVeriTeC:** real-world claims with online evidence; best for end-to-end evidence verification.
- **FEVER:** large Supported/Refuted/Not Enough Information benchmark; best for NLI and verification.
- **ClaimBuster:** useful for check-worthy claim detection evaluation.
- **LIAR:** labeled political statements from PolitiFact; useful for political-claim experiments, not as a live source of truth.
- **MultiFC:** combines multiple fact-checking organizations; useful for testing generalization across labeling systems.
- **FakeNewsNet:** political/news and social-context data; lower priority for the MVP.

## 9. Sprint 2 Candidates
- **Claim detection:** BERT ClaimBuster, mDeBERTa ClaimBuster, LLM extraction.
- **Existing fact checks:** Google Fact Check API.
- **Evidence retrieval:** GDELT, Tavily; Brave/Exa if needed.
- **Claim matching:** MiniLM, E5, BGE.
- **Evidence verification:** DeBERTa-FEVER-ANLI, RoBERTa-MNLI, evidence-grounded LLM.
- **Evaluation:** AVeriTeC, FEVER, ClaimBuster, LIAR, plus a small set of current political examples.

## 10. Product Safety Principle
ClearVote should avoid definitive labels based only on a model score.

Preferred result states:
- Relevant fact check found
- Related fact check found
- Supporting evidence found
- Conflicting evidence found
- Not enough evidence found
- No checkable claim identified
- Verification unavailable

The result should show the exact claim, why it was flagged, evidence, source links, dates, and remaining uncertainty.

## 11. Current Recommendation
Do not train a custom misinformation model yet.

```text
Extension → claim detection → Google Fact Check → live evidence retrieval
→ claim matching → verification → explanation → ClearVote results page
```

Do not lock in FastAPI, Gemini, GDELT, DeBERTa, or any other final stack choice until Sprint 2 benchmarking is complete.

## References
1. Google Fact Check Tools API — https://developers.google.com/fact-check/tools/api
2. GDELT Data and APIs — https://gdeltproject.org/data.html
3. GDELT DOC 2.0 API — https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
4. NewsAPI Pricing — https://newsapi.org/pricing
5. Gemini API Docs — https://ai.google.dev/gemini-api/docs
6. DeBERTa-v3-base — https://huggingface.co/microsoft/deberta-v3-base
7. DeBERTa MNLI/FEVER/ANLI — https://huggingface.co/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli
8. LIAR Dataset — https://github.com/tfs4/liar_dataset
9. AVeriTeC — https://fever.ai/dataset/averitec.html
10. FEVER — https://fever.ai/dataset/fever.html
11. FakeNewsNet — https://github.com/KaiDMML/FakeNewsNet

## Benchmarking Plan

Use this section when completing Milestone 2 benchmarking tasks.  
All candidates within the same benchmark should be tested on the same examples whenever possible.

| Benchmark | Candidates | Measure |
|---|---|---|
| Political-content detection | BART-large-MNLI, DeBERTa-v3 zero-shot, nli-deberta-v3-base | Precision, recall, F1, false positives, latency |
| Check-worthy claim detection | BERT ClaimBuster, mDeBERTa ClaimBuster, LLM claim extraction | Precision, recall, F1, extraction quality, false positives, latency, cost |
| Live evidence retrieval | GDELT, Tavily; Brave/Exa if needed | Relevant-result rate, coverage, recency, latency, API limits, estimated cost |
| Claim-to-evidence matching | MiniLM, E5-small-v2, BGE-small-en-v1.5 | Correct evidence ranking, Precision@K, Recall@K, similarity threshold behavior, latency |
| Evidence verification | DeBERTa-FEVER-ANLI, RoBERTa-MNLI, evidence-grounded LLM | Accuracy, precision, recall, F1, false confident answers, latency, cost |
| LLM explanation | Gemini Flash, GPT-4.1 mini, Claude Haiku | Evidence groundedness, citation support, structured-output reliability, latency, cost |
| AI runtime/provider | Local Hugging Face inference vs shortlisted hosted APIs | Model support, latency, CPU/GPU/RAM requirements, reliability, cost, integration effort |
| Fact-check/evidence quality | Google Fact Check plus selected live retrieval APIs | Coverage, relevance, recency, source quality, no-result rate, latency |

### Shared Evaluation Data

Use:
- AVeriTeC for evidence-based verification
- FEVER for claim/evidence verification
- ClaimBuster data for claim-detection testing
- LIAR for additional political-claim examples
- A small manually reviewed set of current political examples

### Required Benchmark Output

Each benchmark should produce a short comparison table containing:

| Candidate | Main Quality Metric | Latency | Cost / Compute | Important Failure | Recommendation |
|---|---:|---:|---:|---|---|

The person completing the benchmark should recommend one option for the MVP and briefly explain why.

### Benchmarking Rules

- Test candidates on the same examples.
- Record model/API version used.
- Record important configuration or thresholds.
- Do not select a model using accuracy alone.
- Track false positives and false confident answers.
- Record cases where the system correctly abstains.
- Keep raw benchmark results so another team member can reproduce the comparison.

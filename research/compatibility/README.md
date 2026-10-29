# Backend tool compatibility — issue #10

Assessment started October 29, 2026. **Partial findings; not ready to close #10.**

## Baseline and scope

The checked-in main branch has preprocessing but no server. [PR #54](https://github.com/OratorMurambiwa/ClearVote/pull/54), revision `d41781ba2e791fafb140d1e4dd4b03833fb890e3`, proposes Python 3.11+, FastAPI, Uvicorn, environment-variable configuration, and `/health`. It is the provisional baseline; the team still needs to approve/merge it. Its requirements are unpinned. This spike does not change production dependencies or implement #30/#40/#41.

Compatibility means the tool can be called from this backend with manageable dependencies and failure handling. Retrieval quality, model accuracy, latency, and cost comparisons belong to the dedicated benchmarking issues. Passing a fixture does not verify real credentials, quotas, provider responses, or deployment suitability.

## Findings and recommendation

| Candidate | Integration and dependencies | Evidence so far | Complexity / limitation | Recommendation |
|---|---|---|---|---|
| Google Fact Check | Async HTTPX GET to `claims:search`; API key server-side; no Google SDK required | Provider-shaped JSON, missing claims, HTTP 429 and timeout fixtures pass; authenticated call pending | Low adapter effort; nested reviews, pagination, missing fields, no match and service failures need separate handling | First fact-check integration (#30), conditional on live access |
| GDELT DOC | Async HTTPX GET; JSON article-list mode | Live public request attempted; see results JSON for status | Low HTTP effort, medium query/normalization effort; endpoint availability and non-JSON errors need handling | Keep as candidate, not selected as reliable fallback yet |
| Tavily | `tavily-python`, `AsyncTavilyClient`; alternatively HTTPX REST | Installed alongside FastAPI; async search symbol imports; authenticated call pending | Low/medium; SDK adds dependencies, quotas and response fields need live checks | Compare with GDELT in #31/#32 before selecting |
| MiniLM / E5 / BGE embeddings | `sentence-transformers` plus PyTorch/Transformers | All three loaded on CPU and produced finite normalized 384-dimensional vectors; exact revisions in embedding-results.json | Medium; model downloads, token limits, batch sizes and memory per worker. E5 requires query/passage prefixes; BGE has retrieval instruction guidance | All three are technically viable on this CPU environment; compare quality in #35 |
| Political detection / NLI | Transformers/PyTorch; some DeBERTa tokenizers may need SentencePiece | Documentation review only; exact checkpoints and inference pending | Medium/high; tokenization, label mappings, truncation and model memory must be checked per checkpoint | Test exact model revisions before admitting to pipeline |
| spaCy + rules | `spacy` and a separately installed language pipeline if required | Documentation review only | Medium; rules baseline does not establish check-worthiness | Retain as inexpensive baseline for #34 |
| BERT/mDeBERTa ClaimBuster | Need exact checkpoint IDs, licenses and supported loading code | Research names are not unique reproducible identifiers | Unresolved until checkpoints are selected | Obtain exact IDs before testing |
| Gemini Flash / GPT-4.1 mini / Claude Haiku | Hosted API via provider SDK or HTTP; credentials and exact model IDs required | Not executed; no credentials/budget available | Medium; structured JSON validation, evidence grounding, timeouts, quotas, privacy and model availability | Defer selection to #38; do not create all accounts now |
| Brave / Exa / NewsAPI | REST or SDK with provider credentials | Not executed; secondary candidates in existing research | More provider-specific quotas, terms and adapters | Defer unless primary candidates fail |

The simplest provisional integration is FastAPI with a shared async HTTPX client for external retrieval, plus separate optional model dependencies. This is an engineering recommendation from interface shape and local checks, not a completed benchmark decision.

CPU inference must not run directly in an async route's event loop. Use a bounded executor or separate inference worker and measure concurrency. Load models once per worker; additional Uvicorn workers duplicate model memory. Persist model caches on hosts that support them. A container/worker option needs comparison with hosted inference in #37/#45 before deployment is selected. Enforce finite provider timeouts, bounded retries for transient failures, response-size limits and cancellation. Provider failure must remain distinguishable from an empty result.

Normalize provider responses into the shared source contract in #41. Fact-check ratings are provider judgments; article metadata and similarity scores alone are not verification. Keep secrets and raw query URLs out of logs; provider search APIs can put queries in URLs even though the frontend sends `POST /analyze`.

## Reproduce the HTTP spike

From the repository root, create an isolated environment and install the recorded dependencies:

```bash
python3 -m venv /tmp/clearvote-compat-venv
/tmp/clearvote-compat-venv/bin/pip install -r research/compatibility/http-requirements.txt
/tmp/clearvote-compat-venv/bin/python research/compatibility/check_http.py
```

The script checks a replicated scaffold health route via ASGI, HTTPX fixtures, the Tavily async interface import, and one public GDELT query (`election`, last 24 hours, at most five articles). It does not import or certify the unmerged scaffold itself. No private page text, credentials, provider bodies or raw URLs are saved. A GDELT availability failure is recorded rather than treated as a quality result. Assertions fail the process on local check errors.

`http-results.json` records the observed interpreter and primary package versions; `http-requirements.txt` records the full HTTP environment. No Python 3.11 or deployment-host run has been performed.

For the additional CPU embedding checks, install CPU PyTorch first, then the rest of the recorded environment:

```bash
/tmp/clearvote-compat-venv/bin/pip install torch==2.15.0+cpu --index-url https://download.pytorch.org/whl/cpu
/tmp/clearvote-compat-venv/bin/pip install -r research/compatibility/model-requirements.txt
HF_HOME=/tmp/clearvote-model-cache HF_HUB_DISABLE_PROGRESS_BARS=1 /tmp/clearvote-compat-venv/bin/python research/compatibility/check_embeddings.py
```

This downloads public models and needs disk space and outbound Hugging Face access. The script resolves and records each model revision before loading. Repeat runs resolve the then-current revision, so use the recorded revisions for a strict comparison. It checks finite normalized vectors for two synthetic texts, not retrieval quality. Timings include local conditions and are not benchmark results. Peak RSS is cumulative for the process on Linux, not isolated model memory. The combined Python environment passed `pip check`.

## Credentials: next user action

Start with Google only:

1. Sign into Google Cloud Console and select a team-owned project, or create a project approved for ClearVote.
2. In APIs & Services, enable **Fact Check Tools API**.
3. Create an API key in Credentials. Restrict it to that API; use server IP restrictions when a stable deployment IP is available. Review the console's current quotas and any billing requirements before enabling spend.
4. Store it locally as `GOOGLE_FACT_CHECK_API_KEY`, a convention for the future adapter. Keep it out of chat, source control and extension code. This spike does not yet read the key.
5. Tell the developer that the key is available and agree a small request limit before authenticated probes are added.

Google documents an API key for claim search. Search Console site ownership is for ClaimReview writing, which ClearVote does not need for search.

Tavily is optional next: create a team-approved account at its dashboard, obtain an API key, check the currently offered credits/limits, and store it as `TAVILY_API_KEY`. Do not enable paid usage for this assessment without a budget decision. No LLM credentials are required to continue local compatibility work.

## Remaining acceptance work

- Confirm the provisional backend stack after review of #54.
- Run authenticated Google and, if approved, Tavily probes; verify success, empty results, authorization and quota behavior without deliberately exhausting quotas.
- Select exact ClaimBuster and NLI checkpoint IDs/revisions and check licenses.
- Extend the completed embedding smoke checks to NLI loading/inference; record label mappings and truncation behavior. Measure isolated model memory and warm/cold behavior on the deployment candidate. No quality ranking until shared benchmark data exists.
- Check one chosen hosted LLM interface only after the team chooses a candidate and budget.
- Update this report and its recommendation, then request team review before closing #10.

## Primary sources

- [Google Fact Check setup](https://developers.google.com/fact-check/tools/api) and [claim search reference](https://developers.google.com/fact-check/tools/api/reference/rest/v1alpha1/claims/search)
- [GDELT DOC documentation](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)
- [Tavily Python SDK](https://github.com/tavily-ai/tavily-python) and [onboarding](https://docs.tavily.com/)
- [Sentence Transformers installation](https://sbert.net/docs/installation.html)
- Model cards: [MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), [E5](https://huggingface.co/intfloat/e5-small-v2), [BGE](https://huggingface.co/BAAI/bge-small-en-v1.5), [DeBERTa NLI](https://huggingface.co/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli)
- [spaCy installation](https://spacy.io/usage)

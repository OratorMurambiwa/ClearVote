ClearVote MVP --- APIs, AI Models, and Datasets Research

Research date: September 29, 2026

1. MVP context

ClearVote's MVP is intended to analyze text-based political content,
identify content that may require additional verification, and give the
user useful context and links to supporting sources.

The MVP does not need to prove every political statement true or
false. A safer and simpler architecture is:

Extract the main claim from the selected text.

Search for existing fact checks and relevant reporting.

Compare the claim against retrieved evidence.

Produce a short explanation with citations.

Flag content when the evidence/retrieval pipeline finds a meaningful
reason for further review.

Clearly distinguish "flagged for review" from a definitive claim
that something is misinformation.

This reduces the risk of relying on a single classifier to make a
political truth judgment.

2. APIs

2.1 Google Fact Check Tools --- Claim Search API

Use case: Search for existing fact checks matching a political
claim.

Google's Fact Check Claim Search API exposes the same set of fact-check
results available through Fact Check Explorer and can also be used to
retrieve updates for a query. It requires an API key. [1]

What ClearVote could use it for

When a user selects text such as:

"Candidate X voted to eliminate Social Security."

ClearVote could extract the claim and query the Fact Check API. If an
existing fact check matches the claim, the extension can show:

fact-check publisher

rating/verdict supplied by that publisher

fact-check URL

date

matching claim

Cost / limits

Google's public documentation requires an API key but does not state a
simple fixed public price on the Fact Check Tools API documentation
page. Quotas should therefore be checked in the Google API/Cloud
console before production deployment. [1]

Advantages

Directly designed for fact-check retrieval.

More useful for ClearVote than a generic fake-news classifier when a
claim has already been fact-checked.

Returns existing fact-check results rather than asking an AI model
to invent a verdict.

Straightforward HTTP API integration with a Python/FastAPI backend.

Limitations

A claim may have no matching fact check.

Existing fact checks may be old or may cover only part of a claim.

The API does not eliminate the need to evaluate the quality and
relevance of the retrieved evidence.

Fact-check labels come from the organizations that published the
fact checks; ClearVote should attribute them rather than silently
converting them into its own political judgment.

MVP assessment: High value. Use as the first verification
source.

2.2 GDELT DOC 2.0 API

Use case: Find recent news coverage and multiple sources discussing
the same claim/topic.

GDELT provides real-time APIs for news monitoring. Its DOC 2.0 API
supports keyword and phrase search over news and can search English
machine translations of coverage in many languages. GDELT describes DOC
2.0 as returning relevant article headlines for matching queries.
[2][3]

What ClearVote could use it for

After extracting a claim, ClearVote could search for:

the main entities

important phrases from the claim

relevant dates

related events

The results could provide additional reporting from multiple outlets.

Cost / limits

GDELT provides its datasets and live APIs publicly. Its documentation
states that the APIs are rate limited to protect the underlying
search infrastructure. There is no normal per-request commercial price
listed in the cited API documentation. High-volume applications should
account for rate limiting and caching. [4]

Advantages

Useful for finding current reporting.

Broad international coverage.

No requirement to build and maintain a news crawler for the MVP.

Good complement to a fact-check API when no direct fact check
exists.

Limitations

Finding many articles does not prove that a claim is true.

Search results can include conflicting or low-quality sources.

Results need source-quality filtering.

API rate limits make aggressive per-page querying unsuitable without
caching.

MVP assessment: Good secondary retrieval source.

2.3 NewsAPI

Use case: Search recent news articles matching a claim or topic.

NewsAPI provides a simple REST API for searching news and retrieving
headlines. Its current Developer plan is free for development/testing,
with 100 requests/day, but it has a 24-hour delay and cannot be used
as a production/staging service under that free plan. Paid plans are
available for production use. [5][6]

Current published pricing

Plan                               Published price Relevant limit

Developer                                      $0 100 requests/day;
development/testing
only; 24-hour article
delay

Business                               $449/month 250,000
requests/month

[5]

Advantages

Very simple REST interface.

Easy Python/FastAPI integration.

Useful for prototyping article retrieval.

Search parameters are convenient for a claim-verification workflow.

Limitations

Free tier is not appropriate for a public production MVP.

Developer plan has a 24-hour delay.

Full article text is not provided by NewsAPI; results include URLs
that can be used to locate the article. [5]

Commercial production cost can become significant.

MVP assessment: Useful for development, but GDELT or another
production-compatible source should be evaluated before launch.

2.4 Google Custom Search JSON API

Use case: Search a controlled set of websites for supporting
sources.

The Custom Search JSON API can return search results in JSON, but Google
currently states that the API is closed to new customers and that
existing customers must transition by January 1, 2027. Existing
customers have 100 free queries/day and additional queries cost $5 per
1,000, subject to the documented limits. [7]

Advantages

Could search a curated set of domains.

JSON responses are easy to process in a backend.

Useful conceptually for source retrieval.

Limitations

Not appropriate for a new ClearVote MVP because new customers
cannot sign up.

Service transition is required for existing users.

Should not be selected as a new dependency.

MVP assessment: Do not build the MVP around this API.

3. AI Models

3.1 Gemini 3.8 Flash

Use case: Claim extraction, evidence synthesis, explanation
generation, and structured output.

Google currently lists Gemini 3.8 Flash as a stable model available
through the Gemini API. It supports a large context window, structured
outputs, function calling, URL context, and Google Search grounding.
[8][9]

Google lists an introductory price of $0.75 per 1 million input
tokens and $3.75 per 1 million output tokens through the end of 2026.
Pricing and limits should be rechecked before production deployment.
[8]

How ClearVote could use it

Gemini can handle the reasoning layer after retrieval:

Political text
      ↓
Extract claim
      ↓
Retrieve fact checks + sources
      ↓
Gemini analyzes the claim against retrieved evidence
      ↓
Structured JSON response
      ↓
ClearVote results page

Example structured response:

{
  "flagged": true,
  "reason": "A relevant fact check disputes part of the claim.",
  "claim": "...",
  "evidence": [
    {
      "source": "...",
      "title": "...",
      "relevance": "..."
    }
  ]
}

Advantages

Strong general language understanding.

Can combine retrieved evidence and explain it.

Supports structured outputs.

Can use URL context and search grounding.

Easy Python integration through Google's SDK.

Limitations

It is a generative model and can still make reasoning or factual
errors.

The model should not be treated as the source of truth.

Cost increases with token usage.

Political content requires careful prompting and evidence
attribution.

Model behavior can change across model versions.

MVP assessment: Strong candidate for the reasoning/explanation
layer, provided that retrieved sources are supplied and displayed.

3.2 DeBERTa-v3

Use case: Lightweight local text classification or
natural-language-inference component.

Microsoft's DeBERTa-v3-base is available through Hugging Face with an
MIT license. The model can be loaded locally with the Transformers
ecosystem. [10]

A particularly relevant model is
MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli, which is based on
DeBERTa-v3 and is trained for natural-language
inference/fact-verification-style tasks. [11]

How ClearVote could use it

Represent verification as an NLI task:

Claim: "X happened."

Evidence: "A report states that X did not happen."

        ↓

NLI model

        ↓

SUPPORTED / REFUTED / NOT ENOUGH INFORMATION

Advantages

Can run locally rather than paying for every inference request.

Good fit for evidence-vs-claim classification.

Integrates with Python and Hugging Face Transformers.

Can later be fine-tuned using ClearVote-specific data.

Limitations

A classifier does not retrieve evidence by itself.

Performance depends heavily on the training/evaluation data.

Political claims can require current information that an older model
does not know.

Local inference introduces CPU/GPU memory and deployment
requirements.

A generic NLI model should not be assumed to be a reliable political
misinformation detector without evaluation on relevant data.

MVP assessment: Good future component; optional for the first
MVP.

3.3 ELECTRA

Use case: Another local transformer baseline for text
classification.

Google's electra-base-discriminator is available through Hugging Face
under the Apache 2.0 license and can be used with Transformers. The
model has a 512-token maximum position length in its published
configuration. [12][13]

Advantages

Open-source model weights.

Can run locally.

Suitable for fine-tuning on classification datasets.

Useful as a baseline for experiments.

Limitations

Not specifically a political fact-checking model.

Requires task-specific fine-tuning for meaningful misinformation
classification.

Does not replace evidence retrieval.

Older/smaller architecture than some newer NLI models.

MVP assessment: Useful research baseline, not necessary for the
first MVP.

4. Datasets

4.1 LIAR

Use case: Political claim classification.

LIAR contains 12,836 manually labeled political statements collected
from PolitiFact. The dataset includes the statement, label, speaker, job
title, state information, party affiliation, speaker history, and
context. [14]

Why it matters to ClearVote

This is one of the most directly relevant datasets because ClearVote's
MVP analyzes political text rather than general news.

Advantages

Political claims.

Relatively small and manageable.

Includes useful metadata.

Good starting benchmark for a classifier.

Limitations

Published in 2017, so it is not representative of current political
language or current events.

Its labels reflect PolitiFact's historical labeling system.

It should be used for experimentation/evaluation rather than treated
as a current source of truth.

Original source material has usage restrictions noted by the dataset
documentation. [14]

MVP assessment: High relevance for baseline experimentation.

4.2 AVeriTeC

Use case: Real-world claim verification with online evidence.

AVeriTeC contains 4,568 real-world claims from 50 fact-checking
organizations. Claims are accompanied by question-answer pairs supported
by evidence available online, textual justifications, and metadata such
as speaker, publisher, date, and location. Labels include Supported,
Refuted, Not Enough Evidence, and Conflicting Evidence/Cherry-picking.
[15]

Why it matters to ClearVote

AVeriTeC closely resembles ClearVote's desired workflow:

claim → search web → retrieve evidence → determine status → explain

Advantages

Real-world claims.

Explicit web evidence.

Includes explanations/justifications.

Includes metadata useful for research.

More aligned with evidence-based verification than a simple
fake/real label.

Limitations

Only 4,568 claims.

Fact-checking evidence can become stale as events change.

Requires careful handling of the dataset license and source
material.

MVP assessment: Very useful for designing and evaluating the
verification pipeline.

4.3 FEVER

Use case: Training/evaluating evidence-based fact verification.

FEVER contains 185,445 claims labeled as Supported, Refuted, or Not
Enough Info. It also provides evidence sentences and Wikipedia URLs for
supported/refuted claims. [16]

Advantages

Large benchmark.

Directly models claim + evidence verification.

Useful for testing an NLI/evidence-ranking pipeline.

Structured JSONL format.

Limitations

Claims were generated by altering sentences from Wikipedia.

It is not specifically political.

Wikipedia evidence differs from the live web/news environment
ClearVote will encounter.

MVP assessment: Good technical benchmark; not sufficient as the
only ClearVote dataset.

4.4 FakeNewsNet

Use case: Research into fake/real news and social context.

FakeNewsNet contains samples associated with PolitiFact and
GossipCop and includes article URLs, titles, and tweet IDs in its
minimal distributed dataset. The full dataset cannot be completely
redistributed because of Twitter privacy policies and publisher
copyright restrictions. [17]

Advantages

Includes political-news data through PolitiFact.

Useful for studying news and social context.

Provides a starting point for fake-news classification research.

Limitations

Dataset collection is older.

Complete raw data is not freely redistributable.

Some collection functionality depends on external social-media
access.

Social-media signals are not required for the ClearVote MVP.

MVP assessment: Useful research dataset, but lower priority than
LIAR and AVeriTeC for the MVP.

5. Comparison

Option         Type           ClearVote use      Cost / access    MVP relevance

Google Fact    API            Existing           API key; quota   High
Check Claim                   fact-check         should be
Search                        retrieval          verified

GDELT DOC 2.0  API            News/source        Public API; rate High
retrieval          limited

NewsAPI        API            News retrieval     Free dev tier;   Medium
paid production
plans

Google Custom  API            Web/source search  Existing         Low
Search JSON                                      customers only;
being
discontinued

Gemini 3.8     AI model/API   Claim extraction + Token-based;     High
Flash                         evidence           current intro
synthesis +        pricing
explanation        published by
Google

DeBERTa-v3 NLI Local model    Evidence/claim     Model is         Medium/High
classification     downloadable;
compute is
required

ELECTRA        Local model    Classification     Model is         Medium
baseline           downloadable;
compute is
required

LIAR           Dataset        Political claim    Research         High
classification     dataset; check
source/license
terms

AVeriTeC       Dataset        Real-world         Research         High
evidence-based     dataset; check
verification       license

FEVER          Dataset        Fact               Public research  Medium/High
verification/NLI   dataset
benchmark

6. Recommended MVP architecture

For the simplest working ClearVote MVP, avoid training a large
misinformation model first.

Recommended pipeline

Browser Extension
       |
       | selected political text
       v
ClearVote Backend (FastAPI)
       |
       +--> Claim extraction
       |       |
       |       v
       |   Gemini Flash
       |
       +--> Google Fact Check Claim Search
       |
       +--> GDELT news/source search
       |
       v
Evidence collection
       |
       v
Gemini reasoning / explanation
       |
       v
Structured result
       |
       +--> Flagged / needs review
       +--> Explanation
       +--> Supporting sources
       +--> Fact-check links
       |
       v
ClearVote Results Page

Why this approach fits the MVP

The MVP's main value is not building a state-of-the-art misinformation
classifier. It is demonstrating the complete user flow:

political text
      ↓
claim extraction
      ↓
evidence retrieval
      ↓
analysis
      ↓
warning
      ↓
Learn More
      ↓
sources + explanation

This also makes the system easier to explain to users because ClearVote
can show why something was flagged and where the evidence came from.

7. Suggested implementation order

Phase 1 --- Basic prototype

Use:

Browser extension

FastAPI backend

Gemini Flash

Google Fact Check Claim Search API

GDELT

PostgreSQL/SQLite for basic caching

Do not train a custom model yet.

Phase 2 --- Improve verification

Add:

AVeriTeC evaluation

LIAR evaluation

DeBERTa-v3 NLI

Better source ranking

Claim/evidence caching

Evaluation metrics such as precision, recall, and false-positive
rate

Phase 3 --- Production hardening

Add:

Rate limiting

API-key protection

Source-quality rules

Monitoring

More robust privacy controls

Model/version pinning

Human review workflow for ambiguous cases

8. Important design decision: "flagged" should not mean "false"

For the MVP, ClearVote should avoid presenting an AI-generated
classification as an unquestionable political truth.

A better result format is:

Potentially misleading --- review the evidence

Then show:

Claim detected

Why it was flagged

Relevant fact checks

Supporting or conflicting sources

Publication dates

Original source links

If the available evidence is insufficient, the result should say:

Not enough evidence found

rather than forcing a true/false result.

This is particularly important because political claims can depend on
dates, definitions, context, and newly available information.

9. Final recommendations

Recommended for the first MVP

1. Google Fact Check Claim Search API
Use as the first lookup because it directly provides existing fact-check
results.

2. GDELT DOC 2.0
Use as the secondary source-retrieval layer for recent reporting and
cross-source context.

3. Gemini Flash
Use for claim extraction, evidence synthesis, and generating the
user-facing explanation. The model should reason over retrieved evidence
rather than independently acting as the source of truth.

4. AVeriTeC + LIAR
Use for evaluation and experimentation. AVeriTeC is especially useful
for testing evidence-based verification; LIAR is especially relevant to
political claims.

5. DeBERTa-v3 NLI
Keep as the next-stage classifier/evidence-comparison component rather
than making it mandatory for the first demo.

Not recommended as a core MVP dependency

Google Custom Search JSON API --- not available to new customers and
scheduled for transition/discontinuation.

Training a custom misinformation model immediately --- unnecessary
complexity before the end-to-end workflow is working.

Relying on a single AI model's "true/false" output --- insufficient
evidence architecture for a political verification product.

References

Google Fact Check Tools API:
https://developers.google.com/fact-check/tools/api

GDELT Project --- Data, APIs and documentation:
https://gdeltproject.org/data.html

GDELT DOC 2.0 API:
https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/

GDELT API rate limiting:
https://blog.gdeltproject.org/ukraine-api-rate-limiting-web-ngrams-3-0/

NewsAPI pricing: https://newsapi.org/pricing

NewsAPI terms/developer-plan restrictions: https://newsapi.org/terms

Google Custom Search JSON API:
https://developers.google.com/custom-search/v1/overview

Gemini 3.8 Flash: https://ai.google.dev/gemini-api/docs/latest-model

Gemini Google Search grounding:
https://ai.google.dev/gemini-api/docs/google-search

Microsoft DeBERTa-v3-base:
https://huggingface.co/microsoft/deberta-v3-base

DeBERTa-v3-base-mnli-fever-anli:
https://huggingface.co/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli

Google ELECTRA:
https://huggingface.co/google/electra-base-discriminator

ELECTRA model configuration:
https://huggingface.co/google/electra-base-discriminator/blob/main/config.json

LIAR dataset: https://github.com/tfs4/liar_dataset

AVeriTeC dataset: https://fever.ai/dataset/averitec.html

FEVER dataset: https://fever.ai/dataset/fever.html

FakeNewsNet: https://github.com/KaiDMML/FakeNewsNet

# Misinformation detection and fact-checking research

Research date: 26 September 2026. Prepared for [ClearVote issue #1](https://github.com/OratorMurambiwa/ClearVote/issues/1).

## 1. Executive recommendation

ClearVote should begin as an evidence-finding assistant for text-based political claims. Identify the specific claim, find a relevant published fact check, verify that it addresses the same claim and context, and present its attributed assessment with a link and date. When the evidence is missing or the match is uncertain, say so. Do not substitute a model's confidence, a publisher's reputation, or an AI-authorship score for factual verification.

This is a proposed product direction, not a tested implementation. It follows the repository's [MVP](../docs/mvp.md), which prioritizes text, short notifications, explanations, and sources. Image, video, and deepfake detection belong in later phases. The broader [product flow](../docs/product-flow.md) describes those capabilities, but they are not MVP requirements.

The strongest initial candidates are Google's Fact Check claim search for discovery, editorial fact-checking organizations as evidence sources, and the claim-detection and matching patterns demonstrated by Full Fact and ClaimBuster. Factiverse offers a commercial alternative worth comparing if access and budget permit. Media tools should remain separate from text-veracity decisions.

## 2. Scope and research method

This is a structured desk review of primary sources: official product documentation, editorial methodologies, a standards explainer, and original research papers. It covers 13 named tools, platforms, or standards, plus evidence on verification methods and evaluation. Sources are linked beside findings and collected at the end. Product pages describe advertised capabilities; they do not establish independent accuracy. Older research is dated and used to explain demonstrated failure modes, not to rank current products.

No paid accounts were opened, APIs benchmarked, browser extensions installed, or detector models run. Prices, quotas, permissions, retention policies, language coverage, and live availability must be checked before integration. ClaimBuster's main application page did not load during this review; its role is supported by its university's research descriptions, not a successful service test.

The repository does not specify a target election jurisdiction or language. English is a reasonable proposed first pilot language, subject to team agreement. Detailed API procurement, model selection, and dataset implementation remain with the teammates assigned those tasks in [team roles](../docs/team-roles.md).

## 3. Separate the questions being answered

| Question | Relevant approach | What its result can establish | What its result does not establish |
| --- | --- | --- | --- |
| Is this a checkable factual statement? | Claim detection and prioritization | Identifies statements that can potentially be checked against evidence and prioritized for review. | That it is false or harmful. |
| Has this claim already been investigated? | Claim matching | Finds potentially relevant previous investigations; a verified match can support reuse of their findings within the same context. | That a similar-looking claim has identical meaning. |
| Does reliable evidence support it? | Evidence retrieval and verification | Supports an assessment that the claim is supported, contradicted, or unresolved by the available evidence. | Certainty beyond the evidence’s scope and date. |
| Does this publisher follow credible practices? | Source assessment | Provides evidence of how the publisher meets defined editorial and transparency criteria, helping users assess its reliability. | Truth or falsity of every individual statement. |
| Was this media generated or manipulated? | Forensic detection and watermark detection | Provides signals of possible generation or manipulation; a validated watermark can indicate use of a participating generation system. | Whether its accompanying factual claim is true. |
| What is known about this file’s history? | Signed provenance | Can authenticate signed records about the file’s origin and editing history and check whether the content matches those records. | That the depicted event happened as described. |

For this report, misinformation means false or misleading information; calling something deliberate disinformation additionally requires evidence about intent. ClearVote should assess the content without guessing the author's motives. Opinion, satire, predictions, and factual assertions need different treatment. A real photograph can carry a false caption; an AI-generated illustration can accompany an accurate article. These distinctions should determine both the system design and the wording users see.

## 4. Tools and platforms compared

The limitations and ClearVote-fit columns are this report's assessment unless explicitly attributed to a source.

| Tool or platform | Documented capability and strength | Important limitation | Recommended ClearVote role |
| --- | --- | --- | --- |
| Google Fact Check Explorer / Fact Check Tools API | Searches published fact-checked claims; structured records support attribution and review links. [S1], [S2] | Retrieval is not a new investigation; coverage and semantic equivalence must be checked. | First candidate for an MVP discovery source. |
| Full Fact AI | Detects claims, monitors sources, and matches recurring claims to tracked material; includes a review queue. [S4] | Professional workflow; product documentation does not prove suitability, access, or accuracy for ClearVote. | Adopt its detection → matching → review pattern; investigate service access separately. |
| ClaimBuster | University research system emphasizing detection of claims worth checking and matching to prior fact checks. [S5] | A check-worthiness score is not a truth score; current application access unverified. | Reference for prioritizing statements, not a confirmed production dependency. |
| Factiverse | API documentation exposes claim detection, claim search, stance detection, and fact-checking functions. [S6] | Access requires vendor coordination; retrieved agreement can still be based on weak evidence. | Optional commercial comparison against the simpler retrieval baseline. |
| PolitiFact | Publishes political claim investigations with an explicit rating methodology and editorial review. [S7] | Ratings are contextual, time-dependent editorial judgments; coverage is selective. | Attributed evidence source, especially for relevant US political claims. |
| FactCheck.org | Describes research using original records and data, editing, and correction procedures. [S8] | Its editorial coverage cannot encompass all claims or jurisdictions. | Evidence source and model for traceable explanations. |
| Africa Check | Documents precise claim identification, data checking, expert consultation, peer review, and corrections. [S9] | Local relevance still depends on country, language, subject, and available records. | Broaden source selection where its coverage matches the pilot. |
| NewsGuard | Browser extension displays journalist-produced website ratings with detailed explanations. [S10], [S11] | Publisher-level assessment is not claim verification; commercial licensing is separate. | Learn from the compact indicator and explanation design; keep source context distinct. |
| Community Notes | Uses contributor ratings, including agreement across differing rating histories, to identify helpful notes. [S12] | Helpful consensus is not proof; a suitable note may not exist when needed. | Learn from evidence-linked context and correction mechanisms; defer a crowd system. |
| InVID–WeVerify–vera.ai verification plugin | Browser toolkit for reverse image search, keyframes, metadata, and forensic investigation. [S13] | Requires interpretation; external services and platform changes affect usability. | Later media-investigation aid; useful browser UX reference. |
| Reality Defender RealAPI | Advertises image, audio, and video manipulation detection with structured results. [S14] | Vendor scores need independent validation on ClearVote's media; supported modalities depend on plan. | Future candidate for a controlled media pilot. |
| Google SynthID / C2PA Content Credentials | SynthID detects embedded watermarks; C2PA provides signed provenance. These are separate technologies. [S15], [S16] | Neither establishes claim truth; missing signals do not establish human origin or fakery. | Future, separately labeled media context. |

### 4.1 Practical details for text fact-checking

Google's search endpoint accepts a text query and supports language, publisher, age, and pagination filters. Its language filter does not consider region, and its age filter uses the newer of claim date and review date. ClearVote would therefore need its own jurisdiction and temporal checks. A search hit is only a candidate match. [S1]

The returned claim and review records include fields for claim text, claimant, dates, publisher, review URL, language, and textual rating. Preserve the original rating and attribution instead of silently converting every publisher's scale to one number. Empty results mean no matching record was returned, not that the statement is correct. [S2]

An important maintenance distinction: Google has phased out Claim Review presentation in Search, while its documentation says Fact Check Explorer continues to support the markup. Do not mistake removal of a Search feature for removal of the separate claim-search capability; also do not promise Search rich results as a ClearVote feature. [S3]

Full Fact's current product page also advertises AI-generated assessments and harm analysis. Those features should not be copied merely because they are available: its tracked-claim matching and explicit human review are the narrower patterns suited to ClearVote's first version. The team should establish its own evidence requirements before considering automatic judgments. [S4]

Editorial outlets offer methodologies and citable investigations, not an automatically unrestricted content feed. Prefer source links and appropriately permitted excerpts; confirm reuse arrangements before building a copied corpus. NewsGuard's commercial data is a separate procurement question. Its FAQ says the extension sends visited domains to its servers, illustrating that even a small browser indicator has data-handling implications. [S11]

### 4.2 What the comparison does not establish

This review does not show that any vendor is the most accurate or cheapest. Features, independent evidence, operational suitability, and cost are different criteria. No API keys or authenticated responses were tested. InVID's current repository is MIT-licensed, but that does not automatically grant access to every service used by the extension. [S13] Reality Defender's published free offering covers image and audio scans, while video appears in paid plans; recheck the current offering before a trial. [S14]

## 5. Verification approaches and tradeoffs

The automated fact-checking literature separates claim detection, evidence retrieval, and verification with justification. This modular view is more useful for ClearVote than a single article-level “fake news” score, because each stage can fail differently and can be evaluated separately. [S17]

| Approach | How it works | Strength | Failure mode and proposed response |
| --- | --- | --- | --- |
| Rules or supervised claim classification | Identify statements likely to contain checkable facts. | Can reduce unnecessary analysis. | Missed implied claims, sarcasm, or unfamiliar phrasing; retain surrounding context and allow user-selected text. |
| Keyword and semantic claim matching | Retrieve prior investigations using words and meaning. | Reuses researched evidence for recurring claims. | Similar topics with different dates, quantities, entities, or negation; add explicit equivalence checks. |
| Retrieval plus evidence-conditioned assessment | Find documents, then judge their relationship to the claim. | Can address claims absent from a fact-check index. | Bad retrieval, stale evidence, or unsupported synthesis; require cited passages and abstain when insufficient. |
| Structured records / knowledge queries | Compare a claim with a relevant table or official record. | Useful for clearly defined counts and historical events. | Mismatched definitions, periods, units, and revisions; retain exact metadata and calculations. |
| Publisher credibility signals | Provide context about editorial practices. | Helps users evaluate sources. | Reputation substituted for evidence; never use it alone as a verdict. |
| Human editorial or community review | People inspect evidence and reasoning. | Can resolve ambiguity and local context. | Capacity, disagreement, delay, and inconsistent judgments; record decisions and corrections. |

### 5.1 Claim matching should precede novel verification

Proposed sequence: extract one claim, search existing fact checks, retrieve several candidates, and compare their meaning. Preserve who, what, where, when, quantities, and qualifiers. Semantic similarity should propose candidates; it should not transfer a rating automatically.

For example, a fact check about “all ballots in Region A in 2022” does not resolve “some ballots in Region B in 2026.” A quotation of a false claim inside a debunking article should not cause the article to be flagged as endorsing it. These are illustrative tests, not assertions about actual elections.

Begin with attributed matches and short template-based explanations. This reduces the amount of generated material that must be checked, although matching still needs evaluation. A more ambitious evidence-search fallback can be prototyped separately once the baseline's errors are understood.

### 5.2 Evidence retrieval is a central bottleneck

Research on complex claim verification identifies unrealistic evaluation assumptions, including access to human-curated evidence or material published after the claim. ClearVote should test with evidence genuinely available at the relevant time. Later evidence may be useful for a retrospective update, but must be labeled as such. [S18]

Proposed evidence policy: choose sources appropriate to the claim; inspect their underlying records; record dates and jurisdiction; seek independent corroboration for contested assertions; and distinguish several independent sources from several articles repeating one source. An official statement is evidence that an institution said something, not automatic proof of all assertions within it.

An LLM can help split claims, suggest queries, and summarize retrieved passages. It should not invent citations or rely on its internal recollection as the final authority. Retrieve and store source URLs separately, verify that cited passages actually support the explanation, and return an unresolved result when evidence conflicts or cannot be obtained. Agreement among multiple model outputs is not independent corroboration.

### 5.3 Classification benchmarks are useful but limited

FEVER provides supported, refuted, and insufficient-evidence examples based on Wikipedia-derived claims. It is useful for studying evidence-based inference, but its construction differs from live political content. [S19] AVeriTeC's shared task evaluates real-world claim verdicts together with evidence quality; this is a better evaluation principle for ClearVote than verdict accuracy alone. Its 2024 results are historical benchmark results, not predictions of current ClearVote performance. [S20]

A classifier trained on article style or dataset labels may learn shortcuts that do not establish truth. Treat such a model as a candidate filter until its behavior has been tested on independently labeled, current examples from the intended audience. Dataset and model selection should be coordinated with the AI/ML teammate.

## 6. Deepfakes and AI-generated content: future scope

### 6.1 Detection, watermarking, and provenance are complementary

Content-based detectors inspect statistical or learned signals in images, voices, and video. Watermark detectors look for a signal embedded by a participating generator. Provenance systems inspect recorded creation and editing history. NIST reviews these as distinct transparency approaches rather than a single universal solution. [S21]

SynthID is useful when its watermark is present and detectable. It does not provide a universal test for outputs of every generator. [S15] C2PA's explainer explicitly separates provenance from factual truth. A valid credential can help establish recorded history and integrity, but cannot decide whether a caption or political interpretation is accurate. [S16]

Proposed UI: show separate findings such as “watermark detected,” “credential validated,” “possible manipulation,” or “no provenance information found.” Do not translate a missing watermark or credential into a “real” or “fake” verdict. Verification of media history should remain independent of verification of the claims made about it.

### 6.2 Real-world robustness must be tested

Deepfake-Eval-2024 studies media circulated online and reports substantially weaker performance for evaluated open-source detectors than on older benchmarks. This supports testing on realistic content, not a blanket conclusion that all open models are inferior. [S22] A later baseline study reports substantial improvement from better tuning on the same benchmark, illustrating how model setup and evaluation choices affect comparisons. Both sources are research reports, not a ClearVote trial. [S23]

Any future pilot should include unseen generators, compressed and cropped media, screen recordings, short clips, language variation, and genuine media processed by ordinary editing tools. Record performance separately for image, audio, and video. A single overall accuracy number can hide unacceptable errors in one category.

Start future media work with context investigation: find earlier appearances, inspect keyframes and metadata, and compare the original caption or source. The InVID toolkit supports this workflow. [S13] Add automated detection only as an additional signal, with uncertain cases left unresolved.

### 6.3 AI-text detectors should not drive MVP warnings

RAID evaluated text detectors across different generators, domains, decoding settings, and attacks, finding robustness problems. Its findings apply to the evaluated systems and conditions, not every future product. [S24] Liang and colleagues demonstrated false positives affecting non-native English writing in their 2023 evaluation; use this as a reason to test fairness, not as a current error-rate estimate. [S25]

More fundamentally, authorship and truth are different targets. Even a perfectly accurate AI-authorship detector would not resolve whether a statement is supported by evidence. ClearVote should exclude AI-text scores from its MVP misinformation verdicts.

## 7. Proposed ClearVote MVP design

These are recommendations for team review, not changes to the existing project requirements.

1. **Capture a bounded text passage and its context.** Preserve the original wording and page reference. A user-selected passage is a useful first prototype; automatic scanning can follow within the agreed browsing scope.
2. **Identify individual factual claims.** Separate quotations, opinions, satire, and predictions. Return “no checkable claim identified” where appropriate.
3. **Retrieve existing fact checks.** Use a replaceable provider adapter so the project is not tied to one source. Check language, jurisdiction, date, and source coverage.
4. **Validate the match.** Compare entities, numbers, qualifiers, negation, and time. If uncertain, show only a related resource or abstain.
5. **Return an attributed result.** Include the exact assessed claim, original publisher rating, explanation, review URL, relevant dates, and limitations.
6. **Show a short notification and a Learn More page.** Display the evidence and why it applies. Provide a correction/report-problem route and avoid repeating the same warning unnecessarily.

### Suggested result states

| State | Meaning and presentation |
| --- | --- |
| Matched fact check | Show the publisher's assessment, attribution, and date after equivalence checks. |
| Related fact check | Context is relevant, but it does not settle this exact claim; do not transfer its verdict. |
| Insufficient evidence | The available material does not support a defensible assessment. |
| Conflicting evidence | Relevant sources disagree; describe the disagreement without forcing a binary judgment. |
| No checkable claim | The passage was not identified as a factual assertion suitable for this process. |
| Check unavailable | A service or retrieval failed; distinguish failure from an evidence search returning no answer. |

Store the original text, normalized claim, assessed scope/date, result status, evidence links and passages, publisher, original rating, retrieval time, and pipeline version. This is a proposed information contract, not a finalized API schema. Keep source assessments and any future media indicators in separate fields.

Avoid an unexplained “87% true” indicator. Similarity scores and model confidence are not calibrated probabilities of factual correctness. A useful explanation answers: what was assessed, who investigated it, what evidence was used, when it applies, and what remains uncertain.

## 8. Important limitations and safeguards

| Risk | Proposed response |
| --- | --- |
| Missing fact checks and breaking news | Abstain clearly; prioritize coverage measurement instead of pretending all claims can be resolved. |
| Temporal or geographic mismatch | Keep dates and jurisdiction; recheck changing claims and invalidate stale cached results. |
| Source or language imbalance | Publish supported scope; examine errors by topic, jurisdiction, language, and source coverage. |
| Unsupported generated explanations | Restrict explanations to retrieved evidence; review citation relevance, not just URL existence. |
| Quoted misinformation mistaken for endorsement | Preserve surrounding text and distinguish the speaker's claim from the article's position. |
| Multiple dependent sources mistaken for consensus | Trace original evidence and group duplicate reporting. |
| Browser data exposure | Send only the necessary passage; exclude private fields and sensitive pages by design; define retention before a pilot. |
| Hostile page text influencing analysis | Treat page content as data, not instructions; restrict any model-driven actions and validate outputs. |
| Users interpreting silence as verification | Explain that no warning does not mean a page was checked or found accurate. |
| Incorrect published assessment | Keep source versions, provide corrections, and ensure corrected results replace cached ones. |

The silence problem has empirical support: Pennycook and colleagues found an “implied truth” effect when warnings appeared on only some false headlines. That study does not establish the size of the effect in ClearVote, but supports testing whether users understand unchecked content. [S26] Privacy and security items above are proposed design requirements; they do not claim a completed legal or security review.

## 9. Evaluation plan before choosing a production approach

This plan is proposed work, not reported test results. First choose the pilot jurisdiction, language, and supported page types. Then assemble a small human-reviewed development set and a separate held-out evaluation set. A practical starting point is 100–200 examples for an exploratory pilot; this is not sufficient to certify broad reliability or subgroup fairness.

Include supported and refuted claims, misleading context, unresolvable claims, opinion/satire, quotations in debunks, changed dates/numbers, paraphrases, and unrelated search hits. Have two reviewers label independently, record supporting evidence and its date, and adjudicate disagreements. Keep near-duplicate claims in the same split and avoid using the answer article as undisclosed input to a novel-verification test.

Compare: (A) keyword retrieval of existing checks; (B) semantic retrieval plus equivalence checks; and, if accessible, (C) a commercial or retrieval-plus-model pipeline. Evaluate every system on the same examples. Keep a record of versions, configuration, and abstentions.

| Measure | Why it matters |
| --- | --- |
| Claim extraction errors | Shows missed assertions and false detections of opinion or quotation. |
| Correct-match precision and recall | Separates wrongly transferred fact checks from missed relevant checks. |
| Evidence relevance and explanation support | Tests whether the result is justified, not merely plausible. |
| Warning precision and false-warning rate | Measures erroneous warnings and the burden on correctly stated content. |
| Coverage and abstention rate | Prevents a system that answers almost nothing from appearing successful. |
| Verdict performance by category | Exposes failures hidden by overall accuracy; include an explicit unresolved category. |
| Latency and cost per check | Tests whether the workflow fits browsing; measure median and slower-tail response times. |
| User understanding | Ask users whether no warning means verified, and whether they can locate the evidence. |

Warning precision means the fraction of warnings that are justified; false-warning rate means the fraction of non-warning-worthy cases incorrectly flagged. Report counts and uncertainty, not just percentages. Choose release thresholds before examining held-out results. If reliable matching cannot be demonstrated, narrow the pilot or show evidence links without an automatic warning.

## 10. Priorities and team handoff

| Priority | Recommendation | Follow-up |
| --- | --- | --- |
| MVP | Existing fact-check retrieval, equivalence checks, clear attribution, unresolved states | Henry and backend teammates define result needs with frontend and AI/ML owners. |
| MVP | Evidence-first explanations and correction handling | Agree on wording and required metadata; test user comprehension. |
| MVP | Small, realistic evaluation and coverage statement | Coordinate annotations and model assessment with Tatenda. |
| Next | Evidence retrieval for previously unchecked claims | Compare with the baseline after access, cost, and accuracy checks. |
| Later | Context-based media investigation, provenance, and detector trials | Keep media findings separate from claim truth and validate each modality. |
| Defer | Universal truth scores, AI-text-based misinformation warnings, a new crowd-review platform | These add uncertainty or operational scope without proving MVP value. |

Open decisions: pilot jurisdiction/language; first supported websites; acceptable false-warning rate; who reviews disputed results; API access and budget; source reuse permissions; data retention; and whether novel claims should be handled at all in the first release. Vensen and Orator can use these findings to inform API/dataset research; Tatenda can use the failure cases and evaluation criteria when selecting a model.

## Sources

All sources below were consulted on 26 September 2026. Product documentation supports descriptions of features, not independently measured accuracy. Numbered links in the report resolve to these primary sources.

- **S1.** [Google: claims.search API reference][S1] — search controls and age/language semantics.
- **S2.** [Google: Claim and ClaimReview resource][S2] — returned fields and attribution.
- **S3.** [Google: Fact check structured data][S3] — Search versus Explorer support distinction.
- **S4.** [Full Fact AI: Product][S4] — detection, tracked claims, analysis, and review queue.
- **S5.** [University of Texas at Arlington: ClaimBuster research (2017)][S5] — historical project description; current lab [project listing](https://idir.uta.edu/projects/) also identifies its claim-spotting role.
- **S6.** [Factiverse: API documentation][S6] — available operations and access instructions.
- **S7.** [PolitiFact: Methodology][S7] — contextual ratings and editorial process.
- **S8.** [FactCheck.org: Our Process][S8] — research, editing, and corrections.
- **S9.** [Africa Check: How we fact-check][S9] — evidence and review workflow.
- **S10.** [NewsGuard: Rating process and criteria][S10] — website-level ratings.
- **S11.** [NewsGuard: FAQ][S11] — licensing and extension data flow.
- **S12.** [Community Notes: Diversity of perspectives][S12] — basis of cross-perspective agreement.
- **S13.** [AFP Medialab: Current verification-plugin repository][S13] — features, MIT license, and service configuration.
- **S14.** [Reality Defender: RealAPI][S14] — advertised modalities, output, and plan distinctions.
- **S15.** [Google DeepMind: SynthID][S15] — watermark-based identification.
- **S16.** [C2PA: Version 2.2 explainer][S16] — provenance and its limits; cited as a conceptual reference, not a claim that 2.2 is the latest specification.
- **S17.** [Guo et al. (2022): A Survey on Automated Fact-Checking][S17] — stages and research framework.
- **S18.** [Complex Claim Verification with Evidence Retrieved in the Wild (2024)][S18] — evidence and timing limitations.
- **S19.** [Thorne et al. (2018): FEVER][S19] — evidence-based verification dataset.
- **S20.** [Schlichtkrull et al. (2024): AVeriTeC shared task][S20] — joint evaluation of evidence and verdicts.
- **S21.** [NIST AI 100-4 (2024): Reducing Risks Posed by Synthetic Content][S21] — overview of transparency approaches.
- **S22.** [Chandra et al. (2025, revised 2026): Deepfake-Eval-2024][S22] — in-the-wild benchmark; arXiv research report.
- **S23.** [Castaneda et al. (2025): Revisiting Simple Baselines for In-The-Wild Deepfake Detection][S23] — tuning-sensitive benchmark comparisons; arXiv research report.
- **S24.** [Dugan et al. (2024): RAID][S24] — robustness evaluation of text detectors.
- **S25.** [Liang et al. (2023): GPT detectors are biased against non-native English writers][S25] — evaluated fairness failure; arXiv page links the published Patterns article.
- **S26.** [Pennycook et al. (2020): The Implied Truth Effect][S26] — experimental evidence on warning-label interpretation.

[S1]: https://developers.google.com/fact-check/tools/api/reference/rest/v1alpha1/claims/search
[S2]: https://developers.google.com/fact-check/tools/api/reference/rest/v1alpha1/claims
[S3]: https://developers.google.com/search/docs/appearance/structured-data/factcheck
[S4]: https://fullfact.ai/product/
[S5]: https://www.uta.edu/news/news-releases/2017/08/24/claimbuster-nsf
[S6]: https://api.factiverse.ai/v1/redoc
[S7]: https://politifact.com/article/2018/feb/12/principles-truth-o-meter-politifacts-methodology-i/
[S8]: https://www.factcheck.org/our-process/
[S9]: https://www.africacheck.org/how-we-fact-check
[S10]: https://www.newsguardtech.com/ratings/rating-process-criteria/
[S11]: https://www.newsguardtech.com/newsguard-faq/
[S12]: https://communitynotes.x.com/guide/en/contributing/diversity-of-perspectives
[S13]: https://github.com/AFP-Medialab/verification-plugin
[S14]: https://www.realitydefender.com/product/realapi
[S15]: https://deepmind.google/models/synthid/
[S16]: https://spec.c2pa.org/specifications/specifications/2.2/explainer/Explainer.html
[S17]: https://aclanthology.org/2022.tacl-1.11/
[S18]: https://aclanthology.org/2024.naacl-long.196/
[S19]: https://aclanthology.org/N18-1074/
[S20]: https://aclanthology.org/2024.fever-1.1/
[S21]: https://www.nist.gov/publications/reducing-risks-posed-synthetic-content-overview-technical-approaches-digital-content
[S22]: https://arxiv.org/abs/2503.02857
[S23]: https://arxiv.org/abs/2509.04150
[S24]: https://aclanthology.org/2024.acl-long.674/
[S25]: https://arxiv.org/abs/2304.02819
[S26]: https://pubsonline.informs.org/doi/abs/10.1287/mnsc.2019.3478

# ClearVote Tools Research

## 1. Political Content Detection

### BART-large-MNLI
[BART-large-MNLI](https://huggingface.co/facebook/bart-large-mnli) 
**Cost:** Free locally  
zero-shot classifier that can classify page text into categories without task-specific training.

### DeBERTa-v3-base-zeroshot-v2.0
[DeBERTa Zero-Shot](https://huggingface.co/MoritzLaurer/deberta-v3-base-zeroshot-v2.0)  
**Cost:** Free locally  
Another zero-shot classifier 

### nli-deberta-v3-base
[NLI DeBERTa v3](https://huggingface.co/cross-encoder/nli-deberta-v3-base)  
**Cost:** Free locally  
Natural-language-inference model that can also support zero-shot classification.

---

## 2. Finding Check-Worthy Claims

### spaCy + Rules
[spaCy](https://spacy.io/)  
**Cost:** Free  
Split page text into sentences and prioritize sentences containing names, dates, locations, money, percentages, and other factual information.

### BERT ClaimBuster
[BERT ClaimBuster model](https://huggingface.co/Nithiwat/bert-base_claimbuster)  
**Cost:** Free locally  
BERT model fine-tuned on ClaimBuster data to detect whether a statement is worth fact-checking.

### mDeBERTa ClaimBuster
[mDeBERTa ClaimBuster model](https://huggingface.co/Nithiwat/mdeberta-v3-base_claimbuster)  
**Cost:** Free locally  
DeBERTa-based model trained for claim detection and check-worthiness classification.

---

## 3. Existing Fact Checks

### Google Fact Check Tools API
[Google Fact Check Tools API](https://developers.google.com/fact-check/tools/api)  
**Cost:** API key required; 
Searches Google's collection of existing fact-checks and can return the publisher, rating, review URL, and date.

### ClaimBuster API
[ClaimBuster project](https://idir.uta.edu/projects/)  
**Cost:** Public pricing not clearly listed  
Research system with tools for claim spotting, claim matching, search-based checking, and knowledge-base checking.

### Factiverse
[Factiverse](https://www.factiverse.ai/)  
**Cost:** Free/trial options may be available; paid API plans available  
Commercial fact-checking platform that identifies claims, retrieves sources, and performs automated verification.

---

## 4. Finding Current Evidence

### Tavily
[Tavily pricing](https://www.tavily.com/pricing)  
**Cost:** 1,000 free credits/month; paid usage after the free tier  
AI-focused search API for retrieving recent web sources and evidence.

### Brave Search API
[Brave Search API](https://brave.com/search/api/)  
**Cost:** Paid per request, with monthly free credit available  
Provides live web, news, image, and other search results.

### Exa Search
[Exa pricing](https://exa.ai/pricing)  
**Cost:** Free credits available; paid usage after the free allowance  
Search API designed for AI applications that can return search results and webpage text.

---

## 5. Matching Claims to Search Results

### all-MiniLM-L6-v2
[MiniLM model](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)  
**Cost:** Free locally  
Creates sentence embeddings so ClearVote can find fact-checks or articles that mean the same thing even when wording differs.

### E5-small-v2
[E5-small-v2](https://huggingface.co/intfloat/e5-small-v2)  
**Cost:** Free locally  
Small embedding model designed for semantic retrieval and similarity search.

### BGE-small-en-v1.5
[BGE-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)  
**Cost:** Free locally  
Lightweight embedding model suitable for matching claims to relevant evidence.

---

## 6. Evidence Verification

### DeBERTa-v3-base-MNLI-FEVER-ANLI
[DeBERTa FEVER model](https://huggingface.co/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli)  
**Cost:** Free locally  
Trained on FEVER and NLI datasets and can classify evidence as supporting, contradicting, or neutral toward a claim.

### nli-deberta-v3-base
[NLI DeBERTa v3](https://huggingface.co/cross-encoder/nli-deberta-v3-base)  
**Cost:** Free locally  
Compares two statements and returns `contradiction`, `entailment`, or `neutral`.

### RoBERTa-large-MNLI
[RoBERTa-large-MNLI](https://huggingface.co/FacebookAI/roberta-large-mnli)  
**Cost:** Free locally  
Another NLI model that can compare retrieved evidence against a claim.

---

## 7. Optional LLM Approach

An LLM could assist with **claim extraction** 

| Model | Cost | Possible Use |
|---|---:|---|
| GPT-4.1 mini | Usage-based | Claim extraction and explanation generation |
| Gemini 2.5 Flash | Free tier + paid usage | Claim extraction, structured output, explanations |
| Claude Haiku | Usage-based | Fast claim analysis and explanation generation |

**Why use an LLM:** Less custom model development and easier structured explanations.

**Why not rely on one:** LLMs can hallucinate, so they should not decide whether a political claim is true without retrieved evidence.

---

## 8. Useful Datasets

### ClaimBuster
[ClaimBuster Dataset](https://zenodo.org/records/3836810)  
Best for training or testing whether a sentence contains a factual claim worth checking.

### FEVER
[FEVER Dataset](https://fever.ai/dataset/fever.html)  
Best for testing whether retrieved evidence supports, refutes, or does not provide enough information for a claim.

### AVeriTeC
[AVeriTeC Dataset](https://fever.ai/dataset/averitec.html)  
Useful for evaluating real-world claim verification using web evidence.

### MultiFC
[MultiFC Paper](https://aclanthology.org/D19-1475/)  
Contains real-world claims collected from multiple fact-checking websites 

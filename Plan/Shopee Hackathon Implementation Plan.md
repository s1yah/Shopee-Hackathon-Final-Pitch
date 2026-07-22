# Shopee Hackathon Matcher Implementation Plan

This plan details the technical approach to implementing the concept defined in `Final Hackathon Pitch Concept.txt`, split into the two core pipelines: **The Live Matcher** and **The Maintenance Harness & Rule Scorecard**.

## User Review Required

> [!IMPORTANT]
> Please review the proposed technology stack and architecture below. Once approved, I will begin scaffolding the project, creating the necessary modules for Pipeline A (fast inference and cascading logic) and Pipeline B (the evaluation harness).

## Open Questions

1. **Vision-LLM Provider:** Do you have a preference for the Vision-LLM provider for Stage 7? (e.g., Google Gemini Pro Vision, OpenAI GPT-4o, or an open-source alternative?)
2. **Performance Constraints:** Are there strict latency requirements for the overall pipeline? The CPU/Fuzzy stages are very fast, but Vision and LLM calls can take 1-3 seconds.
3. **Data Availability:** Do we have access to a sample dataset of shop names and logos to build the "20-Pair Evaluation Dataset" for Pipeline B?

---

## Proposed Changes and Architecture

### Technology Stack

*   **Language:** Python (Ideal for combining text processing, ML models, and API integration).
*   **Web Framework:** **FastAPI** (For exposing Pipeline A as a high-performance, asynchronous REST API).
*   **Text Matching:** Basic regex for Stage 1-3. `TheFuzz` (formerly `fuzzywuzzy`) for Stage 4 fuzzy distance scoring.
*   **Visual Pre-filter (CLIP):** `transformers` and `torch` (HuggingFace) to run a lightweight, local CLIP model (e.g., `openai/clip-vit-base-patch32`) for fast logo comparison.
*   **Rule Database:** A simple SQLite or PostgreSQL database (or an in-memory solution like Redis for the hackathon) to store the active/archived rules for Stage 6.
*   **LLM Integration:** `langchain` or native SDKs to interact with the chosen Vision-LLM.
*   **Dashboard (Pipeline B):** **Streamlit** (To quickly build the Rule Scorecard Evaluation Loop and Human-in-the-Loop approval interface).

### Project Structure Overview

I propose structuring the repository as follows:

```text
/shopee-matcher
├── api/                   # FastAPI application (Pipeline A entry point)
├── core/                  # Shared domain logic
│   ├── models/            # Pydantic data models
│   ├── rules/             # Rule retrieval logic (Stage 6)
│   └── database.py        # Rule Bank DB connection
├── pipeline_a/            # The Live Matcher Modules
│   ├── stages/
│   │   ├── s1_preprocess.py     # Regex/Direct Match
│   │   ├── s2_initials.py       # Acronym Guard
│   │   ├── s3_whitespace.py     # Cleaning
│   │   ├── s4_fuzzy.py          # Fuzzy Distance
│   │   ├── s5_clip.py           # Visual Pre-filter
│   │   └── s7_vision_llm.py     # Final LLM Judgment
│   └── matcher.py         # Orchestrates the stages in a cascading DAG
├── pipeline_b/            # Maintenance Harness
│   ├── evaluator.py       # Runs the dataset against rules (On vs Off)
│   └── dashboard.py       # Streamlit app for Human-in-the-Loop review
├── data/                  # Evaluation datasets and temporary files
└── requirements.txt
```

### Component Details

#### Pipeline A: The Live Matcher (FastAPI)
The core logic will follow the "fail-fast" or "pass-fast" cascading approach. 
- **Stages 1-4 (CPU Bound):** Handled via standard Python text manipulation. Requests will quickly return a `PASS` or `REJECT` without hitting expensive models if confidence is extremely high or low.
- **Stage 5 (CLIP Pre-filter):** If the fuzzy score is in the ambiguous zone (40-85%), a local CLIP model calculates the cosine similarity between the two logos.
- **Stages 6-7 (LLM Agent):** Only if the visual comparison is still ambiguous do we query the Rule Bank DB for contextual rules (e.g., active rules for the seller's region) and prompt the Vision-LLM for a final verdict.

#### Pipeline B: Rule Scorecard & Dashboard (Streamlit)
- **Evaluator Script:** A background script that takes a ground-truth dataset (e.g., 20 pairs) and runs it through Pipeline A. It will do an A/B test (or ablation study) by running the dataset with a specific rule *included* in the prompt, and then *excluded*.
- **Streamlit Interface:** A web UI displaying the evaluation results. It will show the "lift" (improvement in accuracy) for each rule. A human can click to change the state of a rule to `ACTIVE`, `ARCHIVED`, or `MIGRATED` directly updating the Rule Bank Database.

## Verification Plan

### Automated Tests
- Unit tests for the CPU-bound stages (Regex, Initials, Whitespace, Fuzzy).
- Mock the CLIP and Vision-LLM endpoints to test the cascading orchestration (ensuring requests short-circuit correctly based on scores).

### Manual Verification
- Run a set of mock shop pairs (same name diff logo, different name same logo, completely different, etc.) against the FastAPI endpoint to verify latency and accuracy.
- Launch the Streamlit dashboard, run an evaluation loop with dummy rules, and verify that updating a rule's state in the UI correctly affects the live retrieval in Pipeline A.

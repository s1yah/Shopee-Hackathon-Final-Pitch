# Shopee Matcher 🛍️

A proof-of-concept system developed for the Shopee Hackathon Final Pitch. It evaluates whether two shop listings refer to the same real-world entity by comparing their names and logos.

The project is split into two main pipelines:
*   **Pipeline A (The Live Matcher):** A high-performance FastAPI backend that runs incoming shop pairs through a cascading series of evaluations (Regex -> Fuzzy Matching -> CLIP Vision -> Vision-LLM). It fails fast on obvious mismatches and only invokes expensive ML models on ambiguous cases.
*   **Pipeline B (The Maintenance Harness):** An interactive Streamlit dashboard designed for a Human-in-the-Loop workflow. It evaluates the impact of custom business rules on the matcher's accuracy against a 20-pair ground truth dataset.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.9+
*   Windows (PowerShell) or macOS/Linux (Bash)

### 1. Installation

Clone or download the repository, then navigate to the project folder:

```bash
cd shopee-matcher
```

Create a virtual environment and activate it:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

*(Note: For the hackathon demo, heavy ML packages like `torch` and `transformers` have been omitted and their stages are mocked to ensure the demo runs quickly on standard laptops).*

---

## 🧪 How to Run

### Run the Evaluation Dashboard (Pipeline B)
To view the dataset, evaluate rule performance, and update the Rule Bank:

**Windows:**
```powershell
.\venv\Scripts\python.exe -m streamlit run pipeline_b\dashboard.py
```
**macOS/Linux:**
```bash
python -m streamlit run pipeline_b/dashboard.py
```
The dashboard will open automatically in your browser at `http://localhost:8501`.

### Run the Backend API (Pipeline A)
To test the core cascading matcher directly via an API endpoint:

**Windows:**
```powershell
.\venv\Scripts\python.exe -m uvicorn api.main:app --reload
```
**macOS/Linux:**
```bash
python -m uvicorn api.main:app --reload
```
Once running, navigate to `http://127.0.0.1:8000/docs` in your browser. You can use the interactive Swagger UI to send `POST /match` requests with mock shop data.

---

## 📁 Project Structure

```text
shopee-matcher/
├── api/
│   └── main.py              # FastAPI entry point
├── core/
│   ├── models/              # Pydantic schemas (MatchRequest, MatchResponse, Rule)
│   └── rules/               # Rule retrieval logic (mocked for demo)
├── pipeline_a/
│   ├── matcher.py           # Orchestrator for the cascading pipeline
│   └── stages/              # Individual evaluation stages (s1-s7)
├── pipeline_b/
│   └── dashboard.py         # Streamlit evaluation UI
├── requirements.txt         # Python dependencies
└── README.md                # This document
```

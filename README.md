# CV-to-Job Analyzer — Backend

Backend part of the CV-to-Job Analyzer web application.
Provides REST API for CV analysis, job description parsing, and AI-powered compatibility matching.

---

## Stack

- Python 3.13
- Flask + Flask-CORS
- pypdf
- OpenAI API
- Docker
- GCP Cloud Run

---

## API

### `POST /analyze`

Analyze a CV against a job description.

**Form parameters:**

| Parameter  | Type   | Required | Description                          |
|------------|--------|----------|--------------------------------------|
| `cv_file`  | File   | ✅       | CV in PDF format                     |
| `byText`   | string | —        | `"true"` to use `job_text` (default) |
| `job_text` | string | ✅ if byText | Job description text              |
| `byLink`   | string | —        | `"true"` to use `job_link`           |
| `job_link` | string | ✅ if byLink | URL to a job posting              |

**Response:** JSON with CV analysis, job analysis, matcher results, and summary.

---

### `GET /`

Health check.
```json
{ "message": "CV-to-Job Analyzer API" }
```

---

## Local Setup

**1. Clone the repository**
```bash
git clone <repository_url>
cd <repository_folder>
```

**2. Create `.env` file**
```env
OPENAI_API_KEY=your_openai_api_key
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run**
```bash
python app.py
```

---

## Project Structure
```
agents/           # AI logic modules
  cv_extractor    # CV extraction from PDF
  job_analyzer    # Job description parsing
  job_cv_matcher  # CV ↔ Job matching
  finalizer       # Summary generation
  page_scraper    # Job URL scraper
app.py            # Flask entry point
requirements.txt  # Dependencies
Dockerfile        # Docker configuration
.env              # Environment variables (not committed)
```

---

## Deployment

Deployed to **GCP Cloud Run** via GitHub Actions on push to `main`.

Required GitHub secrets and variables:

| Name                | Type     | Description               |
|---------------------|----------|---------------------------|
| `GCP_SA_KEY`        | Secret   | GCP Service Account JSON  |
| `OPENAI_API_KEY`    | Secret   | OpenAI API key            |
| `GCP_PROJECT_ID`    | Variable | GCP project ID            |
| `ARTIFACT_REPO`     | Variable | Artifact Registry repo    |
| `REGION`            | Variable | GCP region                |
from flask import Flask, request, jsonify
from flask_cors import CORS
from io import BytesIO

from agents.cv_extractor import extract_cv_from_bytes
from agents.job_analyzer import analyze_job_description
from agents.job_cv_matcher import match_cv_to_job
from agents.finalizer import finalist_summary
from agents.page_scraper import scrape_job_text

app = Flask(__name__)
CORS(app)

@app.post("/analyze")
def analyze():
    by_text = request.form.get("byText", "true").lower() == "true"
    by_link = request.form.get("byLink", "false").lower() == "true"

    if "cv_file" not in request.files:
        return jsonify({"error": "cv_file is required"}), 400

    cv_file = request.files["cv_file"]
    cv_bytes = BytesIO(cv_file.read())
    cv_json = extract_cv_from_bytes(cv_bytes)

    job_text = ""
    if by_text:
        if "job_text" not in request.form:
            return jsonify({"error": "job_text is required when byText is true"}), 400
        job_text = request.form["job_text"]
    elif by_link:
        if "job_link" not in request.form:
            return jsonify({"error": "job_link is required when byLink is true"}), 400
        job_link = request.form["job_link"]
        try:
            job_text = " ".join(scrape_job_text(job_link))
        except Exception as e:
            return jsonify({"error": f"Failed to scrape job text: {str(e)}"}), 400
    else:
        return jsonify({"error": "Either byText or byLink must be true"}), 400

    job_json = analyze_job_description(job_text)
    matcher_json = match_cv_to_job(cv_json, job_json)
    summary = finalist_summary(cv_json, job_json, matcher_json)
    return jsonify(summary)


@app.get("/")
def root():
    return jsonify({"message": "CV-to-Job Analyzer API"})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
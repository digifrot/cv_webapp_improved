# app.py
from flask import Flask, render_template, request, send_file
import os
from generator.config import SYSTEM_PROMPT, LINKEDIN_PROFILE
from generator.linkedin_scraper import scrape_linkedin
from generator.cv_builder import generate_cv
from generator.pdf_exporter import save_pdf
from generator.training import save_training_example

app = Flask(__name__)

# ================================
# HOME PAGE
# ================================
@app.route("/")
def index():
    return render_template("index.html", default_prompt=SYSTEM_PROMPT)


# ================================
# GENERATE CV
# ================================
@app.route("/generate", methods=["POST"])
def generate():
    url = request.form.get("linkedin_url")
    custom_prompt = request.form.get("custom_prompt", "").strip()

    # Scrape job details
    job_title, job_desc = scrape_linkedin(url)
    if not job_desc:
        return "Could not extract job description from LinkedIn.", 400

    # Generate CV (HTML/TXT + PDF-safe)
    cv_text, cv_pdf, job_fit_percent = generate_cv(job_desc, custom_prompt)

    return render_template(
        "result.html",
        job_title=job_title,
        job_desc=job_desc,
        cv=cv_text,
        cv_pdf=cv_pdf,
        linkedin_profile=LINKEDIN_PROFILE,
        custom_prompt=custom_prompt,
        job_fit_percent=job_fit_percent,
    )


# ================================
# DOWNLOAD TXT
# ================================
@app.route("/download/txt", methods=["POST"])
def download_txt():
    text = request.form.get("cv_text")
    job_title = request.form.get("job_title", "Job_Position")

    filename = "".join(c if c.isalnum() else "_" for c in job_title) + ".txt"
    path = os.path.join("outputs", f"Liran_Roth_CV_{filename}")

    os.makedirs("outputs", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return send_file(path, as_attachment=True)


# ================================
# DOWNLOAD PDF
# ================================
@app.route("/download/pdf", methods=["POST"])
def download_pdf():
    text = request.form.get("cv_pdf")
    job_title = request.form.get("job_title", "Job_Position")

    safe_name = "".join(c if c.isalnum() else "_" for c in job_title)
    path = os.path.join("outputs", f"Liran_Roth_CV_{safe_name}.pdf")

    os.makedirs("outputs", exist_ok=True)
    save_pdf(text, path)
    return send_file(path, as_attachment=True)


# ================================
# SAVE TRAINING DATA
# ================================
@app.route("/save_training", methods=["POST"])
def save_training():
    data = request.get_json()
    job_desc = data.get("job_desc")
    cv = data.get("cv_text")
    custom_prompt = data.get("custom_prompt")

    save_training_example(job_desc, cv, custom_prompt)
    return "OK", 200


# ================================
# RUN SERVER
# ================================
if __name__ == "__main__":
    app.run(port=5000, debug=True)

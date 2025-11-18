# generator/linkedin_scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_linkedin(url):
    """Extract job title + job description from LinkedIn job page."""
    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    # Job title
    title_tag = soup.find("h1", class_="top-card-layout__title")
    if not title_tag:
        title_tag = soup.find("h1", class_="top-card-layout__headline")

    job_title = title_tag.get_text(strip=True) if title_tag else "Job Position"

    # Job description
    desc_tag = soup.find("div", class_="show-more-less-html__markup")
    job_desc = desc_tag.get_text("\n").strip() if desc_tag else None

    return job_title, job_desc

# generator/config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# User header information (editable via environment variables or defaults)
USER_NAME = os.getenv("USER_NAME", "")
USER_PHONE = os.getenv("USER_PHONE", "")
USER_EMAIL = os.getenv("USER_EMAIL", "")
LINKEDIN_PROFILE = os.getenv("LINKEDIN_PROFILE", "")

SYSTEM_PROMPT = (
    "You are a professional CV editor.\n\n"
    "Rules:\n"
    "- Tailor the CV using ONLY existing content from the base CV.\n"
    "- Keep only what is relevant for the specific role.\n"
    "- Do NOT add name/contact info (added externally).\n"
    "- Start with SUMMARY.\n"
    "- No hallucinations, no invented skills, no fake experience.\n"
    "- No markdown symbols.\n"
    "- Sections: SUMMARY, EXPERIENCE, SKILLS, EDUCATION & CERTIFICATIONS, LANGUAGES, PERSONAL PROJECTS.\n"
    "- Clear, short paragraphs.\n"
    "- 1.5 pages max.\n"
)

import re
import spacy

nlp = spacy.load("en_core_web_sm")


# -------------------------------------------------
# SECTION KEYWORDS
# -------------------------------------------------

SECTION_HEADERS = {
    "education": ["education", "academic"],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship",
        "internships",
        "technical and research experience",
    ],
    "skills": [
        "skills",
        "technical skills",
        "technologies",
        "programming languages",
    ],
    "projects": [
        "projects",
        "academic projects",
        "personal projects",
    ],
    "certifications": [
        "certification",
        "certifications",
    ],
    "achievements": [
        "achievement",
        "achievements",
    ],
    "extracurricular": [
        "extracurricular",
        "positions of responsibility",
        "leadership",
    ],
}


# -------------------------------------------------
# NAME
# -------------------------------------------------

def extract_name(text):

    for line in text.split("\n"):

        line = line.strip()

        if (
            line
            and "@" not in line
            and len(line.split()) >= 2
            and len(line) < 40
        ):
            return line.title()

    return ""


# -------------------------------------------------
# EMAIL
# -------------------------------------------------

def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )

    return match.group() if match else ""


# -------------------------------------------------
# PHONE
# -------------------------------------------------

def extract_phone(text):

    match = re.search(
        r"(\+?\d[\d\s-]{8,}\d)",
        text,
    )

    return match.group() if match else ""


# -------------------------------------------------
# SECTION PARSER
# -------------------------------------------------

def extract_sections(text):

    sections = {}

    current = "header"

    sections[current] = []

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        found = False

        for section, keywords in SECTION_HEADERS.items():

            if any(keyword in lower for keyword in keywords):

                current = section

                if current not in sections:
                    sections[current] = []

                found = True
                break

        if found:
            continue

        sections[current].append(line)

    return sections


# -------------------------------------------------
# MAIN PARSER
# -------------------------------------------------

def parse_resume(text):

    return {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "sections": extract_sections(text),

    }
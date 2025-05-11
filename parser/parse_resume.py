
import re
import spacy
from .extract_text import extract_text_from_pdf

nlp = spacy.load("en_core_web_sm")

def extract_name(text):
    raw_lines = text.split("\n")
    blacklist_keywords = [
        "python", "c++", "java", "tensorflow", "mongodb", "eclipse", "github",
        "linkedin", "email", "skills", "objective", "contact", "resume", "intern",
        "opshift", "engineer"
    ]

    for line in raw_lines[:15]:
        line = line.strip()
        if (
            line.isupper() and
            2 <= len(line.split()) <= 4 and
            all(w.isalpha() for w in line.split()) and
            not any(kw in line.lower() for kw in blacklist_keywords)
        ):
            return line.title()

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return "Unknown"

def extract_section(lines, start_headers, stop_headers):
    capture = False
    result = []

    for line in lines:
        lower_line = line.lower().strip()

        if any(start.lower() == lower_line for start in start_headers):
            capture = True
            continue

        if capture:
            if any(stop.lower() == lower_line for stop in stop_headers):
                break
            if line.strip():
                result.append(line.strip())

    return result

def parse_resume(text: str) -> dict:
    data = {}
    lines = text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    data["name"] = extract_name(text)

    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    email = email_match.group(0) if email_match else None
    # Email fix
    if email:
        email = email.replace("Q", "@").replace("@@", "@")
    data["email"] = email

    skills_keywords = [
        "Python", "C++", "Java", "TensorFlow", "Scikit-Learn", "React",
        "HTML", "CSS", "SQL", "MongoDB", "OpenShift", "Eclipse", "Mercurial"
    ]
    data["skills"] = [skill for skill in skills_keywords if skill.lower() in text.lower()]

    data["education"] = extract_section(
        lines,
        ["EDUCATION"],
        ["PROJECTS", "AWARDS", "PUBLICATIONS", "SKILLS", "EXPERIENCE", "CAREER OBJECTIVE", "LEADERSHIP", "VOLUNTEER"]
    )

    data["experience"] = extract_section(
        lines,
        ["WORK EXPERIENCE", "EXPERIENCE", "PROFESSIONAL EXPERIENCE"],
        ["PROJECTS", "AWARDS", "PUBLICATIONS", "SKILLS", "EDUCATION", "CAREER OBJECTIVE", "LEADERSHIP", "VOLUNTEER", "MISC", "PROJECTS/RESEARCH WORK"]
    )

    data["projects"] = extract_section(
        lines,
        ["PROJECTS", "PROJECTS/RESEARCH WORK", "RESEARCH WORK"],
        ["AWARDS", "PUBLICATIONS", "SKILLS", "EDUCATION", "WORK EXPERIENCE", "LEADERSHIP", "VOLUNTEER", "MISC","LEADERSHIP", "VOLUNTEER", "LEADERSHIP & VOLUNTEER EXPERIENCE", "EXTRACURRICULAR", "MISC" ]
    )

    data["awards"] = extract_section(
        lines,
        ["AWARDS", "ACHIEVEMENTS"],
        ["PROJECTS", "PUBLICATIONS", "SKILLS", "EDUCATION", "WORK EXPERIENCE"]
    )

    data["publications"] = extract_section(
        lines,
        ["PUBLICATIONS"],
        ["REFERENCES", "LEADERSHIP", "VOLUNTEER", "SKILLS", "EDUCATION"]
    )

    data["miscellaneous"] = extract_section(
        lines,
        ["LEADERSHIP", "VOLUNTEER", "LEADERSHIP & VOLUNTEER EXPERIENCE", "EXTRACURRICULAR", "MISC"],
        ["REFERENCES", "SKILLS", "EDUCATION"]
    )

    # ✅ Deduplicate content in major sections
    for key in ["experience", "projects", "miscellaneous"]:
        if key in data:
            seen = set()
            unique_lines = []
            for line in data[key]:
                if line not in seen:
                    unique_lines.append(line)
                    seen.add(line)
            data[key] = unique_lines

    return data

# utils/parser.py

from io import BytesIO
import re
import fitz  # PyMuPDF

# 1) Extract raw text from PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=BytesIO(file.read()), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

# 2) Basic cleanup
def clean_text(text: str) -> str:
    text = text.replace("\u00a0", " ")  # non-breaking spaces
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

# 3) Heuristic section splitter using common resume headings
SECTION_PATTERNS = {
    "summary": r"(summary|profile|objective)",
    "experience": r"(experience|work experience|employment history)",
    "education": r"(education)",
    "skills": r"(skills|technical skills|tech skills)",
    "projects": r"(projects|personal projects)",
    "certifications": r"(certifications|licenses|certs)"
}

def split_sections(text: str) -> dict:
    # Build a combined regex to find headings
    pattern = r"(?im)^\s*(?:{})\s*:?$".format("|".join(SECTION_PATTERNS.values()))
    # Find all headings and their positions
    matches = list(re.finditer(pattern, text))
    sections = {}
    if not matches:
        return sections  # nothing matched, return empty and fall back to raw text

    # Grab blocks between headings
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        heading = m.group(0).strip().lower()
        normalized = None
        for key, pat in SECTION_PATTERNS.items():
            if re.search(rf"(?i)\b{pat}\b", heading):
                normalized = key
                break
        if normalized:
            sections[normalized] = text[start:end].strip()

    return sections

# 4) Contact info extraction
EMAIL_RE = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
PHONE_RE = r"(\+?\d[\d\-\(\) ]{7,}\d)"
URL_RE = r"(https?://[^\s)]+|www\.[^\s)]+)"

def extract_contact_info(text: str) -> dict:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    email = re.search(EMAIL_RE, text)
    phone = re.search(PHONE_RE, text)
    urls = re.findall(URL_RE, text)
    # Guess name from the very first non-empty line if it does not look like a heading
    possible_name = lines[0] if lines else ""
    if re.search(r"(?i)(resume|curriculum|summary|experience)", possible_name):
        possible_name = ""
    return {
        "name": possible_name,
        "email": email.group(0) if email else "",
        "phone": phone.group(0) if phone else "",
        "links": list(dict.fromkeys(urls))  # de-dup while preserving order
    }

# 5) Skills matching from a lightweight dictionary
DEFAULT_SKILLS = [
    # languages
    "python", "javascript", "typescript", "java", "c++", "sql",
    # data
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    # web
    "react", "angular", "flask", "django", "fastapi",
    # cloud and devops
    "aws", "gcp", "azure", "docker", "kubernetes", "git",
]

def match_skills(text: str, skills_list=None):
    skills_list = skills_list or DEFAULT_SKILLS
    lower = text.lower()
    found = [s for s in skills_list if re.search(rf"\b{re.escape(s.lower())}\b", lower)]
    return sorted(set(found))

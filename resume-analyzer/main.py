# Click run, preview tab should populate, and follow prompt to upload pdf resume.

import json
import streamlit as st
from utils.parser import (
    extract_text_from_pdf,
    clean_text,
    split_sections,
    extract_contact_info,
    match_skills,
)

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("AI Powered Resume Analyzer")

# File uploader
uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if not uploaded:
    st.info("Upload a PDF resume to begin.")
    st.stop()

# Extract + clean
raw_text = extract_text_from_pdf(uploaded)
text = clean_text(raw_text)

# Contact and sections
contact = extract_contact_info(text)
sections = split_sections(text)

# Fallback when headings are not present
if not sections:
    sections = {"summary": text}

# Skills detection from entire text
detected_skills = match_skills(text)

# 1) Header area with key info
left, mid, right = st.columns([1.5, 1, 1])
with left:
    st.subheader(contact.get("name") or "Name not detected")
    st.write(f"**Email:** {contact.get('email') or 'N/A'}")
    st.write(f"**Phone:** {contact.get('phone') or 'N/A'}")
with mid:
    st.metric("Detected Skills", len(detected_skills))
    st.write(", ".join(detected_skills) or "None detected")
with right:
    if contact.get("links"):
        st.write("**Links**")
        for link in contact["links"]:
            st.write(f"- {link}")

st.markdown("---")

# 2) Score breakdown
score = 0
reasons = []

def has_content(key): 
    return key in sections and sections[key].strip()

needed = ["summary", "experience", "education", "skills"]
for key in needed:
    if has_content(key):
        score += 1
    else:
        reasons.append(f"Missing or empty **{key.title()}** section.")

if len(detected_skills) >= 5:
    score += 1
else:
    reasons.append("Add more concrete technical skills.")

# Display score
st.subheader("Score")
st.progress(min(score / 5, 1.0))
st.write(f"**{score} out of 5**")
if reasons:
    st.warning("Improvements:")
    for r in reasons:
        st.write(f"- {r}")

st.markdown("---")

# 3) Render sections nicely
def render_block(title, content):
    st.subheader(title)
    if not content:
        st.caption("No content found.")
        return
    # Split bullets by line for simple formatting
    lines = [l.strip("•- \t") for l in content.splitlines() if l.strip()]
    for line in lines:
        st.write(f"- {line}")

# Two column layout for readability
colA, colB = st.columns(2)
with colA:
    render_block("Summary", sections.get("summary", ""))
    render_block("Experience", sections.get("experience", ""))
    render_block("Projects", sections.get("projects", ""))

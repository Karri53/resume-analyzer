# AI-Powered Resume Analyzer

An interactive Streamlit web app that extracts and evaluates resume content from PDF files, giving instant feedback on completeness and keyword usage.  
Built as a personal project to demonstrate skills in Python, NLP, and web app deployment.

---

## Features
- **PDF Resume Parsing** – Extracts text from uploaded PDF resumes using PyMuPDF.
- **Keyword & Section Scoring** – Checks for essential sections (Summary, Skills, Education, Projects).
- **Real-time Feedback** – Generates suggestions to improve resume content.
- **Structured Output** – Displays extracted sections in a clean, organized format.
- **Web App Interface** – Fully interactive UI built with Streamlit.

---

## Tech Stack
- **Language**: Python 3
- **Framework**: Streamlit
- **Libraries**: PyMuPDF, io, re
- **Deployment**: Replit (Cloud-hosted, browser-accessible)

---


## Project Structure
```bash
Resume-Analyzer/
│
├── utils/
│   ├── __init__.py
│   ├── parser.py          # Extracts text from PDFs
│
├── main.py                # Streamlit UI + Resume analysis logic
├── .replit                # Replit configuration
├── pyproject.toml         # Dependencies
└── README.md              # Project documentation

import os
import zipfile
import base64
import io
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

from readme_utils import analyze_project_files
from prompts import README_PROMPT

# Setup
st.set_page_config(page_title="AI README.md Generator")
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("📄 AI README.md Generator")
uploaded_zip = st.file_uploader("Upload your Project ZIP", type=["zip"])

def get_gemini_response(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

def extract_zip(uploaded_file):
    extract_path = "uploads"
    os.makedirs(extract_path, exist_ok=True)
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        zip_ref.extractall(extract_path)
    return extract_path

if uploaded_zip:
    st.success("✅ ZIP uploaded successfully!")
    extract_path = extract_zip(uploaded_zip)
    code_summary, tech_stack = analyze_project_files(extract_path)

    # Prepare input for Gemini
    structured_input = f"""
    Code Summary:
    {code_summary}

    Tech Stack Detected:
    {tech_stack}
    """

    # Generate README
    final_prompt = README_PROMPT.format(project_summary=structured_input)
    if st.button("🪄 Generate README.md"):
        readme_text = get_gemini_response(final_prompt)
        st.subheader("📄 Your Auto-Generated README.md:")
        st.code(readme_text, language="markdown")

import os

# Common libraries you want to detect
TECH_KEYWORDS = [
    "tensorflow", "torch", "flask", "streamlit", "sklearn", "pandas", "numpy",
    "matplotlib", "seaborn", "xgboost", "cv2", "nltk", "spacy", "requests"
]

def analyze_project_files(folder_path):
    summary = ""
    tech_stack = set()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()
                        summary += f"\n\n--- File: {file_path} ---\n{code[:1500]}"  # Truncate for Gemini

                        for keyword in TECH_KEYWORDS:
                            if keyword in code:
                                tech_stack.add(keyword)
                except Exception as e:
                    summary += f"\n\n[Could not read {file_path}: {str(e)}]"

    return summary.strip(), ", ".join(sorted(tech_stack)) or "Standard Python"


README_PROMPT = '''
You are a professional documentation generator.

Based on the following code summary and tech stack, write a clean, well-structured, and professional `README.md` file for a GitHub project.

Please include:
1. Project title
2. Short project overview
3. Detected tech stack
4. Folder and file structure
5. Installation instructions
6. How to run the project
7. Example usage
8. License (if not specified, assume MIT)

Here is the extracted content:
{project_summary}
'''

import base64
import io
import os
import re

import streamlit as st
import PyPDF2 as pdf
import pdf2image
import pytesseract
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Setup Streamlit page
st.set_page_config(page_title="ATS Resume Expert")

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Helper Functions ---

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF, fallback to OCR if needed."""
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    if not text.strip():
        # Fallback to OCR
        uploaded_file.seek(0)
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        for image in images:
            text += pytesseract.image_to_string(image)
    return text

def clean_text(text):
    """Clean extracted text."""
    text = text.encode('ascii', 'ignore').decode()
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def split_text(text, max_length=4000):
    """Split text into chunks for Gemini."""
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

def input_pdf_setup(uploaded_file):
    """Convert PDF to image parts if fallback needed (not used now, but kept)."""
    if uploaded_file is not None:
        uploaded_file.seek(0)
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        pdf_parts = []
        for page in images:
            img_byte_arr = io.BytesIO()
            page.save(img_byte_arr, format="JPEG")
            img_byte_arr = img_byte_arr.getvalue()
            pdf_parts.append({
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            })
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

def get_gemini_response(input_text, pdf_content, prompt):
    """Send request to Gemini model."""
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([input_text] + pdf_content + [prompt])
    return response.text

# --- Stronger Prompts ---

input_prompt1 = """
You are an expert Technical Recruiter specializing in Data Science, Artificial Intelligence, Machine Learning, Deep Learning, Natural Language Processing (NLP), Generative AI, MLOps, and Cloud Computing (AWS, Azure, Google Cloud, etc.).
Evaluate the candidate’s resume against the job description carefully.
Focus especially on relevant skills, technologies, certifications, and project experiences in these fields.
Please do the following:
- Summarize the candidate's key strengths and skills relevant to the data science/AI/cloud domain.
- Highlight any major gaps, missing tools/skills, or weak areas.
- Suggest specific improvements to better align the resume with the job requirements in these technical areas.
Respond in a clear, professional, and structured manner.
"""

input_prompt3 = """
You are acting as a smart ATS (Applicant Tracking System) specializing in Data Science, Artificial Intelligence, Machine Learning, Deep Learning, NLP, Generative AI, MLOps, and Cloud Computing (AWS, Azure, Google Cloud, etc.).
Your task:
- Analyze the resume and the job description carefully.
- Provide an overall **percentage match score** based on skills, tools, technologies, experience, certifications, and keywords in these areas.
- List **missing important keywords** especially related to data science, AI, cloud platforms, and other technical fields.
- Give **final professional advice** on how to improve the resume to become a stronger candidate for technical data-related roles.

Structure your response clearly:
- Percentage Match: xx%
- Missing Keywords: [list]
- Final Thoughts: [summary]
"""

# --- Streamlit UI ---

st.header("📄 ATS Resume Expert")

input_text = st.text_area("📋 Paste the Job Description here:", key="input")
uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ Resume Uploaded Successfully!")

# Buttons
submit1 = st.button("📖 Review My Resume")
submit3 = st.button("📊 Check ATS Match Percentage")

if submit1 or submit3:
    if uploaded_file is not None and input_text.strip() != "":
        resume_text = extract_text_from_pdf(uploaded_file)
        resume_text = clean_text(resume_text)
        
        if len(resume_text.strip()) > 100:
            pdf_content = split_text(resume_text)
        else:
            pdf_content = input_pdf_setup(uploaded_file)  # rare fallback
        
        if submit1:
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
        elif submit3:
            response = get_gemini_response(input_text, pdf_content, input_prompt3)

        st.subheader("📝 Response")
        st.write(response)

        # Show progress bar if Percentage Match available
        if "Percentage Match:" in response:
            try:
                percentage = int(response.split("Percentage Match:")[1].split("%")[0].strip())
                st.progress(percentage)
            except Exception as e:
                st.warning("Could not detect percentage properly.")

        # Downloadable ATS report
        st.download_button('⬇️ Download ATS Report', response, file_name='ats_report.txt')

    else:
        st.error("🚨 Please upload your resume and paste the job description.")


import base64
import io
import os

from dotenv import load_dotenv
import streamlit as st
st.set_page_config(page_title="ATS Resume Expert")

import PyPDF2 as pdf
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        uploaded_file.seek(0)  # Reset file pointer after reading text
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
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([input_text] + pdf_content + [prompt])
    return response.text

# Streamlit UI
st.header("ATS Tracking System")
input_text = st.text_area("Paste the Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully!")

submit1 = st.button("Tell Me About The Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Evaluate the resume against the provided job description. 
Give me the percentage match if the resume matches the job description.
First, show the output as percentage match, then missing keywords, and finally final thoughts.
"""

if submit1:
    if uploaded_file is not None and input_text.strip() != "":
        resume_text = extract_text_from_pdf(uploaded_file)
        if len(resume_text.strip()) > 100:
            # Text is good, use plain string
            pdf_content = [resume_text]
        else:
            # Fallback to images
            pdf_content = input_pdf_setup(uploaded_file)
        
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.error("Please upload resume and paste job description.")

elif submit3:
    if uploaded_file is not None and input_text.strip() != "":
        resume_text = extract_text_from_pdf(uploaded_file)
        if len(resume_text.strip()) > 100:
            pdf_content = [resume_text]
        else:
            pdf_content = input_pdf_setup(uploaded_file)

        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.error("Please upload resume and paste job description.")


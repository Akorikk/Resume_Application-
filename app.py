
"""
load_dotenv()

import streamlit as st 
import os 
from PIL import Image
import pdf2image 
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:

     image = pdf2image.convert_from_bytes(uploaded_file.read())

    first_page=image[0]

    img_bytes_arr = io.BytesIO()
    first_page.save(img_bytes_arr, format="JPEG")
    img_bytes_arr = img_bytes_arr.getvalue()

    pdf_part = [
        {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_bytes_arr).decode()
        }
    ]
    return pdf_part
"""

import base64
import io
import os

from dotenv import load_dotenv
import streamlit as st
st.set_page_config(page_title="ATS Resume Expert")
from PIL import Image
import pdf2image
import google.generativeai as genai


# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_bytes_arr = io.BytesIO()
        first_page.save(img_bytes_arr, format="JPEG")
        img_bytes_arr = img_bytes_arr.getvalue()

        pdf_part = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_bytes_arr).decode()
            }
        ]
        return pdf_part
    else:
        raise FileNotFoundError("No File Uploaded")
    


st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file =st.file_uploader("Upload your resume(pdf)",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully!")

submit1 =st.button("Tell Me About The Resume")
submit2 =st.button("How Can I Imporovise my Skills?")
submit3 =st.button("Percentage Match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")



   





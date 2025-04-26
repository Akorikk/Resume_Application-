import base64
import io
from dotenv import load_dotenv
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
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
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

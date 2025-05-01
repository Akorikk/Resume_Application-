import google.generativeai as genai
import PyPDF2 as pdf 
import json

def config_genai(api_key):
    """"Configure the Generative AI API"""
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        raise Exception(f"Faild to configure Generative AI {str(e)}")    

def extract_pdf_text(uploaded_file):

    try:
        reader = pdf.PdfReader(uploaded_file)
        if len(reader.pages) == 0:
            raise Exception("PDF file is empty")

        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

            if not text:
                raise Exception("no text could be extract from the PDF")

            return  ' '.join(text)
        
    except Exception as e:
        raise Exception(f"Error Extracting PDF text: {str(e)}")
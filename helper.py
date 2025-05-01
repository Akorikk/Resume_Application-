import google.generativeai as genai
import PyPDF2 as pdf 
import json

def config_genai(api_key):
    """"Configure the Generative AI API"""
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        raise Exception(f"Faild to configure Generative AI {str(e)}")    
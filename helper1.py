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
        
        """ reader.pages: This refers to the list of pages in the PDF document.
len(reader.pages): This gives the number of pages in the PDF.
If the PDF has no pages (i.e., the length of reader.pages is 0),
 the function raises an exception with the message "PDF file is empty"."""

        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

            if not text:
                raise Exception("no text could be extract from the PDF")

            return  ' '.join(text)
        '''    
        ' '.join(text): Joins all the text chunks (from each page) into a single string, separating them by spaces.
        
        text = ['Hello from page 1', 'Hello from page 2']

# With join
joined_text = ' '.join(text)
print(joined_text)
# Output: Hello from page 1 Hello from page 2

# Without join
print(text)
# Output: ['Hello from page 1', 'Hello from page 2']
        '''    
    except Exception as e:
        raise Exception(f"Error Extracting PDF text: {str(e)}")
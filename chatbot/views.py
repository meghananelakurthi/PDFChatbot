import os
import fitz  # PyMuPDF
import logging
from django.shortcuts import render
from .forms import PDFUploadForm
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Setup logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

# API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBnr0lTwAnyBm9QwnwCWGWnVONWKelSO7w")
API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyAUZMCOc_RAHDZTM2hfVcEv2PBBpS1CZA4")
# API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyC3h11C3oYmo5j0bgPEcGMfNw9AK2wIftU")
# API_KEY = os.getenv("HUGGING_FACE_API_KEY", "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")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=API_KEY
)

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
    return text.strip()


def pdf_qa_view(request):
    response = ""
    last_question = ""
    last_answer = ""
    
    # Initialize or clear session variables on page refresh
    if request.method == 'GET':
        # This logic will run when the page is refreshed (GET request)
        if 'previous_conversation' in request.session:
            # Clear the conversation history on refresh
            del request.session['previous_conversation']

    # Handle PDF upload
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)

        if form.is_valid() and 'pdf_file' in request.FILES:
            pdf_file = request.FILES['pdf_file']
            pdf_text = extract_text_from_pdf(pdf_file)

            if pdf_text:
                request.session['pdf_text'] = pdf_text
                response = "PDF uploaded successfully. You can now ask questions."
            else:
                response = "The uploaded PDF is empty or cannot be read."

        # Handle questions
        elif 'question' in request.POST:
            question = form.cleaned_data['question']
            pdf_text = request.session.get('pdf_text', "")
            
            # Initialize conversation history if it doesn't exist
            if 'previous_conversation' not in request.session:
                request.session['previous_conversation'] = []

            if pdf_text:
                prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", "You are a chatbot knowledgeable about the provided document."),
                        ("human", f"Question: {question}\nContext: {pdf_text}")
                    ]
                )
                output_parser = StrOutputParser()
                chain = prompt | llm | output_parser

                logging.info(f"Question: {question}")
                logging.info(f"Context (truncated): {pdf_text[:100]}...")  # Log the first 100 chars

                try:
                    answer = chain.invoke({'question': question, 'context': pdf_text})
                    answer = answer.replace('*', '').strip()  # Clean the answer
                    logging.info(f"Response: {answer}")

                    # Prepend the current question and answer in the session
                    request.session['previous_conversation'].insert(0, {
                        'question': question,
                        'answer': answer
                    })

                    # Update last_question and last_answer for display
                    last_question = question
                    last_answer = answer

                except Exception as e:
                    response = f"Error while querying the API: {e}"
            else:
                response = "Please upload a PDF first."
    
    else:
        form = PDFUploadForm()

    # Retrieve previous conversation for display (it will already be in the desired order)
    previous_conversation = request.session.get('previous_conversation', [])

    return render(request, 'chatbot/index.html', {
        'form': form,
        'last_question': last_question,
        'last_answer': last_answer,
        'response': response,
        'previous_conversation': previous_conversation
    })


# import os
# import fitz  # PyMuPDF
# import logging
# from django.shortcuts import render
# from .forms import PDFUploadForm
# from dotenv import load_dotenv
# import requests

# # Setup logging
# logging.basicConfig(level=logging.INFO)

# load_dotenv()

# HUGGINGFACE_API_KEY = os.getenv("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")

# def extract_text_from_pdf(pdf_file):
#     text = ""
#     try:
#         with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
#             for page in doc:
#                 text += page.get_text()
#     except Exception as e:
#         logging.error(f"Error reading PDF: {e}")
#     return text.strip()

# def query_huggingface_model(question, context):
#     headers = {
#         "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
#     }
    
#     payload = {
#         "inputs": f"Context: {context}\nQuestion: {question}",
#         "options": {
#             "use_cache": False
#         }
#     }
    
#     response = requests.post(
#         "https://api-inference.huggingface.co/models/distilbert-base-uncased-distilled-squad",
#         headers=headers,
#         json=payload
#     )
    
#     if response.status_code == 200:
#         return response.json()[0]['generated_text'].strip()
#     else:
#         logging.error(f"Error querying Hugging Face model: {response.text}")
#         return "Error querying model."

# def pdf_qa_view(request):
#     response = ""
#     last_question = ""
#     last_answer = ""
    
#     # Initialize or clear session variables on page refresh
#     if request.method == 'GET':
#         if 'previous_conversation' in request.session:
#             del request.session['previous_conversation']

#     # Handle PDF upload
#     if request.method == 'POST':
#         form = PDFUploadForm(request.POST, request.FILES)

#         if form.is_valid() and 'pdf_file' in request.FILES:
#             pdf_file = request.FILES['pdf_file']
#             pdf_text = extract_text_from_pdf(pdf_file)

#             if pdf_text:
#                 request.session['pdf_text'] = pdf_text
#                 response = "PDF uploaded successfully. You can now ask questions."
#             else:
#                 response = "The uploaded PDF is empty or cannot be read."

#         # Handle questions
#         elif 'question' in request.POST:
#             question = form.cleaned_data['question']
#             pdf_text = request.session.get('pdf_text', "")
            
#             if 'previous_conversation' not in request.session:
#                 request.session['previous_conversation'] = []

#             if pdf_text:
#                 logging.info(f"Question: {question}")
#                 logging.info(f"Context (truncated): {pdf_text[:100]}...")  # Log the first 100 chars

#                 try:
#                     answer = query_huggingface_model(question, pdf_text)
#                     logging.info(f"Response: {answer}")

#                     request.session['previous_conversation'].insert(0, {
#                         'question': question,
#                         'answer': answer
#                     })

#                     last_question = question
#                     last_answer = answer

#                 except Exception as e:
#                     response = f"Error while querying the model: {e}"
#             else:
#                 response = "Please upload a PDF first."
    
#     else:
#         form = PDFUploadForm()

#     previous_conversation = request.session.get('previous_conversation', [])

#     return render(request, 'chatbot/index.html', {
#         'form': form,
#         'last_question': last_question,
#         'last_answer': last_answer,
#         'response': response,
#         'previous_conversation': previous_conversation
#     })

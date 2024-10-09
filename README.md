# PDFChatbot App

## Description
PDFChatBot is an innovative chatbot designed to help users interact seamlessly with PDF documents. It enables users to ask questions, extract information, and perform actions within their PDFs through Langchain, making document management easier and more efficient. Whether you need to summarize content or find specific sections, PDFChatBot is your go-to assistant for all PDF-related tasks.

## Features
- Intuitive user interface for a smooth user experience.
- Seamless integration with various external services, enhancing functionality and versatility.

## Technologies Used
- **Python** and **Django** for chatbot app creation.
- **AWS EC2** for app deployment.

## Installations

### Clone the Repository
  ```bash
    git clone https://github.com/meghananelakurthi/PDFChatbot/
    cd pdfchatbot
  ```

### Create a Virtual Environment
  ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```
### Install Required Packages 
- Django
- PyMuPDF
- python-dotenv
- langchain-core
- langchain-google-genai
### Then run:
```bash
   pip install -r requirements.txt
```

### Run Migrations (if using Django)
```bash
   python manage.py migrate
```

### Start the Server
```bash
   python manage.py runserver
```

### USAGE:
### Interacting with the Chatbot
- Upload a PDF Document: Click the "Upload" button to select and upload a PDF file.

- Ask Questions About the PDF: Inquire about topics or summaries after uploading.

- Extract Specific Information: Request specific details or definitions from the document.

### CONTRIBUTION:
1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch`
3. Make your changes and commit them
4. Push to the branch: `git push origin feature-branch`
5. Create a Pull Request


### RESOURCES
### YouTube Videos
- Know About AI Models
  - [Video Tutorial 1](https://www.youtube.com/watch?v=xP_ZON_P4Ks&list=PLeo1K3hjS3uuyHkzjBfd3nwD7SJ5C11aB)

- Know About Langchain
  - [Video Tutorial 2](https://www.youtube.com/watch?v=aywZrzNaKjs&t=700s)

- Deploying
  - [Video Tutorial 3](https://www.youtube.com/watch?v=uiPSnrE6uWE)
  
### Google
- Explore Google’s resources and documentation on relevant technologies to deepen our knowledge and skills.

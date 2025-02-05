from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
import os
import requests
import charset_normalizer
import mimetypes
from docx import Document  # For handling .docx files
from PyPDF2 import PdfReader

app = Flask(__name__)

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '123456'
Session(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Hyperbolic API Configuration
API_URL = "https://api.hyperbolic.xyz/v1/chat/completions"
API_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYWNoZWFsLmxlZUBmbGV4aW5mcmEuY29tLm15IiwiaWF0IjoxNzM2MTQ3MzY2fQ.TDeyieSxa7NbESTSKvIZSQXTxQYOR0UxkoZSBsxuSXk"
}

# Store conversation state
conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    role = request.form.get('role', 'user')  # Default to "user" if no role provided
    content = request.form.get('content')
    file = request.files.get('file')

    if not content:
        return "Content is required.", 400

    # Process uploaded file if provided
    document_content = ""
    if file and file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        document_content = process_document(file_path)

        # Store the file content in session
        session['uploaded_file_content'] = document_content
    else:
        # Retrieve stored file content from session
        document_content = session.get('uploaded_file_content', '')

    # Append document content to user input if applicable
    if document_content:
        content = f"{content}\n\n{document_content}"

    # Append the new user message to conversation history
    conversation_history.append({"role": role, "content": content})

    # Prepare API payload with conversation history
    data = {
        "messages": conversation_history,
        "model": "deepseek-ai/DeepSeek-V3",
        "max_tokens": 512,
        "temperature": 0.1,
        "top_p": 0.9,
        "stream": False
    }

    # Make API request
    response = requests.post(API_URL, headers=API_HEADERS, json=data)
    if response.status_code == 200:
        ai_response = response.json()
        return jsonify(ai_response) # Ensure this sends the correct JSON format
    else:
        return jsonify({"error": response.text}), response.status_code

def process_document(file_path):
    """
    Reads the file content with support for .docx and text files.
    """
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        try:
            doc = Document(file_path)
            content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            content = f"Error reading .docx file: {str(e)}"
    else:
        try:
            with open(file_path, 'rb') as f:
                result = charset_normalizer.detect(f.read())
                encoding = result['encoding'] or 'utf-8'
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
        except Exception as e:
            content = f"Error reading file: {str(e)}"

    return content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

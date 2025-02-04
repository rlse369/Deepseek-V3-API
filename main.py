from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
import os
import requests
from config import Config
from utils import process_document

app = Flask(__name__)

# Load configurations
app.config.from_object(Config)
Session(app)

conversation_history = []  # Store conversation state

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    role = request.form.get('role', 'user')
    content = request.form.get('content')
    file = request.files.get('file')

    if not content:
        return jsonify({"error": "Content is required"}), 400

    document_content = ""
    if file and file.filename:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        document_content = process_document(file_path)
        session['uploaded_file_content'] = document_content
    else:
        document_content = session.get('uploaded_file_content', '')

    if document_content:
        content += f"\n\n{document_content}"

    conversation_history.append({"role": role, "content": content})

    response = requests.post(
        Config.API_URL,
        headers=Config.API_HEADERS,
        json={
            "messages": conversation_history,
            "model": "deepseek-ai/DeepSeek-V3",
            "max_tokens": 512,
            "temperature": 0.1,
            "top_p": 0.9,
            "stream": False
        }
    )

    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

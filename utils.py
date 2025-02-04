import mimetypes
import charset_normalizer
from docx import Document
from PyPDF2 import PdfReader

def process_document(file_path):
    """ Reads and extracts text from supported document formats """
    mime_type, _ = mimetypes.guess_type(file_path)

    try:
        if mime_type == "application/pdf":
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        else:
            with open(file_path, 'rb') as f:
                encoding = charset_normalizer.detect(f.read())['encoding'] or 'utf-8'
            
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
    
    except Exception as e:
        return f"Error reading file: {str(e)}"

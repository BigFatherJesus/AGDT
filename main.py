import os
import time
import io
import openai
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from docx import Document
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
client = OpenAI()

# Setup Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=credentials)

def list_files(folder_id):
    """List all files in the specified Google Drive folder."""
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        pageSize=10, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])
    return items

def download_file(file_id, file_name):
    """Download a file from Google Drive."""
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

def upload_file(file_name, folder_id):
    """Upload a file to Google Drive."""
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_name, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")}')

def translate_text(text):
    lines = text.split("\n")
    chunks = []
    chunk = []
    for i, line in enumerate(lines):
        chunk.append(line)
        if (i + 1) % 125 == 0 or i == len(lines) - 1:
            chunks.append("\n".join(chunk))
            chunk = []

    translated_chunks = []
    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a highly specialized AI trained in translating subtitles to {os.getenv('OUTPUT_LANGUAGE')}. Your proficiency in {os.getenv('OUTPUT_LANGUAGE')} is well above university level, ensuring translations are accurate and nuanced. You will be provided with a sentence in English, German, or another non-{os.getenv('OUTPUT_LANGUAGE')} language, and your task is to translate it into {os.getenv('OUTPUT_LANGUAGE')}. Please adhere to the following guidelines: Accuracy: Ensure the translation is precise and maintains the original meaning. Brevity: The translation should be concise and not significantly longer than the original sentence to fit within subtitle constraints. Formatting: Preserve the formatting and timecodes as provided. Cultural Sensitivity: Be aware of cultural context and idiomatic expressions to make translations natural and appropriate for {os.getenv('OUTPUT_LANGUAGE')} audiences. The translations are intended for national television subtitles, so high quality and appropriateness are essential."},
                {"role": "user", "content": chunk}
            ]
        )
        choices = response.choices
        translated_chunk = choices[0].message.content
        # Remove "plaintext" and backticks
        translated_chunk = translated_chunk.replace("```plaintext", "").replace("```", "").replace("```", "")
        translated_chunks.append(translated_chunk)

    translated_text = "\n".join(translated_chunks)
    return translated_text

def translate_file(file_path, file_type):
    """Translate the contents of a text file and return the translated content."""
    if file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':  # .docx
        doc = Document(file_path)
        translated_paragraphs = []
        for paragraph in doc.paragraphs:
            text = paragraph.text
            translated_text = translate_text(text)
            translated_paragraphs.append(translated_text)
        
        new_doc = Document()
        for paragraph in translated_paragraphs:
            new_doc.add_paragraph(paragraph)
        
        file_name, file_extension = os.path.splitext(file_path)
        new_file_path = f"{file_name}_AT_Translated{file_extension}"
        new_doc.save(new_file_path)
    
    elif file_type == 'application/pdf':  # .pdf
        pdf_reader = PdfFileReader(open(file_path, 'rb'))
        new_pdf = PdfFileWriter()
        
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text = page.extractText()
            translated_text = translate_text(text)
            
            # Create a new page with the translated text
            new_page = canvas.Canvas(new_pdf, pagesize=page.mediaBox.getWidth(), bottomup=0)
            new_page.setFont("Helvetica", 12)
            new_page.drawString(100, 700, translated_text)
            new_page.showPage()
            new_page.save()
        
        file_name, file_extension = os.path.splitext(file_path)
        new_file_path = f"{file_name}_AT_Translated{file_extension}"
        with open(new_file_path, 'wb') as out_pdf:
            new_pdf.write(out_pdf)
    
    else:  # .txt and other text-based files
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        translated_text = translate_text(text)
        file_name, file_extension = os.path.splitext(file_path)
        new_file_path = f"{file_name}_AT_Translated{file_extension}"
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)
    
    return new_file_path

def list_folder_contents(folder_id):
    """List the contents of a Google Drive folder."""
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        pageSize=10, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])
    print(f"Contents of folder {folder_id}:")
    for item in items:
        print(f"  {item['name']} ({item['mimeType']})")

input_folder_id = os.getenv('INPUT_FOLDER_ID')
output_folder_id = os.getenv('OUTPUT_FOLDER_ID')

def main():
    print("Script started...")

    print("Input folder contents:")
    list_folder_contents(input_folder_id)
    print()
    print("Output folder contents:")
    list_folder_contents(output_folder_id)
    print()
    
    processed_files = set()
    
    while True:
        files = list_files(input_folder_id)
        for file in files:
            if file['id'] not in processed_files:
                file_id = file['id']
                file_name = file['name']
                mime_type = file['mimeType']
                
                download_file(file_id, file_name)
                
                new_file_path = translate_file(file_name, mime_type)
                
                upload_file(new_file_path, output_folder_id)
                
                processed_files.add(file['id'])
        
        time.sleep(60)  # Wait for 1 minute before checking for new files again

if __name__ == '__main__':
    main()

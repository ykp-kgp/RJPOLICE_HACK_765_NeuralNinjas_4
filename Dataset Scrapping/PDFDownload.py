import os
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from urllib.parse import urljoin
from PIL import Image
import pytesseract

# Set the path to the Tesseract executable (update this with your installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

def download_pdf(pdf_url, output_directory):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Check for errors in the response

        pdf_filename = os.path.join(output_directory, os.path.basename(pdf_url))

        with open(pdf_filename, 'wb') as pdf_file:
            pdf_file.write(response.content)

        return pdf_filename
    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF from {pdf_url}: {e}")
        return None



website_url = 'https://home.rajasthan.gov.in/content/homeportal/en/acbdepartment/Fir-by-year.html'
base_url = 'https://home.rajasthan.gov.in'
output_pdf_directory = 'idownloaded_pdfs'
output_text_directory = 'ioutput_text_files'

os.makedirs(output_pdf_directory, exist_ok=True)
os.makedirs(output_text_directory, exist_ok=True)

# Fetch the HTML content of the webpage
response = requests.get(website_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find and download PDFs
for a_tag in soup.find_all('a', href=True):
    if a_tag['href'].endswith('.pdf'):
        pdf_url = urljoin(base_url, a_tag['href'])  # Join base URL and PDF URL
        pdf_path = download_pdf(pdf_url, output_pdf_directory)



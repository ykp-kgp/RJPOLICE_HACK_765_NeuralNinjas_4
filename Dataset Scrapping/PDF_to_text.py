import os
import fitz  # PyMuPDF
from PIL import Image
import io
import pytesseract
from googletrans import Translator

def extract_text_from_pdf(pdf_path, lang='hin'):
    text_list = []
    pdf_document = fitz.open(pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pix = page.get_pixmap()

        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(image, lang=lang)
        text_list.append(text)

    pdf_document.close()
    return text_list

def translate_text(text_list):
    translator = Translator()

    translated_text_list = []
    for text in text_list:
        if text is not None:
            try:
                translation = translator.translate(text, src='hi', dest='en')
                translated_text_list.append(translation.text)
            except Exception as e:
                print(f"Translation error: {e}")
                translated_text_list.append('')  # Replace with an empty string in case of an error
        else:
            translated_text_list.append('')  

    return translated_text_list



pdf_directory = r'D:\Scraping\idownloaded_pdfs'
output_directory = r'D:\Scraping\Out'

for pdf_number in range(244, 323):  # file from 1.pdf to 322.pdf
    pdf_path = os.path.join(pdf_directory, f'{pdf_number}.pdf')
    
    if not os.path.exists(pdf_path):
        print(f'Error: PDF file {pdf_path} not found. Skipping...')
        continue

    result_text_list = extract_text_from_pdf(pdf_path)

    # Translate text to English
    # translated_text_list = translate_text(result_text_list)

    # Writing to TXT file in the output directory
    txt_file_path = os.path.join(output_directory, f'output_translated_{pdf_number}.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        for page_number, text in enumerate(result_text_list, start=1):
            txt_file.write(f"Page {page_number}:\n{text}\n\n")

    print(f'Data for {pdf_path} has been translated and saved to {txt_file_path}')


# Text-242, 243 not yet converted
#importing libraries
from flask import Flask, render_template, request, flash, redirect, url_for
import pytesseract
from PIL import Image
import os
from googletrans import Translator
import json
from SER import func
from fine_tuned_llama2 import generate_query
from flask import session


app = Flask(__name__)
app.secret_key = 'super_secret_key'

def translate_text(text, src_lang='hi', dest_lang='en'):
    translator = Translator()  # Create a translator instance
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text  # Return the translated text


def nlpFunc(text):
    try:
        translated_text = translate_text(text)  
        result_dict = {"Translated Text": translated_text, "Original Text": text}
        return result_dict
    except Exception as e:
        flash("Translation error:", e)  
        return {"Example Key": text}


def ocrFunc(image_file):
    try:
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img, lang='hin')
        return nlpFunc(text)
    except Exception as e:
        flash("OCR error:", e)
        return {"Example Key": ""}


@app.route('/')
def index():
    return render_template('index.html')




@app.route('/process', methods=['POST'])
def process():
    input_option = request.form.get('inputOption')
    user_input_text = request.form.get('text', '').strip()
    user_input_image = request.files.get('image')

    if input_option == 'text' and not user_input_text:
        flash('Please provide text.')
        return redirect(url_for('index'))
    elif input_option == 'image' and not user_input_image:
        flash('Please upload an image.')
        return redirect(url_for('index'))

    if input_option == 'text':
        result = nlpFunc(user_input_text)
    else:
        image_path = "temp_image.png"
        user_input_image.save(image_path)
        result = ocrFunc(image_path)

    
    # Use the search function from your model
    dict_of_Sections = func(user_input_text)
    # model_result = generate_query(user_input_text, dict_of_Sections)
    # model_result_dict = ast.literal_eval(model_result)
    session['user_input_text'] = user_input_text
    session['dict_of_Sections'] = dict_of_Sections

    return render_template('result.html', result=dict_of_Sections)


@app.route('/model_result')
def model_result():
    # You can include any specific logic or data needed for the model result page
    user_input_text = session.get('user_input_text', '')
    dict_of_Sections = session.get('dict_of_Sections', {})
    print(generate_query(user_input_text, dict_of_Sections))
    model_result = {generate_query(user_input_text, dict_of_Sections):""}
    return render_template('model_result.html', result=model_result)


if __name__ == '__main__':
    app.run(debug=True)
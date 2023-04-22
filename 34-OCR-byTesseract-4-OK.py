# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 22:32:22 2023

@author: Pascaliensis, helped by ChatGPT 3.5 et ChatGPT 4
"""

# pip install pdfrw
# pip install pytesseract


import os
import pdfrw
import pytesseract
from PIL import Image
import io
from PARAMETERS import folder_path



def ocr_pdf(pdf_path, folder_path):
    # Create a PDF reader object
    pdf_reader = pdfrw.PdfReader(pdf_path)

    print("Processing ", pdf_path, " ... ")

    # Initialize an empty string to store the combined text
    combined_text = ""

    # Loop through each page of the PDF
    for page_num, page in enumerate(pdf_reader.pages):
        # Extract the image from the page
        img_obj = page.Resources.XObject.values()[0]
        img_data = img_obj.stream
        img_bytes = img_data.encode('latin1')  # convert the string to bytes
        img = Image.open(io.BytesIO(img_bytes))

        # Extract the text from the image using Pytesseract OCR library
        page_text = pytesseract.image_to_string(img, lang='eng')

        # Append the page text to the combined text
        combined_text += page_text

    # Create the output file name for the merged text file
    output_file = os.path.join(folder_path, f'{os.path.splitext(os.path.basename(pdf_path))[0]}.ocrtext')

    # Write the OCR output to the merged text file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(combined_text)

    print('OCR completed successfully and text file written!')

            

# loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        rawtext_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".rawtext")
        ocrtext_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".ocrtext")
        
        # check if the .rawtext file does not exist or is 1000 times smaller or less than the PDF
        # and also check that the .ocrtext file does not exist
        if (not os.path.exists(rawtext_path) or os.path.getsize(rawtext_path) < os.path.getsize(pdf_path) / 1000) and not os.path.exists(ocrtext_path):
            # start OCR process with Adobe Acrobat
            ocr_pdf(pdf_path, folder_path)


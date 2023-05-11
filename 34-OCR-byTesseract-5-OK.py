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
import shutil
from PIL import Image
import io
from PARAMETERS import folder_path

# Define the name of the subdirectory you want to create for corrupted files
subdirectory = "_corrupted"

def ocr_pdf(pdf_path, folder_path):
    # Create a PDF reader object
    pdf_reader = pdfrw.PdfReader(pdf_path)

    print("Processing ", pdf_path, " ... ")

    # Initialize an empty string to store the combined text
    combined_text = ""
    corruption_page_list = ""

    # Loop through each page of the PDF
    for page_num, page in enumerate(pdf_reader.pages):
        # Extract the image from the page
        img_obj = page.Resources.XObject.values()[0]
        img_data = img_obj.stream
        img_bytes = img_data.encode('latin1')  # convert the string to bytes
        img = None
        page_text = ""
        try: 
            img = Image.open(io.BytesIO(img_bytes))
            # Extract the text from the image using Pytesseract OCR library
            page_text = pytesseract.image_to_string(img, lang='eng')
            print(".", end='')
        except:
            print("corruption p.",page_num,"/", end='')
            corruption_page_list =  corruption_page_list + "p." + str(page_num) + "; "
            # create a subfolder _corrupted if it doesnt exist
            os.makedirs(os.path.join(folder_path, subdirectory), exist_ok=True)
            # create a text file with the file name containing all the corrupted pages
            name, extension = os.path.splitext(filename)
            newname = name + ".corrupt.txt"
            with open(os.path.join(folder_path + subdirectory, newname), "w") as f:
                f.write(corruption_page_list)
                        
        # Append the page text to the combined text
        combined_text += page_text

    # Create the output file name for the merged text file
    output_file = os.path.join(folder_path, f'{os.path.splitext(os.path.basename(pdf_path))[0]}.ocrtext')

    # Write the OCR output to the merged text file
    if not combined_text == "" : 
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(combined_text)
        print('OCR completed', end='')
        if len(corruption_page_list) > 0 :
            print(' but some pages are corrupted - corrupt file documented')
    else:
        print(pdf_path, 'failure to OCR - corrupt file documented')
        # move the .pdf file in subfolder
        shutil.move(pdf_path, os.path.join(folder_path, subdirectory, filename))
        # move the .yaml file in subfolder
        yaml_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".yaml")
        if os.path.exists(yaml_path):
            shutil.move(yaml_path, os.path.join(folder_path, subdirectory, os.path.splitext(filename)[0] + ".yaml"))
        # move the .rawtext file in subfolder
        rawtext_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".rawtext")
        if os.path.exists(rawtext_path):
            shutil.move(rawtext_path, os.path.join(folder_path, subdirectory, os.path.splitext(filename)[0] + ".rawtext"))
    
        

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


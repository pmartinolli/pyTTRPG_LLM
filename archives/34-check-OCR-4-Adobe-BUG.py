# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 22:32:22 2023

@author: martinop
"""

import os
import win32com.client
from PARAMETERS import folder_path

            

# loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        rawtext_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".rawtext")
        ocrtext_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".ocrtext")
        
        # check if the .rawtext file does not exist or is 1000 times smaller or less than the PDF
        # and also check that the .ocrtext file does not exist
        if (not os.path.exists(rawtext_path) or os.path.getsize(rawtext_path) < os.path.getsize(pdf_path) / 1000) and not os.path.exists(ocrtext_path):
            
            # open the PDF file using the Acrobat application object
            pdf_doc = win32com.client.Dispatch("AcroExch.PDDoc")
            pdf_doc.Open(pdf_path)
            print("Processing ", pdf_path, " ... ") 

            # set the OCR options
            ocr_options = win32com.client.Dispatch("AcroOCR")
            ocr_options.Language = "English"
            ocr_options.OCRResolution = 600

            # perform OCR on the PDF document
            pdf_doc.OCR(0, 0, -1, -1, 0, ocr_options)

            # save the PDF document
            pdf_doc.Save(1, pdf_path)
            pdf_doc.Close()
            print(" Done \n")
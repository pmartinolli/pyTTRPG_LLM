# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 15:30:23 2023

@author: Pascaliensis, helped by ChatGPT 3.5 et ChatGPT 4
"""

import os
import win32com.client

# Set the path to the folder containing the PDF files to OCR
pdf_folder = r'C:/00-Yragatheque/test/test' 

# Create an instance of the Adobe Acrobat application object
app = win32com.client.Dispatch("AcroExch.App")

# Loop through each PDF file in the folder
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        # Open the PDF file in Adobe Acrobat
        pdf_path = os.path.join(pdf_folder, filename)
        avdoc = win32com.client.Dispatch("AcroExch.AVDoc")
        avdoc.Open(pdf_path, "")

        # Get the PDDoc object for the PDF file
        pd_doc = avdoc.GetPDDoc()

        # Perform OCR on the PDF file
        try:
            # Perform OCR on the PDF file
            pd_doc.SetInfo("Keywords", "OCR=eng SearchableImage PDFX1a:2001 600dpi")
            pd_doc.Save(1, pdf_path)
            pd_doc.Close()
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")

        # Close the AVDoc object
        avdoc.Close(True)

# Quit Adobe Acrobat
app.Exit()


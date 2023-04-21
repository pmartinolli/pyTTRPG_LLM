# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 22:05:40 2023

@author: martinop
"""

import os
import fitz
from PARAMETERS import folder_path


# Loop through each PDF file in the directory and its subdirectories
for subdir, dirs, files in os.walk(folder_path):
    # Exclude directories named "archives"
    if "archives" in dirs:
        dirs.remove("archives")
        continue
    # Exclude directories that start with an underscore "_"
    dirs[:] = [d for d in dirs if not d.startswith('_')]
    for file in files:
        if file.endswith('.pdf'):
            # Get the full path of the PDF file
            pdf_path = os.path.join(subdir, file)

            # Check if a .rawtext file of the same name already exists
            text_path = os.path.splitext(pdf_path)[0] + '.rawtext'
            if os.path.exists(text_path):
                continue

            # Extract the raw text from the PDF file
            try:
                with fitz.open(pdf_path) as doc:
                    text = ""
                    for page in doc:
                        text += page.get_text()
            except:
                print(f"Error extracting text from {pdf_path}")
                continue

            # Save the text to a .rawtext file of the same name
            try:
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                    print(f"Success for {text_path}")
            except:
                print(f"Error writing text to {text_path}")
                continue

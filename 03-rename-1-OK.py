# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 21:26:51 2023

@author: Pascaliensis, helped by ChatGPT 3.5 et ChatGPT 4
"""

import os
import unicodedata
import re
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

            # Extract the file name without the extension
            file_name = os.path.splitext(file)[0]

            # remove parentheses and brackets (and what's inside)
#            file_name = re.sub(r'\([^)]*\)', '', file_name)
#            file_name = re.sub(r'\[[^]]*\]', '', file_name)

            # Replace multiple spaces with "-"
#            file_name = re.sub(' +', '-', file_name)
            
            # Replace non-ASCII characters with the best corresponding ASCII character
            file_name = unicodedata.normalize('NFKD', file_name).encode('ASCII', 'ignore').decode('ASCII')

            # Rename the PDF file
            new_pdf_path = os.path.join(subdir, file_name + '.pdf')
            os.rename(pdf_path, new_pdf_path)
            
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 16:38:11 2023

@author: martinop
"""

# pip install fitz
# pip install pymupdf 


import os
import yaml
import fitz
import unicodedata

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
            file_name = unicodedata.normalize('NFKD', file_name).encode('ASCII', 'ignore').decode('ASCII')


            # Get the file size in megabytes (MB) rounded up
            file_size = os.path.getsize(pdf_path) / (1024 * 1024)
            file_size = round(file_size, 2)

            # Page count with Check if the PDF file is corrupted
            try:
                doc = fitz.open(pdf_path)
                num_pages = doc.page_count
            except:
                print(f"Corrupted PDF file (pagecount): {pdf_path}")
                continue

            # Check if the YAML file already exists
            yaml_path = os.path.join(subdir, file_name + '.yaml')
            if os.path.exists(yaml_path):
                print(f"YAML file already exists: {yaml_path}")
                continue                    

            # Get the name of the directories in the path to the current file and extract game and line
            sub_dir_parts = os.path.abspath(subdir).split(os.path.sep)
            line = ''
            game = ''
            if len(sub_dir_parts) > 3:
                game = sub_dir_parts[3]
            if len(sub_dir_parts) > 4:
                line = sub_dir_parts[4]

            # Write the information to a YAML file
            yaml_data = {
                'path': pdf_path,
                'name': file_name, 
                'size': file_size, 
                'pages': num_pages,
                'game': game, 
                'line': line }
            yaml_path = os.path.join(subdir, file_name + '.yaml')
            with open(yaml_path, 'w') as file:
                yaml.dump(yaml_data, file)

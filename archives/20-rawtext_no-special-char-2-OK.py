# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:37:56 2023

@author: martinop
"""

import os
import nltk
from nltk.corpus import stopwords
import string  # Add this import statement

nltk.download('stopwords')

# Set the path to the directory containing the PDF files
folder_path = r'C:\00-Yragatheque\0-9'

# Define English and French stop words
en_stopwords = stopwords.words('english')
fr_stopwords = stopwords.words('french')

# Loop through each PDF file in the directory and its subdirectories
for subdir, dirs, files in os.walk(folder_path):
    # Exclude directories named "archives"
    if "archives" in dirs:
        dirs.remove("archives")
        continue
    # Exclude directories that start with an underscore "_"
    dirs[:] = [d for d in dirs if not d.startswith('_')]
    for file in files:
        if file.endswith('.rawtext'):
            file_path = os.path.join(subdir, file)
            with open(file_path, 'r', encoding='utf-8') as raw_file:
                raw_text = raw_file.read()
            # Remove special characters and multiple spaces
            cleaned_text = ' '.join(raw_text.split())
            # Remove punctuations
            cleaned_text = cleaned_text.translate(str.maketrans("", "", string.punctuation))
            # Remove English stop words
            cleaned_text = ' '.join([word for word in cleaned_text.split() if word.lower() not in en_stopwords])
            # Remove French stop words
            cleaned_text = ' '.join([word for word in cleaned_text.split() if word.lower() not in fr_stopwords])
            # Write the cleaned text to a new file
            cleaned_path = os.path.join(subdir, file.replace('.rawtext', '_cleaned.txt'))
            with open(cleaned_path, 'w', encoding='utf-8') as cleaned_file:
                cleaned_file.write(cleaned_text)


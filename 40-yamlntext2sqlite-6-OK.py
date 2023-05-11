# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 22:30:44 2023

@author: Pascaliensis, helped by ChatGPT 3.5 et ChatGPT 4
"""

import os
import sqlite3
import yaml
import re

from PARAMETERS import folder_path
from PARAMETERS import working_directory


# Define the fields for the database table
fields = ['id', 'path', 'name', 'size', 'pages', 'game', 'line', 'typefulltext', 'fulltext']
types = ['TEXT UNIQUE', 'TEXT', 'TEXT', 'REAL', 'INTEGER', 'TEXT', 'TEXT', 'TEXT','TEXT']

# Create a SQLite database
conn = sqlite3.connect(folder_path + working_directory + 'TTRPG_LLM.sqlite')
c = conn.cursor()

# Create the table with the defined fields
query = 'CREATE TABLE IF NOT EXISTS works ({})'.format(', '.join(['{} {}'.format(fields[i], types[i]) for i in range(len(fields))]))
c.execute(query)

# Loop through each YAML file in the directory and its subdirectories
for subdir, dirs, files in os.walk(folder_path):
    for file in files:
        # Check that the file is a YAML file
        if file.endswith('.yaml'):
            # Open the YAML file and extract the data
            with open(os.path.join(subdir, file), 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
            path = os.path.join(subdir, file)
            name = os.path.splitext(file)[0]
            size = os.path.getsize(path)
            pages = yaml_data['pages']
            game = yaml_data['game']
            line = yaml_data['line']
            # Check whether the corresponding .rawtext file exists
            raw_folder_path = os.path.join(subdir, name + '.rawtext')
            if os.path.exists(raw_folder_path):
                # Read the corresponding .rawtxt file
                with open(raw_folder_path, 'r', encoding='utf-8') as f:
                    fulltext = f.read()
                    typefulltext = "RAW"
            
            # Check whether the corresponding .ocrtext file exists
            ocr_folder_path = os.path.join(subdir, name + '.ocrtext')
            if os.path.exists(ocr_folder_path):
                # Read the corresponding .ocrtext file
                with open(ocr_folder_path, 'r', encoding='utf-8') as f:
                    ocrtext = f.read()
                # Compare sizes and set fulltext accordingly
                if os.path.getsize(ocr_folder_path) > os.path.getsize(raw_folder_path):
                    fulltext = ocrtext
                    typefulltext = "OCR"      

            # Generate a unique ID based on the name field
            id_field = re.sub(r'\W+', '', name).lower()
            while True:
                try:
                    # Insert the data into the database
                    c.execute('INSERT INTO works VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                              (id_field, path, name, size, pages, game, line, typefulltext, fulltext))
                    break
                except sqlite3.IntegrityError:
                    # If the insert fails due to a non-unique id_field value, modify the value and try again
                    id_field += "_"
            
# Commit changes and close the database connection
conn.commit()
conn.close()

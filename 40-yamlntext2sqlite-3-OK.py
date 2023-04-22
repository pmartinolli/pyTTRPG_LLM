# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 22:30:44 2023

@author: Pascaliensis, helped by ChatGPT 3.5 et ChatGPT 4
"""

import os
import sqlite3
import yaml

# Set the path to the directory containing the YAML files
folder_path = r'C:\00-Yragatheque\0-9'

# Define the fields for the database table
fields = ['path', 'name', 'size', 'pages', 'game', 'line', 'fulltext']
types = ['TEXT', 'TEXT', 'REAL', 'INTEGER', 'TEXT', 'TEXT', 'TEXT']

# Create a SQLite database
conn = sqlite3.connect('TTRPG_LLM.sqlite')
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
            txt_folder_path = os.path.join(subdir, name + '.rawtext')
            if os.path.exists(txt_folder_path):
                # Read the corresponding .rawtxt file
                with open(txt_folder_path, 'r', encoding='utf-8') as f:
                    fulltext = f.read()
            else:
                fulltext = None
            # Insert the data into the database
            c.execute('INSERT INTO works VALUES (?, ?, ?, ?, ?, ?, ?)', 
                      (path, name, size, pages, game, line, fulltext))
            
# Commit changes and close the database connection
conn.commit()
conn.close()

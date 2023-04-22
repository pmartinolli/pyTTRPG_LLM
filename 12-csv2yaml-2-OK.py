# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:47:56 2023

@author: Pascaliensis, helped by ChatGPT 3.5 et ChatGPT 4
"""

import os
import csv
import yaml
from PARAMETERS import folder_path

# Open the CSV file and loop through each line
with open(os.path.join(folder_path, 'metadata.csv'), 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader) # Get the header row
    for row in reader:
        # Get the PDF and YAML file names from the first column
        pdf_file = row[0]
        yaml_file = os.path.splitext(pdf_file)[0] + '.yaml'
        yaml_file_path = os.path.join(folder_path, yaml_file)

        # Open the YAML file and load its contents
        with open(yaml_file_path, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        # Update the YAML data with the new values from the other columns
        for i in range(1, len(row)):
            col_name = header[i] # Use the header row as variable names
            data[col_name] = row[i]

        # Save the updated YAML data to the file
        with open(yaml_file_path, 'w') as f:
            yaml.dump(data, f)

        print(f'Updated {yaml_file_path} with new data from {pdf_file}')

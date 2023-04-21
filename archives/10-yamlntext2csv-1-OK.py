# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 22:05:06 2023

@author: martinop
"""

import os
import csv
import yaml

# Set the path to the directory containing the PDF files
folder_path = r'C:\00-Yragatheque\0-9'

# Define the header row for the CSV file
csv_header = ['path', 'name', 'size', 'pages', 'game', 'line']

# Create an empty list to store the data from the YAML files
yaml_data = []

# Loop through each PDF file in the directory and its subdirectories
for subdir, dirs, files in os.walk(folder_path):
    # Exclude directories named "archives"
    if "archives" in dirs:
        dirs.remove("archives")
        continue
    # Exclude directories that start with an underscore "_"
    dirs[:] = [d for d in dirs if not d.startswith('_')]
    for file in files:
        if file.endswith('.yaml'):
            # Get the full path of the YAML file
            yaml_path = os.path.join(subdir, file)

            # Load the YAML data into a dictionary
            with open(yaml_path, 'r') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)

            # Get the path to the .text file
            text_path = os.path.join(subdir, data['name'] + '.rawtext')

            # If the .rawtext file exists, get its size in kilobytes (KB)
            if os.path.isfile(text_path):
                text_size = os.path.getsize(text_path)
                text_size = round(text_size, 2)
            else:
                text_size = 'NA'

            # Add the size of the .text file to the YAML data
            data['fulltext_size'] = text_size

            # Append the dictionary to the list of YAML data
            yaml_data.append(data)

# Create a new CSV file and write the header row
csv_path = os.path.join(folder_path, 'metadata.csv')
with open(csv_path, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=csv_header)
    writer.writeheader()

    # Loop through the list of YAML data and write each row to the CSV file
    for row in yaml_data:
        writer.writerow(row)

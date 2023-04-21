# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 09:45:28 2023

@author: martinop
"""

import csv
import os

# Define the directory to search for files
search_dir = 'C:/00-Yragatheque'

# Define the function to search for files
def find_file(file_path):
    filename = os.path.basename(file_path)
    for root, dirs, files in os.walk(search_dir):
        if filename in files:
            return os.path.abspath(os.path.join(root, filename))
    return ''

# Open the CSV file
with open('C:/00-Yragatheque/test/metadata.csv', 'r', encoding='utf-8', errors='ignore') as csvfile:
    # Decode the file contents to a string using the correct encoding
    file_contents = csvfile.read().encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    # Create a CSV reader object
    reader = csv.DictReader(file_contents.splitlines())
    # Create a list to hold the updated rows
    updated_rows = []
    # Iterate over each row in the file
    for row in reader:
        # Find the path of the file in the folder_search directory
        original_path = find_file(row['path'])
        # Add the original_path column to the row
        row['original_path'] = original_path
        # Add the updated row to the list
        updated_rows.append(row)

# Write the updated rows to a new CSV file
with open('C:/00-Yragatheque/test/metadata2.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames + ['original_path'])
    # Write the header row to the file
    writer.writeheader()
    # Write the updated rows to the file
    writer.writerows(updated_rows)


# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 18:57:32 2023

@author: martinop
"""

import os
import pandas as pd


# Read the CSV file into a DataFrame
df = pd.read_csv('C:/00-Yragatheque/_compilRPGrules/metadata.csv')

# Define the function that will search for the file in the folder_search directory
def search_file(row):
    filename = os.path.basename(row['path'])
    search_dir = 'C:/00-Yragatheque'
    for root, dirs, files in os.walk(search_dir):
        if filename in files:
            return os.path.join(os.path.abspath(root), filename)
    return ''

# Apply the search_file function to each row in the DataFrame to create the original_path column
df['original_path'] = df.apply(search_file, axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('C:/00-Yragatheque/test/metadata_new.csv', index=False)

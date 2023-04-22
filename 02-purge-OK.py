# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 21:47:56 2023

@author: Pascaliensis, helped by ChatGPT 3.5 et ChatGPT 4
"""

import os
from PARAMETERS import folder_path


# Loop through each file in the directory and its subdirectories
for subdir, dirs, files in os.walk(folder_path):
    # Exclude directories named "archives"
    if "archives" in dirs:
        dirs.remove("archives")
        continue
    # Exclude directories that start with an underscore "_"
    dirs[:] = [d for d in dirs if not d.startswith('_')]
    for file in files:
        file_path = os.path.join(subdir, file)
        if file.endswith(('.yaml', '.rawtext', '.ocrtext')):
            # Delete .yaml and .text files
            os.remove(file_path)


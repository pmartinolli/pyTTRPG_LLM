# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 22:14:22 2023

@author: Pascaliensis, helped by ChatGPT 3.5 et ChatGPT 4
"""

import os
import stat

from PARAMETERS import folder_path



# Define permissions (read, write and execute) for owner, group, and others
permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | \
              stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | \
              stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH

# Loop through each PDF file in the directory and its subdirectories
for subdir, dirs, files in os.walk(folder_path):
    # Exclude directories named "archives"
    if "archives" in dirs:
        dirs.remove("archives")
        continue
    # Exclude directories that start with an underscore "_"
    dirs[:] = [d for d in dirs if not d.startswith('_')]
 
    # Change the attributes of each subdirectory to make it readable and writable
    os.chmod(subdir, permissions)
    
    for file in files:
        if file.endswith('.pdf'):
            # Get the full path of the PDF file
            pdf_path = os.path.join(subdir, file)
            
            # Change the attributes of the PDF file to make it readable and writable
            os.chmod(pdf_path, permissions)

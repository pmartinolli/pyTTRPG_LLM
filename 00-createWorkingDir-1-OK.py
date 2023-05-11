# -*- coding: utf-8 -*-
"""
Created on Thu May 11 12:25:32 2023

@author: martinop
"""

import os

from PARAMETERS import folder_path

working_directory = "_working_directory"

# Create the working directory if it doesn't already exist

if not os.path.exists(os.path.join(folder_path, working_directory)):
    os.makedirs(os.path.join(folder_path, working_directory))
    
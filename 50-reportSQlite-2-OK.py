# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:44:19 2023

@author: Pascaliensis, helped by ChatGPT 3.5 et ChatGPT 4
"""


import sqlite3

from PARAMETERS import folder_path
from PARAMETERS import working_directory


# Connect to the database and get the cursor
conn = sqlite3.connect(folder_path + working_directory + 'TTRPG_LLM.sqlite')
c = conn.cursor()

# Get the total number of rows in the database
c.execute("SELECT COUNT(*) FROM works")
total_rows = c.fetchone()[0]

# Get the number of rows where fulltext is empty
c.execute("SELECT COUNT(*) FROM works WHERE fulltext = ''")
empty_fulltext = c.fetchone()[0]

# Calculate the total PDF volume in gigabytes
c.execute("SELECT SUM(Size) FROM works")
total_size_gb = c.fetchone()[0] / 1024 /16 # convert to GB 
# ATTENTION, variable bricolée à la main (contre-vérifier)

# Get the total number of pages of the PDF
c.execute("SELECT SUM(Pages) FROM works")
total_pages = c.fetchone()[0]
total_pages = f"{total_pages:,}".replace(',', ' ')

# Count the number of unique values in the 'game' field
c.execute("SELECT COUNT(DISTINCT game) FROM works")
unique_game_count = c.fetchone()[0]

# Iterate through all rows and sum up the size of the fulltext field
total_fulltext_size_bytes = 0
for row in c.execute("SELECT fulltext FROM works"):
    if row[0] is not None and row[0] != "":
        total_fulltext_size_bytes += len(row[0].encode('utf-8'))
total_fulltext_size_gb = total_fulltext_size_bytes / (1024 ** 3)

# Convert total size to gigabytes
total_fulltext_size_gb = total_fulltext_size_bytes / 1024 / 1024 / 1024


# Get the fields and types of variables
c.execute("SELECT sql FROM sqlite_master WHERE type='table';")
tables = c.fetchall()


# Print the report
print("REPORT:")
print("----------------------------")
print(f"Total rows: {total_rows}")
print(f"Rows with empty fulltext: {empty_fulltext}")
print(f"Total PDFs volume: {total_size_gb:.2f} GB")
print(f"Total pages of the PDFs: {total_pages}")
print(f"Total size of fulltext field: {total_fulltext_size_gb:.2f} GB")
print(f"Number of unique games: {unique_game_count}")
print('\n')
for table in tables:
        print("Table:", table[0].split()[2])
        print("----------------------------")
        c.execute("PRAGMA table_info(%s)" % table[0].split()[2])
        columns = c.fetchall()

        for column in columns:
            print(f"{column[1]} ({column[2]})")
        print()
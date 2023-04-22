# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:06:42 2023

@author: Pascaliensis, helped by ChatGPT 3.5 et ChatGPT 4
"""

import sqlite3

# Define the search string
search_string = "D&D"

# Connect to the database and execute the query
with sqlite3.connect('TTRPG_LLM.sqlite') as conn:
    c = conn.cursor()

    # Execute the query and fetch the results
    c.execute("SELECT name, fulltext FROM works WHERE fulltext LIKE ?", ("%" + search_string + "%",))
    results = c.fetchall()

    # Print the results
    for row in results:
        game_name = row[0]
        fulltext = row[1]
        index = fulltext.find(search_string)
        if index != -1:
            start_index = max(0, index - 50)
            end_index = min(len(fulltext), index + len(search_string) + 50)
            quotation = fulltext[start_index:end_index].replace('\n', ' ')
            print(f"Game name: {game_name}")
            print(f"Position: {index}")
            print(f"Quotation: ...{quotation}...\n")



# The connection to the database is automatically closed when exiting the 'with' statement

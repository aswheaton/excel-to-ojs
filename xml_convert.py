import os
import numpy as np
import pandas as pd

def view_headers(dataframe):
    print(dataframe[0,:])

def view_column(dataframe, column_name):
    # Get index associated with the column name:
    col = np.where(dataframe[0,:]==column_name)
    for row in range(1, dataframe.shape[0]):
        print(row, dataframe[row][col])

dataframe = np.loadtxt("database/Pachy.csv",dtype=str,delimiter="	")

# The column names are ['Authors' 'Title' 'Sec_title' 'Year_pub' 'Section' 'Volume' 'Page_start' 'Page_end' 'Abstract' 'EnteredBy' 'FileName' '']
view_headers(dataframe)

"""
Notes:
1. Papers with multiple authors have line ending semicolon, single authors do not!
2. Sec_title column has both "African Elephant and Rhino Group Newsletter" and "Pachyderm".
3. Capitalisation differs for Section column, i.e. "Rhino Notes" and "Rhino notes".
4. Volume contains entries for Vol 42, for which there are no filenames.
5. Number of rows does NOT match number of files in database/articles (extra rows)
   It appears that some files are referenced by multiple rows, for short articles.
6. Not clear wwhat purpose the final column serves.
"""

view_column(dataframe, "")

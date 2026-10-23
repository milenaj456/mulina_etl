import openpyxl 
import sqlite3 as sql
import re 

# connect to the DB
conn = sql.connect('mulina.db')
c = conn.cursor()

# specify the file and worksheet. Worksheet layout: column A has codes, column B has corresponding
# colour names. Code values can be e.g. Ecru, B5200, 1 
file = './files/dmc_colors.xlsx'
sheet = 'Print - By Number'
data = openpyxl.load_workbook(file)

ws1=data[sheet]

# get the data. Check if the value is not empty, it is not a header row or if in code column
# there is no other data (longer than 10 chars). Sometimes they have * or ^ that I want to remove
rows = []
for code, name in ws1.iter_rows(min_col=1, max_col=2, values_only=True):
    if code is None or name is None:
        continue
    if code == "Number" or name == "Name" or (type(code) == str and len(code) > 10):
        continue
    rows.append((str(code).upper(), name))

# insert the data into the DB if it is not there already (to avoid duplicates/errors)
for code, colour in rows:
    c.execute("insert or ignore into mulina (producer, code, colour) values (?,?,?)", ('DMC', code.rstrip("*^"), colour)
)
conn.commit()
c.close()
conn.close()
import requests
from bs4 import BeautifulSoup
import sqlite3 as sql
import pandas as pd
import re

#connect to the DB
conn = sql.connect('mulina.db')
c = conn.cursor()

#EXTRACT data from the website and parse
url = 'https://anchorsite.com/example'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#search for tags with specified parameters, TRANSFORM the data
div_tag = soup.find_all('div', attrs = {'style':True, 'id' : True, 'data-swatch-group': True, 'class':True})

for i, tag in enumerate(div_tag):
    #get the clean data for code (no leading zeros) and colour name, then LOAD into the DB
    code, colour = div_tag[i]['id'].lstrip('0'), div_tag[i]['data-swatch-group']
    if not re.fullmatch(r"\d{1,4}[A-Za-z]?", code): continue
    conn.execute("INSERT OR IGNORE INTO MULINA (PRODUCER, CODE, COLOUR) VALUES (?,?,?) ", 
                 ('ANCHOR', code.upper(), colour)  
                 )
conn.commit()    

#disconnect and print data 
c.close()
conn.close()

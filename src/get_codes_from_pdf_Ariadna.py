import re
import sqlite3 as sql
import pdfplumber

pdf_path = "./files/mulina_ulotka.pdf"

# get codes from PDF. Codes are 4-digits, sometimes with a trailing letter
codes = [] 
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages[1:3]:
        text = page.extract_text()
        if text:
            found = re.findall(r"\b[1-9]\d{3}[a-zA-Z]?\b", text)
            codes.extend(found)

conn=sql.connect('mulina.db')
c=conn.cursor()

for code in codes:
    c.execute("INSERT OR IGNORE INTO MULINA (PRODUCER, CODE) VALUES ('ARIADNA',  ?)", (code.upper(),))
conn.commit()
c.close()
conn.close()
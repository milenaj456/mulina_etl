import sqlite3 as sql

conn=sql.connect('mulina.db')
c=conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS MULINA(
PRODUCER TEXT,
CODE TEXT,
COLOUR TEXT,
IN_STOCK TEXT,
TO_BUY TEXT,
IN_STOCK_COUNT INT,
TO_BUY_COUNT INT,
PRIMARY KEY (PRODUCER,CODE)
)
'''
)

conn.close()
import snowflake.connector
import sqlite3 as sql
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
# connect to my account
conn = snowflake.connector.connect(
    user=os.environ["user"],
    password=os.environ["password"],
    account=os.environ["account"],
    warehouse=os.environ["warehouse"],
    database=os.environ["database"],
    schema=os.environ["schema"]
)

# create a table if it does not exist already
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

c.close()
conn.close()
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

# connect to my local DB 
conn_local=sql.connect('mulina.db')
c_local=conn_local.cursor()
df = pd.read_sql("SELECT * FROM MULINA", conn_local)
df.to_parquet("mulina.parquet", engine="pyarrow", compression="snappy", index=False)

# connect to snowflake DB, create staging for my DB file
c = conn.cursor()

c.execute("CREATE STAGE IF NOT EXISTS mulina_stage; ")
c.execute("REMOVE @mulina_stage") # remove the content
c.execute("PUT file:///filepath/mulina_projekt/mulina.parquet @mulina_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;")
c.execute("TRUNCATE TABLE MULINA") 
# copy data from staging to snowflake DB
c.execute("""
    COPY INTO mulina
    FROM @mulina_stage
    FILE_FORMAT = (TYPE = PARQUET)
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
""")
# check the data got inserted
print(c.fetchone())

c.close()
conn.close()
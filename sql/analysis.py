import sqlite3 as sql
import pandas as pd

conn = sql.connect('mulina.db')
c = conn.cursor()

df_num_of_colours = pd.read_sql('''select producer, count(*) as colours from mulina group by producer  
order by colours desc''', conn)

df_codes_for_same_colour = pd.read_sql('''SELECT PRODUCER, UPPER(TRIM(COLOUR)) AS colour, COUNT(*) AS codes,
       GROUP_CONCAT(CODE, ', ') AS code_list
FROM MULINA
WHERE COLOUR IS NOT NULL
GROUP BY 1, 2
HAVING COUNT(*) > 1
ORDER BY codes DESC''', conn)

df_dmc_number_gaps = pd.read_sql('''WITH nums AS (
    SELECT DISTINCT CAST(CODE AS INTEGER) AS n
    FROM MULINA
    WHERE PRODUCER = 'DMC' AND CODE <> '' 
)
SELECT n AS last_code_before_gap, next_n AS next_code, next_n - n - 1 AS missing
FROM (SELECT n, LEAD(n) OVER (ORDER BY n) AS next_n FROM nums)
WHERE next_n - n > 1
ORDER BY n''', conn)

print(df_num_of_colours)
#print(df_codes_for_same_colour)
print(df_dmc_number_gaps)
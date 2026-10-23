import os
import sqlite3
from contextlib import closing

import pytest
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif("user" not in os.environ, reason="no Snowflake credentials"),
]


@pytest.fixture(scope="module")
def sf():
    conn = snowflake.connector.connect(
        user=os.environ["user"],
        password=os.environ["password"],
        account=os.environ["account"],
        warehouse=os.environ["warehouse"],
        database=os.environ["database"],
        schema=os.environ["schema"],
    )
    yield conn.cursor()
    conn.close()

@pytest.fixture(scope="module")
def local_rows():
    with closing(sqlite3.connect("mulina.db")) as conn:
        return set(conn.execute("SELECT PRODUCER, CODE, COLOUR FROM MULINA"))

# check if number of rows is the same
def test_row_counts_match(sf, local_rows):
    sf.execute("SELECT COUNT(*) FROM MULINA")
    assert sf.fetchone()[0] == len(local_rows)

def test_content_matches(sf, local_rows):
    sf.execute("SELECT PRODUCER, CODE, COLOUR FROM MULINA")
    remote_rows = set(sf.fetchall())
    assert local_rows - remote_rows == set(), "in SQLite but missing in Snowflake"
    assert remote_rows - local_rows == set(), "in Snowflake but not in SQLite"


def test_no_duplicates(sf):
    sf.execute("""
        SELECT PRODUCER, CODE FROM MULINA
        GROUP BY PRODUCER, CODE HAVING COUNT(*) > 1
    """)
    assert sf.fetchall() == []

def test_no_bad_codes(sf):
    sf.execute("""
        SELECT COUNT(*) FROM MULINA
        WHERE CODE IS NULL OR TRIM(CODE) = ''
           OR CODE <> UPPER(CODE)
           OR REGEXP_LIKE(CODE, '.*[*^]$')
    """)
    assert sf.fetchone()[0] == 0
import sqlite3
import pytest
import os
pytestmark = pytest.mark.skipif(not os.path.exists("mulina.db"), reason="no mulina.db")

def test_no_duplicates():
    conn = sqlite3.connect("mulina.db")
    duplicates = conn.execute(
        "SELECT PRODUCER, CODE FROM MULINA GROUP BY PRODUCER, CODE HAVING COUNT(*) > 1"
    ).fetchall()
    conn.close()
    assert duplicates == []

def test_no_trailing_star_or_caret():
    conn = sqlite3.connect("mulina.db")
    bad = conn.execute(
        "SELECT PRODUCER, CODE FROM MULINA WHERE CODE LIKE '%*' OR CODE LIKE '%^'"
    ).fetchall()
    conn.close()
    assert bad == []

#check if all producers have entries in the DB
@pytest.mark.parametrize("producer", ["DMC", "ANCHOR", "ARIADNA"])
def test_producer_has_rows(producer):
    conn = sqlite3.connect("mulina.db")
    count = conn.execute(
        "SELECT COUNT(*) FROM MULINA WHERE PRODUCER = ?", (producer,)
    ).fetchone()[0]
    conn.close()
    assert count > 0

def test_no_empty_codes():
    conn = sqlite3.connect("mulina.db")
    bad = conn.execute(
        "SELECT COUNT(*) FROM MULINA WHERE CODE IS NULL OR TRIM(CODE) = ''"
    ).fetchone()[0]
    conn.close()
    assert bad == 0

def test_codes_are_uppercase():
    conn = sqlite3.connect("mulina.db")
    bad = conn.execute(
        "SELECT PRODUCER, CODE FROM MULINA WHERE CODE <> UPPER(CODE)"
    ).fetchall()
    conn.close()
    assert bad == []
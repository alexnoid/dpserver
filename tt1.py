import sqlite3
import contextlib
import string


def execute_statement(statement):
    with contextlib.closing(sqlite3.connect('DB/data.db')) as conn: # auto-closes
        with conn: # auto-commits
            with contextlib.closing(conn.cursor()) as cursor: # auto-closes
                cursor.execute(statement)
                values = cursor.fetchall()
                return values

log = "оааоао"
pas = "ytbptcnty"
#string.Template('hanning${num}.pdf').substitute(locals()))
query = f"select * from users"
print(execute_statement(query))
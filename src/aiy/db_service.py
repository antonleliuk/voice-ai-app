import sqlite3

DB_NAME = "file:data/voice_app.db"

def execute(sql):
    connection = sqlite3.connect(DB_NAME)
    with connection:
        connection.execute(sql)
    connection.close()

def select(sql, row_factory):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = row_factory
    with connection:
        cursor = connection.execute(sql)
        row = cursor.fetchone()
    connection.close()
    return row

def save(sql, data):
    connection = sqlite3.connect(DB_NAME)
    with connection:
        connection.execute(sql, data)
    connection.close()

def delete(sql, id):
    connection = sqlite3.connect(DB_NAME)
    with connection:
        connection.execute(sql, id)
    connection.close()
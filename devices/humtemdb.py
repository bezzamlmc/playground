# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 18:07:51 2021

@author: laura
"""

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
def setup_table():
    database = r"C:\work\db\humtemp.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS samples (
                                        id integer PRIMARY KEY,
                                        timestamp text NOT NULL,
                                        humidity integer,NOT NULL,
                                        temperature integer, NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")
    return conn
        
def insert_record(conn,id, timestamp, humidity, temperature):
    """ Insert an id, timestamp, humidity, temperature record"""
    
    sql = ''' INSERT INTO samples(id,timestamp,humidity, temperature)
              VALUES(?, ?, ?,?) '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def total_samples(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM samples")
    results = cur.fetchall()
    return len(results)

def query_samples(conn, lastn):
    """Retrieve the last n samples"""
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM samples ORDER BY id DESC LIMIT ? ", (lastn))

    rows = cur.fetchall()
    
    return rows


if __name__ == '__main__':
    setup_table()

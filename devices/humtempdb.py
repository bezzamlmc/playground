# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 18:07:51 2021

@author: laura
"""

import sqlite3
from sqlite3 import Error

class HumTempDB:
    def __init__(self,database):
        self.database = database
        self.conn = None
        self.lastId = 0
        self.setup_table()
        
    def setup_table(self):
        sql_create_samples_table = """CREATE TABLE IF NOT EXISTS samples (
                                        id integer PRIMARY KEY,
                                        timestamp text,
                                        humidity integer,
                                        temperature integer); """
        # create a database connection
        self.conn = self.create_connection()
        # create tables
        if self.conn is not None:
            # create samples table
            self.create_table(sql_create_samples_table)
            self.lastId = self.total_samples()
        else:
            print("Error! cannot create the database connection.")
        
    def create_connection(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.database)
            print(sqlite3.version)
        except Error as e:
            print(e)
        return conn

    def create_table(self,create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
        
        
    def insert_record(self,timestamp, humidity, temperature):
        """ Insert an id, timestamp, humidity, temperature record"""
        self.lastId  = self.lastId + 1

        sql = """INSERT INTO samples(id,timestamp,humidity,temperature) 
                VALUES(?, ?, ?, ?) """
        cur = self.conn.cursor()
        cur.execute(sql,(self.lastId,timestamp,humidity,temperature))
        self.conn.commit()
        return cur.lastrowid

    def total_samples(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM samples")
        results = cur.fetchall()
        return len(results)

    def query_samples(self,lastn):
        """Retrieve the last n samples"""
        cur = self.conn.cursor() 
        idmin = self.lastId - lastn
        cur.execute("SELECT * FROM samples WHERE id > ? ", (idmin,))
        rows = cur.fetchall()    
        return rows
    
    def stats_samples(self,lastn):
        """Retrieve stats for the last n samples"""
        cur = self.conn.cursor() 
        sql = \
        """SELECT avg(humidity),min(humidity), max(humidity), avg(temperature), 
        min(temperature), max(temperature) 
        FROM samples 
        WHERE id > ? """
        findHAvg = cur.execute("SELECT avg(humidity) FROM samples")
        havg = findHAvg.fetchone()[0]
        print(havg)
        
        idmin = self.lastId - lastn
        findAll = cur.execute(sql,(idmin,))
        all = findAll.fetchone()
        print(all)
        
        return all
    
    def shutdown(self):
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    database = r"C:\Users\laura\work\db\humtemp.db"
    db = HumTempDB(database)

import pytest
import os
import sqlite3

os.remove("test.db")
os.environ['DB_PATH'] = "test.db"

def create_database():
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    query = """CREATE TABLE IF NOT EXISTS sports (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sport_name VARCHAR(100) NOT NULL UNIQUE, slug VARCHAR(100) NOT NULL, active BOOLEAN NOT NULL)"""
    cursor.execute(query)
    query = """CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, event_name VARCHAR(100) NOT NULL UNIQUE, slug VARCHAR(100) NOT NULL, active BOOLEAN NOT NULL, type VARCHAR(20) NOT NULL, sport_name VARCHAR(100) NOT NULL, status VARCHAR(20) NOT NULL, scheduled_start DATETIME NOT NULL, actual_start DATETIME, CONSTRAINT fk_sports FOREIGN KEY (sport_name) REFERENCES sports(name))"""
    cursor.execute(query)
    query = """CREATE TABLE IF NOT EXISTS selections (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, selection_name VARCHAR(100) NOT NULL UNIQUE, event_name VARCHAR(100) NOT NULL, price DECIMAL NOT NULL,active BOOLEAN not NULL, outcome VARCHAR(20), CONSTRAINT fk_events FOREIGN KEY (event_name) REFERENCES events(event_name))"""
    cursor.execute(query)   
    connection.close()

create_database()

def execute_query(query):
    connection = sqlite3.connect("test.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    results = cursor.execute(query).fetchall()
    return [dict(result) for result in results]

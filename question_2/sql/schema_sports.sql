CREATE TABLE IF NOT EXISTS sports (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sport_name VARCHAR(100) NOT NULL UNIQUE, slug VARCHAR(100) NOT NULL, active BOOLEAN NOT NULL)

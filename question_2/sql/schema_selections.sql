CREATE TABLE IF NOT EXISTS selections (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                                        selection_name VARCHAR(100) NOT NULL UNIQUE, 
                                        event_name VARCHAR(100) NOT NULL, 
                                        price DECIMAL NOT NULL,
                                        active BOOLEAN not NULL, 
                                        outcome VARCHAR(20),
                                        CONSTRAINT fk_events
                                        FOREIGN KEY (event_name)
                                        REFERENCES events(event_name))
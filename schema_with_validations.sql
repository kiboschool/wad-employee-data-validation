CREATE TABLE IF NOT EXISTS new_employees (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL, 
  email TEXT NOT NULL UNIQUE,
  salary INTEGER
);
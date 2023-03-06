CREATE TABLE IF NOT EXISTS users(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   _username TEXT,
   _password TEXT,
)
CREATE TABLE IF NOT EXISTS tasks{
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    _title TEXT,
    _description TEXT,
    _due TIME,
    _complete BOOLEAN,
    _type TEXT
}
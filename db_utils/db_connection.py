import sqlite3

# Cada vez que abras una conexión, las claves foráneas se activan automáticamente
def get_db_connection(db_path):
  conn = sqlite3.connect(db_path)
  conn.execute("PRAGMA foreign_keys = ON;")  # Activar las claves foráneas
  return conn

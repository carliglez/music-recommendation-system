from db_utils import db_connection

def delete_rows(cursor):  
  # Deactivate foreign keys
  cursor.execute("PRAGMA foreign_keys = OFF;")
  
  # List of tables to be cleaned
  tables = [
    "ARTIST", "CONTAIN", "FAVORITE_ARTIST", "FAVORITE_GENRE", "GENRE",
    "HAVE", "LISTENS", "MOOD", "PLAYLIST", "RECOMMENDATION",
    "SING", "SONG", "USER"
  ]
  
  # Delete data from each table
  for table in tables:
    cursor.execute(f"DELETE FROM {table};")
  
  # # Reset AUTOINCREMENT (NOT USED)
  # cursor.execute("DELETE FROM sqlite_sequence;")
  
  # Reactivate foreign keys
  cursor.execute("PRAGMA foreign_keys = ON;")

def main(vacuum=False):
  with db_connection.get_db_connection("./database/music.db") as conn:
    cursor = conn.cursor()
    delete_rows(cursor)
    # Optimize the database
    conn.commit()  # <- commit before VACUUM
    
    # VACUUM frees the disk space left after deleting data. Useful if you have deleted a lot of records
    if vacuum:
      print("Running VACUUM to optimize the database...")
      cursor.execute("VACUUM;")  # <- outside the transaction

    #conn.close()
  
  print("All rows have been successfully deleted.")

if __name__ == "__main__":
  main(vacuum=True)

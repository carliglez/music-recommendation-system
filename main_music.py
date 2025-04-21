import sqlite3
import csv
from db_utils import db_connection

# Function to create the database tables
def create_tables(cursor: sqlite3.Cursor, schema_path: str):
  # Creates the tables in the database using an external file with the SQL schema
  try:
    with open(schema_path, "r") as f:
      schema = f.read()
    cursor.executescript(schema)
    print("Tables successfully created or verified.")
  except (sqlite3.Error, FileNotFoundError) as e:
    print(f"Error creating tables: {e}")

# Function to insert data into the tables from a CSV file
def insert_data(cursor: sqlite3.Cursor, csv_filename: str):
  file_path = f'./resources/{csv_filename}'
  
  try:
    with open(file_path, 'r', encoding='utf-8') as file:
      contents = csv.reader(file)
      next(contents)  # Skip header row
      
      if csv_filename == "artist.csv":
        data = [(int(row[0]), row[1], row[2], int(row[3])) for row in contents]
        insert_query = "INSERT INTO ARTIST (id, name, country, followers) VALUES (?, ?, ?, ?)"
        count_query = "SELECT COUNT(*) FROM ARTIST"
      elif csv_filename == "sing.csv":
        data = [(int(row[0]), int(row[1])) for row in contents]
        insert_query = "INSERT INTO SING (song_id, artist_id) VALUES (?, ?)"
        count_query = "SELECT COUNT(*) FROM SING"
      elif csv_filename == "song.csv":
        data = [(int(row[0]), row[1], row[2], int(row[3]), int(row[4]), int(row[5])) for row in contents]
        insert_query = "INSERT INTO SONG (id, title, genre, duration, streams, year) VALUES (?, ?, ?, ?, ?, ?)"
        count_query = "SELECT COUNT(*) FROM SONG"
      elif csv_filename == "genre.csv":
        data = [(int(row[0]), row[1]) for row in contents]
        insert_query = "INSERT INTO GENRE (artist_id, genre) VALUES (?, ?)"
        count_query = "SELECT COUNT(*) FROM GENRE"
      else:
        print("Error: Unrecognized filename.")
        return
      
      cursor.executemany(insert_query, data)
      cursor.execute(count_query)
      count_result = cursor.fetchone()[0]
      print(f"Number of rows in {csv_filename.split('.')[0]}: {count_result}")
          
  except FileNotFoundError:
    print("Error: The specified CSV file was not found.")
  except ValueError as e:
    print(f"Data conversion error: {e}")
  except sqlite3.Error as e:
    print(f"Database error: {e}")

# Main function
def main():
  with db_connection.get_db_connection("./database/music.db") as conn:
    cursor = conn.cursor()

    # # Create tables using the schema from the SQL file
    # create_tables(cursor, "./sql_code/create_tables.sql")
    # conn.commit()
    
    # It's important to note that 'sing.csv' depends on 'artist.csv' and 'song.csv'. It should be loaded last
    csv_filename = input("Enter the name of the CSV file (artist.csv, sing.csv, song.csv o genre.csv): ")
    insert_data(cursor, csv_filename)
    conn.commit()

    #conn.close()
    
if __name__ == "__main__":
  main()

from db_utils import db_connection
from datetime import datetime

# Dictionary of genres associated with moods
mood_map = {
  "Pop": "Happy",
  "Indie Pop": "Melancholic",
  "K-Pop": "Energetic",
  "Rock": "Energetic",
  "Afrobeats": "Danceable",
  "Country": "Relaxed",
  "Jazz": "Relaxed",
  "R&B": "Romantic",
  "Blues": "Melancholic",
  "Dance": "Festive",
  "Hip-Hop": "Motivated",
  "Electronic": "Excited",
  "Reggaeton": "Lively",
  "Classical": "Calm"
}

# Function that retrieves the user's most listened-to music genre via a query
def get_most_listened_genre(cursor, user_id):
    cursor.execute('''
        SELECT SONG.genre, SUM(LISTENS.streams) as total_streams
        FROM LISTENS
        JOIN SONG ON LISTENS.song_id = SONG.id
        WHERE LISTENS.user_id = ?
        GROUP BY SONG.genre
        ORDER BY total_streams DESC
        LIMIT 1;
    ''', (user_id,))
    return cursor.fetchone()

# Function to assign a mood to each user based on their most listened-to genre
def assign_user_mood(conn, cursor):
  # Get today's date
  today = datetime.today().strftime('%Y-%m-%d')
  
  # Get all users
  cursor.execute("SELECT id FROM USER;")
  users = cursor.fetchall()
  
  for (user_id,) in users:  # The comma is necessary because users is a list of tuples with only one element
    result = get_most_listened_genre(cursor, user_id)
    
    if result:  # Avoid errors if there are no listening records (truthy)
      genre, _ = result  # _ is a convention in Python that indicates that we do not need that value
      mood = mood_map.get(genre, "Unfolding")  # If the gender is not in the dictionary, assign "Unfolding"
      
      # Insert mood in the MOOD table
      cursor.execute('''
        INSERT INTO MOOD (user_id, set_date, state_of_mind)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, set_date) DO UPDATE SET state_of_mind = excluded.state_of_mind;
      ''', (user_id, today, mood))
  
  conn.commit()

# Function to assign the user's most listened-to genre
def assign_favorite_genre(conn, cursor):
  # Get all users
  cursor.execute("SELECT id FROM USER;")
  users = cursor.fetchall()

  for (user_id,) in users:
    result = get_most_listened_genre(cursor, user_id)
    
    if result:  # Avoid errors if there are no listening records (truthy)
      genre, _ = result

      cursor.execute('''
        INSERT INTO FAVORITE_GENRE (user_id, genre)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET genre = excluded.genre;
      ''', (user_id, genre))
  
  conn.commit()

# Function to assign the user's most listened-to artist
def assign_favorite_artist(conn, cursor):
  # Get all users
  cursor.execute("SELECT id FROM USER;")
  users = cursor.fetchall()

  for (user_id,) in users:
    # Get the most listened-to artist
    cursor.execute('''
      SELECT SING.artist_id, SUM(LISTENS.streams) as total_streams
      FROM LISTENS
      JOIN SING ON LISTENS.song_id = SING.song_id
      WHERE LISTENS.user_id = ?
      GROUP BY SING.artist_id
      ORDER BY total_streams DESC
      LIMIT 1;
    ''', (user_id,))
    result = cursor.fetchone()

    if result:  # Avoid errors if there are no listening records (truthy)
      artist_id, _ = result

      cursor.execute('''
        INSERT INTO FAVORITE_ARTIST (user_id, artist_id)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET artist_id = excluded.artist_id;
      ''', (user_id, artist_id))
  
  conn.commit()

# Main function
def main():
  with db_connection.get_db_connection("./database/music.db") as conn:
    cursor = conn.cursor()
    assign_user_mood(conn, cursor)
    assign_favorite_genre(conn, cursor)
    assign_favorite_artist(conn, cursor)

    #conn.close()
  
  print("Custom data successfully generated.")

if __name__ == "__main__":
  main()

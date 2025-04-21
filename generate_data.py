import random
from db_utils import db_connection
from faker import Faker

fake = Faker()

# Function to create users randomly
def create_users(conn, cursor, num_users=10):
  users = []
  for i in range(num_users):
    # Each 'id' is generated automatically in SQLite because it is defined as INTEGER PRIMARY KEY
    name = fake.first_name()
    email = fake.email()
    cursor.execute("INSERT INTO USER (name, email) VALUES (?, ?)", (name, email))
    users.append(cursor.lastrowid)
  conn.commit()
  return users

# Function to create playlists randomly
def create_playlists(conn, cursor, users):
  playlists = []
  for user_id in users:
    name = fake.word() + " playlist"
    description = fake.sentence()
    cursor.execute("INSERT INTO PLAYLIST (name, description, user_id) VALUES (?, ?, ?)", (name, description, user_id))
    playlists.append(cursor.lastrowid)  # We save only the 'id' of the playlist
  conn.commit()
  return playlists

# Function to assign songs to playlists randomly
def assign_songs_to_playlists(conn, cursor, playlists):
  cursor.execute("SELECT id FROM SONG")
  song_ids = [row[0] for row in cursor.fetchall()]
  
  for playlist_id in playlists:
    songs = random.sample(song_ids, min(len(song_ids), random.randint(1, 5)))
      # random.randint(1, 5): generates a random number between 1 and 5.
      # min(len(song_ids), ...): avoids selecting more songs than are available.
      # Assigns between 1 and 5 different songs to each playlist (or less if there are fewer songs in total).
    for song_id in songs:
      cursor.execute("INSERT INTO CONTAIN (playlist_id, song_id) VALUES (?, ?)", (playlist_id, song_id))
  conn.commit()

# Function to assign song plays to users randomly
def generate_listens(conn, cursor, users):
  cursor.execute("SELECT id FROM SONG")
  song_ids = [row[0] for row in cursor.fetchall()]

  for user_id in users:
    num_listens = random.randint(1, min(16, len(song_ids)))  # Never select more songs than exist
    listened_songs = random.sample(song_ids, num_listens)  # Avoid repetition
    for song_id in listened_songs:
      streams = random.randint(1, 40)
      cursor.execute("INSERT INTO LISTENS (user_id, song_id, streams) VALUES (?, ?, ?)", (user_id, song_id, streams))
  conn.commit()

# Function to assign playlists to users randomly
def assign_playlists_to_users(conn, cursor, users, playlists):
  for playlist_id in playlists:
    assigned_users = random.sample(users, random.randint(1, min(3, len(users))))
      # min(3, len(users)): limits the maximum to 3 users, but if there are less than 3 users in total, it takes that number instead.
      # random.randint(1, ...): randomly chooses how many users are selected for that playlist.
      # Each playlist becomes collaborative on a random basis, with between 1 and 3 users assigned (or less if there are less than 3 users).
    for user_id in assigned_users:
      cursor.execute("INSERT INTO HAVE (user_id, playlist_id) VALUES (?, ?)", (user_id, playlist_id))
  conn.commit()

# Main function
def main():
  with db_connection.get_db_connection("./database/music.db") as conn:
    cursor = conn.cursor()
    
    users = create_users(conn, cursor, num_users=100)
    playlists = create_playlists(conn, cursor, users)
    assign_songs_to_playlists(conn, cursor, playlists)
    generate_listens(conn, cursor, users)
    assign_playlists_to_users(conn, cursor, users, playlists)
    
    #conn.close()

  print("Data successfully generated.")

if __name__ == "__main__":
  main()

import numpy as np
from db_utils import db_connection
from sklearn.neighbors import NearestNeighbors

# Function for obtaining the user-song interaction matrix
def get_user_song_matrix(cursor):
  cursor.execute("SELECT id FROM USER;")
  users = [row[0] for row in cursor.fetchall()]

  cursor.execute("SELECT id FROM SONG;")
  songs = [row[0] for row in cursor.fetchall()]

  # Create dictionaries from index to ID
  user_index = {user_id: i for i, user_id in enumerate(users)}
  song_index = {song_id: i for i, song_id in enumerate(songs)}

  # Interactions matrix (users x songs)
  interaction_matrix = np.zeros((len(users), len(songs)))

  cursor.execute("SELECT user_id, song_id, streams FROM LISTENS;")
  for user_id, song_id, streams in cursor.fetchall():
    interaction_matrix[user_index[user_id], song_index[song_id]] = streams

  return interaction_matrix, users, songs, user_index, song_index

# Function to assign recommendations to users using KNN
def assign_recommendations(conn, cursor):
  interaction_matrix, users, songs, user_index, song_index = get_user_song_matrix(cursor)
    # 'song_index' is a dictionary from ID to index and is not currently used.

  # Apply KNN to find similar users
  model = NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='brute')
  model.fit(interaction_matrix)

  for user_id in users:
    user_vec = interaction_matrix[user_index[user_id]].reshape(1, -1)
    distances, neighbors = model.kneighbors(user_vec)
      # 'distances' could be used to weight recommendations (closer = more weight).

    # Get the songs most listened to by neighboring users
    recommended_songs = {}
    for neighbor_idx in neighbors[0]:  # 'neighbors[0]' contains the indices (rows) of the users most similar to the current user
      for song_idx, listens in enumerate(interaction_matrix[neighbor_idx]):
        if listens > 0:
          recommended_songs[songs[song_idx]] = recommended_songs.get(songs[song_idx], 0) + listens

    # Sort by most played songs by the neighbors
    recommended_songs = sorted(recommended_songs.keys(), key=lambda s: -recommended_songs[s])
      # A list of the keys from the dictionary 'recommended_songs' is obtained.
      # The keys are sorted by their values in descending order (-), rather than the default ascending order of sorted().

    # Insert the recommendations into the RECOMMENDATION table (maximum 5 per user)
    cursor.execute("DELETE FROM RECOMMENDATION WHERE user_id = ?;", (user_id,))
    for song_id in recommended_songs[:1]:
      cursor.execute('''
        INSERT INTO RECOMMENDATION (user_id, song_id, date)
        VALUES (?, ?, DATE('now'));
      ''', (user_id, song_id))

  conn.commit()
  cursor.close()

# Main function
def main():
  with db_connection.get_db_connection("./database/music.db") as conn:
    cursor = conn.cursor()
    assign_recommendations(conn, cursor)

    #conn.close()
  
  print("Recommendations successfully generated.")

if __name__ == "__main__":
  main()

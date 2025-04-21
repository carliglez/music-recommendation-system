# 🎵 Music Recommendation System — Python & SQL Project

This repository contains the code and resources for a music recommendation system built as a personal project to practice both **Python programming** and **SQL database design**. The project simulates the entire lifecycle of a data-driven application: from **data cleaning and database design** to **automated data loading** and the use of **machine learning algorithms** for music recommendations.

---

## 💡 Project Overview

The project originated from the idea of reinforcing programming and database management skills by designing a realistic scenario:  
A music app that recommends songs to users based on their listening history using **K-Nearest Neighbors (KNN)**.

The development started with:

- An **initial study and design** of the database through an Entity-Relationship (ER) model.
- Refinement of the ER model into a **relational schema**, including attributes, relationships, and integrity constraints.
- Loading real-world music data into the database from a public dataset.

---

## 📁 Dataset Information

The primary data source for this project was the [Billboard Hits Songs Dataset](https://www.kaggle.com/datasets/dem0nking/billboard-hits-songs-dataset?resource=download) from Kaggle.

All raw datasets were cleaned, structured, and analyzed in a set of explanatory Jupyter notebooks (using Google Colab):

- `music_main_datasets.ipynb`  
- `get_unique_genres.ipynb`  
- `genre_dataset.ipynb`  
- `clean_artists_country.ipynb`  

Each notebook includes real code snippets and detailed explanations about the cleaning, preparation, and transformation processes.

The cleaned data was then exported to the following `.csv` files for direct database loading:

- `artist.csv`
- `sing.csv`
- `song.csv`
- `genre.csv`

---

## ⚙️ Scripts Overview

The project is modular and organized through standalone Python scripts that can be executed sequentially:

| Script Name               | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `main_music.py`           | Creates the database schema and loads cleaned datasets into the database.   |
| `generate_data.py`        | Generates random synthetic data to enrich the database.                    |
| `custom_tables.py`        | Calculates the favorite artist, favorite genre, and mood for each user.     |
| `knn_recommendation.py`   | Uses the KNN algorithm to recommend 5 songs to each user based on user similarity. Future versions will extend and improve this logic. |
| `db_delete_rows.py`       | Utility script to delete all data from the database tables (useful for testing). |

---

## 🧠 Recommendation System

The core recommendation algorithm uses:

- **K-Nearest Neighbors (KNN)** from `scikit-learn`.
- A **cosine similarity metric** to identify the 5 most similar users.
- Recommendations are generated based on the listening habits of these similar users.

The system is designed to evolve, and future improvements (such as item-based collaborative filtering, weighted scores, avoiding recommending songs that have already been listened, or hybrid models) are planned for upcoming versions.

---

## 🗃️ Tech Stack

- **Python 3.12.6**  
- **SQLite3** as the database engine  
- **SQL** for data modeling and querying  
- **Jupyter Notebooks** for data exploration and cleaning  
- **Scikit-learn** for machine learning (KNN algorithm)  

The project was developed and executed within a Python virtual environment (`.venv`).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

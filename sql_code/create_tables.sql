CREATE TABLE IF NOT EXISTS `USER` (
  `id` integer PRIMARY KEY,
  `name` varchar(32),
  `email` varchar(320)
);

CREATE TABLE IF NOT EXISTS `PLAYLIST` (
  `id` integer PRIMARY KEY,
  `name` varchar(50),
  `description` varchar(100),
  `user_id` integer,
  FOREIGN KEY (`user_id`) REFERENCES `USER` (`id`) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS `HAVE` (
  `user_id` integer,
  `playlist_id` integer,
  PRIMARY KEY (`user_id`, `playlist_id`),
  FOREIGN KEY (`playlist_id`) REFERENCES `PLAYLIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `USER` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `MOOD` (
  `user_id` integer,
  `set_date` date,
  `state_of_mind` varchar(50),
  PRIMARY KEY (`user_id`, `set_date`),
  FOREIGN KEY (`user_id`) REFERENCES `USER` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `FAVORITE_ARTIST` (
  `user_id` integer PRIMARY KEY,
  `artist_id` integer,
  FOREIGN KEY (`user_id`) REFERENCES `USER` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`artist_id`) REFERENCES `ARTIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `FAVORITE_GENRE` (
  `user_id` integer PRIMARY KEY,
  `genre` varchar(50),
  FOREIGN KEY (`user_id`) REFERENCES `USER` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `RECOMMENDATION` (
  `user_id` integer,
  `song_id` integer,
  `date` date,
  PRIMARY KEY (`user_id`, `song_id`),
  FOREIGN KEY (`user_id`) REFERENCES `USER` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`song_id`) REFERENCES `SONG` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `LISTENS` (
  `user_id` integer,
  `song_id` integer,
  `streams` integer,
  PRIMARY KEY (`user_id`, `song_id`),
  FOREIGN KEY (`user_id`) REFERENCES `USER` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`song_id`) REFERENCES `SONG` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `SONG` (
  `id` integer PRIMARY KEY,
  `title` varchar(50),
  `genre` varchar(50),
  `duration` integer,
  `streams` integer,
  `year` integer
);

CREATE TABLE IF NOT EXISTS `CONTAIN` (
  `playlist_id` integer,
  `song_id` integer,
  PRIMARY KEY (`playlist_id`, `song_id`),
  FOREIGN KEY (`playlist_id`) REFERENCES `PLAYLIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`song_id`) REFERENCES `SONG` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `SING` (
  `song_id` integer,
  `artist_id` integer,
  PRIMARY KEY (`song_id`, `artist_id`),
  FOREIGN KEY (`song_id`) REFERENCES `SONG` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`artist_id`) REFERENCES `ARTIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `ARTIST` (
  `id` integer PRIMARY KEY,
  `name` varchar(50),
  `country` varchar(50),
  `followers` integer
);

CREATE TABLE IF NOT EXISTS `GENRE` (
  `artist_id` integer,
  `genre_name` varchar(50),
  PRIMARY KEY (`artist_id`, `genre_name`),
  FOREIGN KEY (`artist_id`) REFERENCES `ARTIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
);

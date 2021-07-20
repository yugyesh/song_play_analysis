# CREATE TABLE QUERIES
songplay_table_create = """CREATE TABLE IF NOT EXISTS songplay
(songplay_id int, start_time int, user_id int, level varchar, song_id int, artist_id int, session_id int, location varchar, user_agent varchar)"""

users_table_create = """CREATE TABLE IF NOT EXISTS users
(user_id int PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar)"""

songs_table_create = """CREATE TABLE IF NOT EXISTS songs
(song_id int PRIMARY KEY, title varchar, artist_id int, year int, duration int)"""

artists_table_create = """CREATE TABLE IF NOT EXISTS artists
(artist_id int PRIMARY KEY, name varchar, location varchar, latitude varchar, longitude varchar)"""

time_table_create = """CREATE TABLE IF NOT EXISTS time
(start_time float, hour int, day int, week int, month int, year int, weekday int)"""

create_table_queries = [
    songplay_table_create,
    users_table_create,
    songs_table_create,
    artists_table_create,
    time_table_create,
]

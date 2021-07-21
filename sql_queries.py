# DROP TABLE QUERIES
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
users_table_drop = "DROP TABLE IF EXISTS users"
songs_table_drop = "DROP TABLE IF EXISTS songs"
artists_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"


# CREATE TABLE QUERIES
songplays_table_create = """CREATE TABLE IF NOT EXISTS songplays(songplay_id int, start_time int, user_id int,
 level varchar, song_id varchar, artist_id varchar, session_id int, location varchar, user_agent varchar)"""

users_table_create = """CREATE TABLE IF NOT EXISTS users
(user_id int PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar)"""

songs_table_create = """CREATE TABLE IF NOT EXISTS songs
(song_id varchar PRIMARY KEY, title varchar, artist_id varchar, year int, duration int)"""

artists_table_create = """CREATE TABLE IF NOT EXISTS artists
(artist_id varchar PRIMARY KEY, name varchar, location varchar, latitude varchar, longitude varchar)"""

time_table_create = """CREATE TABLE IF NOT EXISTS time
(start_time float, hour int, day int, week int, month int, year int, weekday int)"""

# QUERY LIST
create_table_queries = [
    songplays_table_create,
    users_table_create,
    songs_table_create,
    artists_table_create,
    time_table_create,
]

drop_table_queries = [
    songplay_table_drop,
    users_table_drop,
    songs_table_drop,
    artists_table_drop,
    time_table_drop,
]

import glob
import os

import pandas as pd
import psycopg2
from dotenv import dotenv_values

from sql_queries import (
    song_table_insert,
    time_table_insert,
    user_table_insert,
    artist_table_insert,
    song_select,
    songplay_table_insert,
)


def process_song_file(cur, filepath):
    """This method extracts a song data and stores it in the database

    Args:
        cur ([object]): [database cursor]
        filepath ([string]): [Path of a json file]
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = [
        df.at[0, "song_id"],
        df.at[0, "title"],
        df.at[0, "artist_id"],
        int(df.at[0, "year"]),
        df.at[0, "duration"],
    ]
    try:
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as error:
        print("Error: Unable to insert the song data")
        print(error)

    # insert artists data
    artist_data = [
        df.at[0, "artist_id"],
        df.at[0, "artist_name"],
        df.at[0, "artist_location"],
        df.at[0, "artist_latitude"],
        df.at[0, "artist_latitude"],
    ]
    try:
        cur.execute(artist_table_insert, artist_data)
    except psycopg2.Error as error:
        print("Error: Unable to insert artist data")
        print(error)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"] == "NextSong"]

    # Extract time data
    t = pd.to_datetime(df.ts, unit="ms")
    df["timestamp"] = t
    df["hour"] = t.dt.hour
    df["day"] = t.dt.day
    df["week"] = t.dt.hour
    df["month"] = t.dt.month
    df["year"] = t.dt.year
    df["day_name"] = t.dt.day_name()

    time_df = df[["timestamp", "hour", "day", "week", "month", "year", "day_name"]]
    time_df.drop_duplicates(subset=["timestamp"])

    # Insert time data
    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as error:
            print("Error: Unable to insert time data")
            print(error)

    # Load user data
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # Deleting duplicate userid
    user_df = user_df.drop_duplicates()

    # Change naming convention
    user_df.columns = ["user_id", "first_name", "last_name", "gender", "level"]

    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except psycopg2.Error as error:
            print("Error: Unable to insert user")
            print(error)

    # Insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        try:
            cur.execute(song_select, (row.song, row.artist, row.length))
        except psycopg2.Error as error:
            print("Error: Unable to select artistid and songid")
            print(error)
            continue

        results = cur.fetchone()
        if results:
            songid, artistid = results
            print(results)
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            pd.to_datetime(row.ts),
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent,
        )
        try:
            cur.execute(songplay_table_insert, songplay_data)
        except psycopg2.Error as error:
            print("Error: Unable to insert songplay data")
            print(error)


def process_data(cur, conn, filepath, func):
    """This method process the data and store into the database one by one

    Args:
        cur ([object]): [database cursor]
        conn ([object]): [database connection]
        filepath ([string]): [Root path for the data]
        func ([string]): [Name of the function used to process and store the data]
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print("{} files found in {}".format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print("{}/{} files processed.".format(i, num_files))


def main():
    # extract user and password
    try:
        config = dotenv_values(".env")
        user = config["USER"]
        password = config["PASSWORD"]
    except KeyError as error:
        print("Error: username and password not defined in the environment variable")
        print(error)

    # connect to default database
    try:
        conn = psycopg2.connect(
            "host=127.0.0.1 dbname=sparkifydb user={} password={}".format(
                user, password
            )
        )
    except psycopg2.Error as error:
        print("Error: Unable to connect to the database")
        print(error)

    try:
        cur = conn.cursor()
    except psycopg2.Error as error:
        print("Error: Unable to get cursor")
        print(error)

    # Process song data
    process_data(cur, conn, filepath="data/song_data", func=process_song_file)
    process_data(cur, conn, filepath="data/log_data", func=process_log_file)


if __name__ == "__main__":
    main()

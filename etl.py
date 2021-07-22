import glob
import os

import pandas as pd
import psycopg2
from dotenv import dotenv_values

from sql_queries import *


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
    except psycopg2.Error as e:
        print("Error: Unable to store the song data")
        print(e)

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
    except psycopg2.Error as e:
        print("Error: Unable to store artist data")
        print(e)


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


if __name__ == "__main__":
    main()

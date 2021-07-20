import psycopg2
from dotenv import dotenv_values
from sql_queries import create_table_queries


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
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
            "host=127.0.0.1 dbname=udacity user={} password={}".format(user, password)
        )
    except psycopg2.Error as error:
        print("Error: Unable to connect to the database")
        print(error)

    conn.set_session(autocommit=True)

    try:
        cur = conn.cursor()
    except psycopg2.Error as error:
        # TODO: Use logging
        print("Error: Unable to get cursor")
        print(error)

    # create sparkify database with UTF8 encoding
    try:
        cur.execute("DROP DATABASE IF EXISTS sparkifydb")
        cur.execute(
            "CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0"
        )
    except psycopg2.Error as error:
        print("Error: unable to create database sparkifydb")
        print(error)

    # close connection to default database
    conn.close()

    # connect to sparkify database
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
        # TODO: Use logging
        print("Error: Unable to get cursor")
        print(error)

    return cur, conn


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    try:
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()
    except psycopg2.Error as error:
        print("Error: Unable to create table")
        print(error)


def main():
    """
    - Drops (if exists) and Creates the sparkify database.

    - Establishes connection with the sparkify database and gets
    cursor to it.

    - Drops all the tables.

    - Creates all tables needed.

    - Finally, closes the connection.
    """
    cur, conn = create_database()

    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

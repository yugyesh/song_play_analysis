import psycopg2
from dotenv import dotenv_values


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
    # extract user and password
    config = dotenv_values(".env")
    user = config["USER"]
    password = config["PASSWORD"]

    # connect to default database
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=udacity user={} password={}".format(user, password)
    )
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user={} password={}".format(user, password)
    )
    cur = conn.cursor()

    return cur, conn

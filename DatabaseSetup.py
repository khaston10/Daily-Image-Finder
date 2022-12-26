"""
This script should only be used to initially setup the database and tables for this project.

"""
import mysql.connector
import os
from DatabaseFunctions import add_credentials


def main():
    # Define database Stuff
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ["MySql_Password"],
    )

    # Create a cursor
    c = conn.cursor()

    # Create a database
    c.execute("CREATE DATABASE IF NOT EXISTS Daily_Image_Finder")

    conn.database = "Daily_Image_Finder"
    # Add user_data table.
    sql = """
        CREATE TABLE user_data
        (
        user_id int NOT NULL AUTO_INCREMENT,
        email varchar(50),
        psswrd varchar(50),
        keyword varchar(30),
        primary key(user_id)
        );
    """

    c.execute(sql)

    sql = """
        CREATE TABLE log
        (
        user_id int,
        date_of_log date,
        scraper_success bool,
        email_success bool
        );
    """

    c.execute(sql)


if __name__ == '__main__':
    main()
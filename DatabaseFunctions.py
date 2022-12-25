import mysql.connector
import os


def add_credentials(email, psswrd):
    # Define database Stuff
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ["MySql_Password"],
        database="daily_image_finder",
    )

    if not check_if_email_exists(email):
        # Create a cursor
        c = conn.cursor()

        sql = "INSERT INTO user_data (email, psswrd, keyword) VALUES (%s, %s, %s)"
        val = (email, psswrd, "")
        c.execute(sql, val)
        conn.commit()
        return True
    else:
        return False


def check_if_email_exists(email):
    # Define database Stuff
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ["MySql_Password"],
        database="daily_image_finder",
    )
    email_listed_in_table =  False
    # Create a cursor
    c = conn.cursor()

    query = "SELECT email FROM user_data"
    c.execute(query)

    rows = c.fetchall()
    for row in rows:
        if row[0].lower() == email.lower():
            email_listed_in_table = True

    return email_listed_in_table


def check_if_credentials_are_correct(email, psswrd):
    credentials_are_correct = False

    # Define database Stuff
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ["MySql_Password"],
        database="daily_image_finder",
    )
    # Create a cursor
    c = conn.cursor()

    query = "SELECT email, psswrd FROM user_data"
    c.execute(query)
    rows = c.fetchall()

    for row in rows:
        if email.lower() == row[0].lower() and psswrd == row[1]:
            credentials_are_correct = True

    return credentials_are_correct


def get_user_id(email):
    user_id = 0

    # Define database Stuff
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ["MySql_Password"],
        database="daily_image_finder",
    )
    # Create a cursor
    c = conn.cursor()

    query = "SELECT user_id, email FROM user_data"
    c.execute(query)
    rows = c.fetchall()

    for row in rows:
        if email.lower() == row[1].lower():
            user_id = row[0]

    return user_id


def update_key_word(email, key_word):
    key_word_updated = True
    user_id = get_user_id(email)

    # Define database Stuff
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ["MySql_Password"],
        database="daily_image_finder",
    )
    # Create a cursor
    c = conn.cursor()

    c.execute("UPDATE user_data SET keyword = \"" + key_word + "\" Where user_data.user_id = " + str(user_id) + ";")

    conn.commit()

    return key_word_updated


def check_email_password(email, password):
    # In the future this needs to query the database
    if email == "good@email.com" and password == "good password":
        return True
    else:
        return False


def get_key_word(email):
    key_word = ""

    # Define database Stuff
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ["MySql_Password"],
        database="daily_image_finder",
    )
    # Create a cursor
    c = conn.cursor()

    query = "SELECT email, keyword FROM user_data"
    c.execute(query)
    rows = c.fetchall()

    for row in rows:
        if row[1] is not None:
            if email.lower() == row[0].lower():
                key_word = row[1]

    return key_word

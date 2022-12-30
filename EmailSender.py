import smtplib
from email.message import EmailMessage
import os
import imghdr
import mysql.connector


Email_Address = os.environ.get("EmailAddress")
Email_Password = os.environ.get("EmailPassword")
user_data = {}  # Key: User_id, Value: email
log_data = {} # Key: User_id, Value: scraper_success


def main():
    # 1. Import data from the user and log table.
    import_user_data()
    import_log_data()
    # 2. Send emails to all users that have a last log entry set as a success.
    send_all_emails()
    # 3. Update the log table with successes and failures.


def import_user_data():
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
        user_data[row[0]] = row[1]

    conn.close()


def import_log_data():
    # Define database Stuff
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ["MySql_Password"],
        database="daily_image_finder",
    )

    # Create a cursor
    c = conn.cursor()

    query = "SELECT user_id, scraper_success FROM log WHERE date_of_log = current_date();"
    c.execute(query)

    rows = c.fetchall()
    for row in rows:
        log_data[row[0]] = row[1]

    print(log_data)
    conn.close()


def send_all_emails():
    for key in user_data:
        if log_data[key]:
            send_email(key, "DIF", "Daily_Image_Finder")


def send_email(user_id, subject, message):
    to_email = user_data[user_id]
    path_to_image = 'imgs/' + str(user_id) + '.jpg'
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = Email_Address
    msg['To'] = to_email
    msg.set_content(message)

    with open(path_to_image, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name

    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(Email_Address, Email_Password)
        smtp.send_message(msg)


if __name__ == '__main__':
    main()



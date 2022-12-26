import time
from random import randint
from selenium import webdriver
import requests
import io
from PIL import Image
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import mysql.connector
import os
import datetime

PATH = "\\chromedriver.exe"
service_obj = Service(PATH)
wd = webdriver.Chrome(service=service_obj)
user_data = {}
log = {}


def get_user_data():
    # Define database Stuff
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ["MySql_Password"],
        database="daily_image_finder",
    )

    # Create a cursor
    c = conn.cursor()

    query = "SELECT user_id, keyword FROM user_data"
    c.execute(query)

    rows = c.fetchall()
    for row in rows:
        user_data[row[0]] = row[1]

    conn.close()


def update_log_table(user_id, success):
    # Define database Stuff
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ["MySql_Password"],
        database="daily_image_finder",
    )

    # Create a cursor
    c = conn.cursor()

    sql = "INSERT INTO log(user_id, date_of_log, scraper_success) VALUES (" + str(user_id).upper() + ", \'" + \
          str(datetime.date.today()) + "\', " + str(success) + ");"
    print(sql)
    c.execute(sql)
    conn.commit()
    conn.close()


def download_all_images_using_user_data():
    for key in user_data:
        initial_image_url = set_initial_image_url(user_data[key])
        urls = get_images_from_google(wd, 2, 3, initial_image_url)
        # Grab random URL from the returned set and download it.
        rand_index = randint(0, len(urls) - 1)
        image_has_been_down_loaded = download_images("imgs/", list(urls)[rand_index], str(key) + ".jpg")
        # log the data.
        update_log_table(key, image_has_been_down_loaded)


def set_initial_image_url(key_word):
    in_image_url = "https://www.google.com/search?tbm=isch&q=" + key_word
    return in_image_url


def download_images(download_path, url, file_name):

    image_has_been_downloaded = False
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
        image_has_been_downloaded = True

    except Exception as e:
        print("Fail")

    return image_has_been_downloaded


def get_images_from_google(wd, delay, max_images, in_image_url):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    wd.get(in_image_url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_to_end(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls): max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                # Check to see if we are stuck pulling the same image.
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print("Found Image!")

        return image_urls


if __name__ == '__main__':
    get_user_data()
    download_all_images_using_user_data()


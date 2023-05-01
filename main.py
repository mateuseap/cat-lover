import os
import tweepy
from dotenv import load_dotenv
import datetime
import requests
from keep_alive import keep_alive
import time

def api():
    auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    return tweepy.API(auth)

def generate_posts_datetime():
    start_date = datetime.datetime.today().replace(hour=0, minute=0)
    end_date = start_date + datetime.timedelta(days=1)

    interval = datetime.timedelta(hours=1)

    date_array = []
    current_date = start_date
    while current_date < end_date:
        date_array.append(current_date.strftime("%Y-%m-%d %H:%M"))
        current_date += interval

    return date_array

def get_cat_image(tag: str = None):
    if tag is not None:
        url = "https://cataas.com/cat"
    else:
        url = f'https://cataas.com/cat/{tag}'

    response = requests.get(url)

    if response.status_code == 200:
        image = response.content

        with open("cat.png", "wb") as f:
            f.write(image)
    else:
        print("Error: could not retrieve image.")

def upload_files(api: tweepy.API, files_paths: list):
    files_ids = []

    for file_path in files_paths:
        media = api.media_upload(filename = file_path)
        files_ids.append(media.media_id)

    return files_ids

def retweet(api: tweepy.API, tweet_id: int, message: str = None, tweet_base_url: str = None, files_paths: list = None):
    if (message is not None) and (files_paths is not None):
        files_ids = upload_files(api, files_paths)
        api.update_status(status = message, attachment_url = tweet_base_url + tweet_id, media_ids = files_ids)
    elif message is not None:
        api.update_status(status = message, attachment_url = tweet_base_url + tweet_id)
    elif files_paths is not None:
        files_ids = upload_files(api, files_paths)
        api.update_status(status = '', attachment_url = tweet_base_url + tweet_id, media_ids = files_ids)
    else:
        api.retweet(id=tweet_id)

    print('Retweeted Successfully!')

def tweet(api: tweepy.API, message: str, file_path: str = None):
    if file_path is not None:
        api.update_status_with_media(status = message, filename = file_path)
    else:
        api.update_status(status = message)

    print('Tweeted Successfully!')

if __name__ == '__main__':
    load_dotenv()
    
    api = api()

    sleep_duration = 2 * 60 * 60

    keep_alive()

    while True:
        get_cat_image(tag = 'cute')
        tweet(api, message = 'Cute cat!', file_path = 'cat.png')

        time.sleep(sleep_duration)

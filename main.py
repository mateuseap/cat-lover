import os
import time
import tweepy
from dotenv import load_dotenv
from keep_alive import keep_alive
from utils import get_cat_image, tweet, get_random_tag

def api():
    auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    return tweepy.API(auth)

if __name__ == '__main__':
    load_dotenv()
    
    api = api()

    sleep_duration = 2 * 60 * 60

    keep_alive()

    while True:
        get_cat_image(tag = 'cute')
        tweet(api, message = 'Cute cat!', file_path = 'cat.png')

        time.sleep(sleep_duration)

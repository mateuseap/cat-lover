import os
import tweepy
from dotenv import load_dotenv
from datetime import datetime

def api():
    auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    return tweepy.API(auth)

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

    retweet(
        api,
        tweet_id='1644892115149651968',
        message=f'Hello calvo @Jongaranhao! {datetime.now()}', 
        tweet_base_url='https://twitter.com/mateuseliaas/status/', 
    )
import tweepy
import os
import random

# Twitter API credentials
API_KEY = 'EaQ9DgVWf5owWGbMxuK5RRILC'
API_SECRET_KEY = 'xNsdN2nN0YA04D0eEV3M91Zd2RFXfhh9jL4fIczeJ9rQ9Go226'
ACCESS_TOKEN = '1798813245127426048-pgDHcfjQjVU9c1Fz5jXNKKVSOntpfr'
ACCESS_TOKEN_SECRET = 'qJjCmQXsoS4TOhM06EctEvCZ7xqKnkqYQujJ3XfbPMmUo'

def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client

client_v1 = get_twitter_conn_v1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
client_v2 = get_twitter_conn_v2(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Path to the directory containing photos
photos_directory = "photos"
log_file = "tweeted_photos.log"

# Ensure the directory exists
if not os.path.exists(photos_directory):
    raise FileNotFoundError(f"The directory {photos_directory} does not exist")

# List all files in the directory
photos = os.listdir(photos_directory)

# Read the log file to get the list of already tweeted photos
if os.path.exists(log_file):
    with open(log_file, "r") as file:
        tweeted_photos = set(file.read().splitlines())
else:
    tweeted_photos = set()

# Select a photo that hasn't been tweeted yet
untweeted_photos = list(set(photos) - tweeted_photos)

# Ensure there are untweeted photos
if not untweeted_photos:
    raise FileNotFoundError("All photos have been tweeted")

# Select a random untweeted photo
selected_photo = random.choice(untweeted_photos)
media_path = os.path.join(photos_directory, selected_photo)

# Upload the media
media = client_v1.media_upload(filename=media_path)
media_id = media.media_id

# Create a tweet with the uploaded media
client_v2.create_tweet(media_ids=[media_id])

# Update the log file with the tweeted photo
with open(log_file, "a") as file:
    file.write(f"{selected_photo}\n")

print(f"Tweeted with media: {media_path}")

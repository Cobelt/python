import tweepy
import stream_listener
import random

# variables
languages = ["en"]
locations_number = 15
trends_number = 5

# auth variables of the twitter app
consumer_key = 'syw9UpyitiyKL87kG0prc73gL'
consumer_secret = 'aQ8FTv1mujffEnltgFHCr0PRbXG3UG7hBngkYAYI33722qHwxE'
access_token_secret = '13GJmaVke8i6C8ckF2aI9Xu9z97u91PwzfBMZpKmj3ks8'
access_token = '758698296584048640-mTWwvJFBBYIKMMI4jzH28cGymNhURHP'

# auth to the tweepy API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


trends_locations = api.trends_available()
trends_name = []

# appending random top trends
for i in range(0, locations_number):
    rand = random.randint(0, 49)
    woeid = trends_locations[rand]['woeid']
    data = api.trends_place(woeid)
    trends = data[0]['trends'][:trends_number]
    for trend in trends:
        trends_name.append(trend['name'])


# creation of the tweepy stream
stream_listener = stream_listener.Twitter_stream_listener()
stream = tweepy.Stream(auth, stream_listener)

stream.filter(languages=languages, track=trends_name, async=True)


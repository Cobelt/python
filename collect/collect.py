import tweepy
import stream_listener
import random

# variables
languages = ["en"]
locations_number = 15

# trends_number = 5
# auth variables of the twitter app
consumer_key = 'syw9UpyitiyKL87kG0prc73gL'
consumer_secret = 'aQ8FTv1mujffEnltgFHCr0PRbXG3UG7hBngkYAYI33722qHwxE'
access_token_secret = '13GJmaVke8i6C8ckF2aI9Xu9z97u91PwzfBMZpKmj3ks8'

access_token = '758698296584048640-mTWwvJFBBYIKMMI4jzH28cGymNhURHP'
# auth to the tweepy API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)

# trends_locations = api.trends_available()
trends_name = []


# appending random top trends
# for i in range(0, locations_number):
#     rand = random.randint(0, 49)
#     woeid = trends_locations[rand]['woeid']
#     data = api.trends_place(woeid)
#     trends = data[0]['trends'][:trends_number]
#     for trend in trends:
#         trend += " "
#         trends_name.append(trend['name'])


def emoji_store(start, end, tab):
    for val in range(start, end):
        tab.append(chr(val))

emoji_tab = []


emoji_store(int("1F600", 16), int("1F607",16), emoji_tab)
emoji_store(int("1F609", 16), int("1F60F",16), emoji_tab)
emoji_store(int("1F617", 16), int("1F61D",16), emoji_tab)
emoji_store(int("1F61E", 16), int("1F629",16), emoji_tab)
emoji_store(int("1F630", 16), int("1F631",16), emoji_tab)


def collect_stream(query, languages):
    # creation of the tweepy stream

    listener = stream_listener.Twitter_stream_listener()
    stream = tweepy.Stream(auth, listener)
    stream.filter(languages=languages, track=query, async=True)


collect_stream(emoji_tab, languages)





import tweepy
import stream_listener

# auth variables
consumer_key = 'syw9UpyitiyKL87kG0prc73gL'
consumer_secret = 'aQ8FTv1mujffEnltgFHCr0PRbXG3UG7hBngkYAYI33722qHwxE'
access_token_secret = '13GJmaVke8i6C8ckF2aI9Xu9z97u91PwzfBMZpKmj3ks8'
access_token = '758698296584048640-mTWwvJFBBYIKMMI4jzH28cGymNhURHP'

# auth to the API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


stream_listener = stream_listener.Twitter_stream_listener()
stream = tweepy.Stream(auth, stream_listener)

stream.filter(track=['#python'], async=True)





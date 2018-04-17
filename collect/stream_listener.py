import tweepy
import json
import io

class Twitter_stream_listener(tweepy.StreamListener):

    def on_status(self, data):
        with io.open('../collecting_file.json', 'a') as outfile:
            outfile.write(data)
            outfile.close()
        print(data)
        return True


    def on_error(self, status_code):
        if status_code == 420:
            return False



import tweepy

class Twitter_stream_listener(tweepy.StreamListener):

    def on_data(self, data):
        collecting_file = open('collecting_file.json', 'a')
        collecting_file.write(data)
        print(data)

    def on_error(self, status_code):
        if status_code == 420:
            return False

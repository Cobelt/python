from preprocessing import text_preprocessing

csv_name = "../preprocess_tweet_file.csv"

def load_tweets():
    print("ok")
    tweets = text_preprocessing.csv_file_to_numpy_array(csv_name)

    return tweets

load_tweets()
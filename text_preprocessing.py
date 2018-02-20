import json
import polyglot
from polyglot.text import Text, Word


class Tweet_process:
    text = None

    #à mettre des condition avec isinstance pour gerer cas chaine de tweet ou json etc
    def __init__(self, tweet_string):
        tweet_json = json.loads(tweet_string)
        self.text = Text(tweet_json["text"])


    def tokenize_text(self):
        return self.text.words

'''
    def tokenize_text(self, json_tweet):
        if isinstance(json_tweet, json):
            print ("Erreur : ce n'est pas un json")
        else:
            tweet_text = Text(json_tweet.text)
            self.token_text = tweet_text
'''

def fill_tab_tweet_from_file(tab, file_name):
    with open (file_name) as file:
        for line in file:
            tab.append(Tweet_process(line))


#main

tab_tweet = []
fill_tab_tweet_from_file(tab_tweet, "collecting_file.json")


# Partie test

print(tab_tweet[0].text.words)

'''
tweet = {}
tweet["text"] = "hello i'm from france :D"
tweet['people'] = []
tweet['people'].append({
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
tweet['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
tweet['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})


tweet2 = {}
tweet2["text"] = "hi, i'm born in Vietnam, nice to meet you :p"

print ("tweet")
print(tweet)

#écriture d'un json dans un fichier
with open('tweet_test.json', 'w') as outfile:
    json.dump(tweet, outfile)
    json.dump(tweet2, outfile)


with open("collecting_file.json") as file:
    for line in file:
        print ("tweet ", " : ", "\n")
        #line = file.readline()
        json_data = json.loads(line)
        print(json_data["text"], "\n")
'''
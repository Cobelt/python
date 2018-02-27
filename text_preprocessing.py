import json
import polyglot
from polyglot.text import Text, Word
from polyglot.detect import Detector


class Tweet_process:
    tab_tweet_text = []
    tab_tweet_words = [[]]



    #à mettre des condition avec isinstance pour gerer cas chaine de tweet ou json etc
    # def __init__(self):
    #     tab_tweet_text = []
    #     tab_tweet_word = [[]]

    # def tokenize_text(self):
    #     return self.text.words



    def fill_tab_tweet_from_file(self, file_name):
        tab_words = [] #no more need length of list for loop
        with open (file_name) as file:
            for line in file:
                tweet_json = json.loads(line)
                tweet_text = Text(tweet_json['text'])
                self.tab_tweet_text.append(tweet_text)
                print (Detector(tweet_json['text']).language)
                # try:
                for x in tweet_text.words:
                    tab_words.append(str(x))
                self.tab_tweet_words.append(tab_words)
# main

tweet = Tweet_process()
tab = []
tweet.fill_tab_tweet_from_file('collecting_file.json')
for x in tweet.tab_tweet_text[0].words:
    tab.append(x)

print (tab)

# Partie test


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
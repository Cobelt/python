import json
import polyglot
from polyglot.text import Text, Word
from polyglot.detect import Detector
import sys

import re
import encodings


file_in = 'collecting_file2.json'
file_out = 'collecting_file_test.json'


#Cleaning function may leave blankspace at the start or the end because it only remove emot
# ex : ":) hello :)" => " hello "
class Tweet_process:


    #à mettre des condition avec isinstance pour gerer cas chaine de tweet ou json etc
    def __init__(self):
        self.text = ''
        self.clean_text = ''
        self.emoticons_list = []
        self.polarity = 0 # 1 : happy, 0: neutral, -1 : angry
        self.words_list = []


    #construct the class
    #line : json line
    def constructor_json(self, line):
        tweet_data = json.loads(line)

        #dont know how to handle probleme tweet dont have key text
        #return value(false) different of what function normaly do is a bad habit
        #raise error may not be worth to use
        if 'text' in tweet_data:
            tweet_text = tweet_data['text']
        else:
            tweet_text = ""

        self.text = tweet_text

        self.clean_store_emoticon(tweet_text)
        self.store_polarity_emoticon(self.emoticons_list)

        # self.store_tokenize(self.clean_text, "Anglais")
        #dont know what is the best : function or a constructor
        #return self


    #text is a string
    def clean_store_emoticon(self, sentence):
        #regex
        emoticons_unicode = r"""
                            ([\U0001F600-\U0001F64F])| #emoticons
                            ([\U00002702-\U000027B0])| #Enclosed Characters
                            ([\U0001F680-\U0001F6C0])| #dingbats
                            ([\U000004C2-\U0001F251]) #transport and map symboles
                            """

        emoticon_re = re.compile(emoticons_unicode, re.VERBOSE | re.UNICODE)

        line = sentence
        match_obj = emoticon_re.search(line)
        while (match_obj is not None):
            self.emoticons_list.append(match_obj.group())
            line = line[:match_obj.start()] + line[match_obj.end():]
            match_obj = emoticon_re.search(line)

        self.clean_text = line

    def store_polarity_emoticon(self, emoticon_list):
        #regex
        happy_emote_unicode = r"""([\U0001F601-\U0001F60F])"""
        angry_emote_unicode = r"""([\U0001F61E-\U0001F624])"""

        re_happy_emote = re.compile(happy_emote_unicode, re.VERBOSE|re.UNICODE)
        re_agnry_emote = re.compile(angry_emote_unicode, re.VERBOSE|re.UNICODE)

        counter_happy_emote = 0
        counter_angry_emote = 0

        #count number of emoji in text
        for x in emoticon_list:
            if re_happy_emote.match(x):
                counter_happy_emote += 1
            elif re_agnry_emote.match(x):
                counter_angry_emote += 1

        #processing polarity
        if counter_happy_emote > 0 and counter_angry_emote > 0:
            self.polarity = 0
        elif counter_happy_emote > 0:
            self.polarity = 1
        elif counter_angry_emote > 0:
            self.polarity = -1
        else:
            self.polarity = 0 #traitement non nécessaire du au constructeur

    def store_tokenize(self, text, language):
        #Only process reliable langage detect by polyglot




        try:
            detector = Detector(text)
            # if not detector.reliable and detector.language.name == language:
            #     T_text = Text(text)
            #     self.words_list = T_text.words
        except UnknownLanguage:
            print ("Can't tokenize, can't detect language of tweet")
            raise
        except:
            raise


        # try:
        #     self.words_list = T_text.words
        #     break;
        # except UnknownLanguage:



    def create_json(self):
        #json format
        data = {"text": "", "clean_text": "", "emoticons_list" : []}

        #fill data
        data['text'] = self.text
        data['clean_text'] = self.clean_text

        for x in self.emoticons_list:
            data['emoticons_list'].append(x)

        return data

def fill_tab_Tweet_process_from_json_file(tab, file_name):
    with open (file_name) as file:
        for line in file:
            x = Tweet_process()
            x.constructor_json(line)
            tab.append(x)


def fill_json_file_from_tab_Tweet_process(tab, file_name):
    with open(file_name, 'w') as file:
        for tweet_preprocess in tab:
            json.dump(tweet_preprocess.create_json(),file)
            file.write('\n')
#main

tab_tweet = []
fill_tab_Tweet_process_from_json_file(tab_tweet, file_in)
fill_json_file_from_tab_Tweet_process(tab_tweet, file_out)

# Partie test
#
# phrase = "bonjour - je test aha ha ha :. Mais, Tu sais je suis peut être...; non rien! Demain il va faire beau, ça te dirait de sortir. I have the fate to rule over the world"
# phrase = "fplsfdjgpefjgnod ghegoierg nhçerpghqer goerhgiugrbhpe"
# token_phrase = Text(phrase)
# detector = Detector(phrase)
#
# for language in Detector(phrase).languages:
#   print(language)
#
# print (detector.reliable)
# print (detector.language.name)
#
# print (token_phrase)
# print(detector.language)
# print (token_phrase.words)

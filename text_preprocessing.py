import json
from polyglot.detect import Detector
import preprocessor
import re
import pandas



tweet_file = 'collecting_file.json'
preprocess_tweet_json = 'preprocess_tweet_file.json'
preprocess_tweet_csv = 'preprocess_tweet_file.csv'


#Cleaning function may leave blankspace at the start or the end because it only remove emot
# ex : ":) hello :)" => " hello "
class Tweet_preprocess:


    #à mettre des condition avec isinstance pour gerer cas chaine de tweet ou json etc
    def __init__(self, language = ''):
        self.language = language
        self.text = ''
        self.clean_text = ''
        self.emoticons_list = []
        self.polarity = 0 # 1 : positive, 0: neutral, -1 : negative
        self.words_list = []

    def constructor_json(self, line):
        """
        **construct the class from tweet data**
        :param line: json
        :return: boolean
        """
        tweet_data = json.loads(line)

        # dont know how to handle probleme tweet dont have key text
        # return value(false) different of what function normaly do is a bad habit
        # raise error may not be worth to use
        # if 'text' att dont existe we won't do a empty tweet (we can)
        if 'text' in tweet_data:
            tweet_text = tweet_data['text']
            tweet_text_exist = True
        else:
            tweet_text_exist = False


        if tweet_text_exist:
            # Only process reliable langage detect by polyglot
            try:
                detector = Detector(tweet_text, quiet=True)
                #if reliable, we use language detect by polyglot detector
                if not detector.reliable and not self.language: #empty string => false in boolean context
                    process_reliable = True
                    self.language = detector.language.name
                #if reliable and language is what we define
                elif not detector.reliable and detector.language.name == self.language:
                    process_reliable = True
                else:
                    process_reliable = False
            except:
                raise


        if tweet_text_exist and process_reliable:

            self.text = tweet_text

            #cleaning
            self.clean_store_emoticon(tweet_text) #normally clean_text empty, this one fill it
            self.clean_text = preprocessor.clean(self.clean_text)

            self.polarity = self.polarity_emoticon(self.emoticons_list)

            self.tokenize_text(self.clean_text)
            return True
        else:
            return False


    def clean_store_emoticon(self, sentence):
        """
        **remove emoji using unicode then store in emoticons_list**
        :param sentence: string
        :return: string: text clean
        """

        #regex
        emoticons_unicode = r"""
                            ([\U0001F300-\U0001F64F])| #emoticons + Uncategorized
                            ([\U00002122-\U00003299])| #Enclosed Characters + Uncategorized
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

    def polarity_emoticon(self, emoticon_list):
        """
        **polarity work for sentence with only 1 type of emoji (positive/negative) else neutral**
        :param emoticon_list: list of unicode emoji
        :return: 1 (positive), -1 (negative), 0 (neutral)
        """

        #regex
        positive_emote_unicode = r"""
                                ([\U0001F600-\U0001F607])|
                                ([\U0001F609-\U0001F60F])|
                                ([\U0001F617-\U0001F61D])
                                """
        negative_emote_unicode = r"""
                                ([\U0001F61E-\U0001F629])|
                                ([\U0001F630-\U0001F631])
                                """

        re_positive_emote = re.compile(positive_emote_unicode, re.VERBOSE|re.UNICODE)
        re_agnry_emote = re.compile(negative_emote_unicode, re.VERBOSE|re.UNICODE)

        counter_positive_emote = 0
        counter_negative_emote = 0

        #count number of emoji in text
        for x in emoticon_list:
            if re_positive_emote.match(x):
                counter_positive_emote += 1
            elif re_agnry_emote.match(x):
                counter_negative_emote += 1

        #processing polarity
        if counter_positive_emote > 0 and counter_negative_emote > 0:
            return 0
        elif counter_positive_emote > 0:
            return 1
        elif counter_negative_emote > 0:
            return -1
        else:
            return 0

    def tokenize_text(self, text):
        """
        tokenize text in to words then store in clean_text
        :param text: string
        :return: None
        """
        text_token = preprocessor.tokenize(text)
        self.words_list = text_token.split()



    def create_json(self):
        """
        **Create a json of Tweet_preprocess class
        :return: A json of the class with all att of class
        """

        #json format
        data = {"language": "","text": "", "clean_text": "", "emoticons_list" : [], "polarity" : "0", "words_list" : []}

        #fill data
        data['language'] = self.language
        data['text'] = self.text
        data['clean_text'] = self.clean_text
        data['emoticons_list'] = self.emoticons_list
        data['polarity'] = self.polarity
        data['words_list'] = self.words_list

        return data


def fill_tab_Tweet_preprocess_from_json_file(tab, file_name):
    """
    **Extract data from json file to add to tab with Tweet_preprocess**
    :param tab: a list of Tweet_preprocess or empty
    :param file_name: path to a json file[IN]
    :return: None
    """
    with open (file_name) as file:
        for line in file:
            x = Tweet_preprocess()
            if x.constructor_json(line): #construct and test in same time
                tab.append(x)

def fill_json_file_from_tab_Tweet_preprocess(tab, file_name, neutral_polarity = False):
    """
    **extract data of tab of Tweet_preprocess to write it on a file in json format**
    :param tab: a list of Tweet_preprocess
    :param file_name: path to a json file[OUT]
    :param neutral_polarity: boolean : True keep neutral tweet else dont
    :return: None
    """
    with open(file_name, 'w') as file:
        for tweet_preprocess in tab:
            if neutral_polarity == False:
                if tweet_preprocess.polarity != 0:
                    json.dump(tweet_preprocess.create_json(), file, sort_keys=True)
                    file.write('\n')
            else:
                json.dump(tweet_preprocess.create_json(), file, sort_keys=True)
                file.write('\n')



#upgrade possible: take a json file (dict methode)
#with row name parameter (can chose what to write in csv)
#and the test on polarity != 0 can be done in json
def fill_csv_file_from_Tweet_preprocess(tab, file_out, neutral_polarity = False):
    """
    #Write clean_text and polarity of a table of Tweet_preprocess in a csv file
    :param tab: a list of Tweet_preprocess
    :param file_out: path to a csv file [OUT]
    :param neutral_polarity: boolean : True keep neutral tweet else dont
    :return: None
    """
    df_result = pandas.DataFrame()
    for tweet_preprocess in tab:
        if neutral_polarity == False:
            if tweet_preprocess.polarity != 0:
                data = [[tweet_preprocess.clean_text, tweet_preprocess.polarity]]
                df_local = pandas.DataFrame(data=data,columns=['clean_text', 'polarity'])
                df_result = df_result.append(df_local, ignore_index=True)
        else:
            data = [[tweet_preprocess.clean_text, tweet_preprocess.polarity]]
            df_local = pandas.DataFrame(data=data, columns=['clean_text', 'polarity'])
            df_result = df_result.append(df_local, ignore_index=True)
    df_result.to_csv(file_out)


def csv_file_to_numpy_array(csv_file_in, row=slice(0,None, None), column=["clean_text", "polarity"]):
    """
    **convert dataFrame from a csv file to a numpy array**
    by default: function use all row and column clean_text,polarity
    :param csv_file_in:
    :param row: single label, array label, slice label, boolean array
    :param column: single label, array label, slice label, boolean array
    :return: numpy Array
    """
    df = pandas.read_csv(preprocess_tweet_csv)
    sub_df = df.loc[row,column]
    return sub_df.values


#main

tab_tweet = []
fill_tab_Tweet_preprocess_from_json_file(tab_tweet, tweet_file)
fill_json_file_from_tab_Tweet_preprocess(tab_tweet, preprocess_tweet_json, True)
fill_csv_file_from_Tweet_preprocess(tab_tweet, preprocess_tweet_csv, True)
numpy_array = csv_file_to_numpy_array(preprocess_tweet_csv)


# Partie test
# print ("debut partie test")
# with open(tweet_file) as file:
#     for line in file:
#         print ("============================= TWEET ========================")
#         tweet = json.loads(line)
#         print (tweet['id'])

# print(numpy_array)
# print ("fin partie test")

# for i in range (10):
#     print ("tweet numero ", i)
    # print (tab_tweet[i].create_json())
    # print ("text complet")
    # print (tab_tweet[i].text)
    # print ("text clean")
    # print (tab_tweet[i].clean_text)
    # print ("emoticon list")
    # print (tab_tweet[i].emoticons_list)
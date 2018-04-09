import preprocessing.text_preprocessing as txt_prepro
from sklearn.feature_extraction.text import TfidfVectorizer

dataset = []
txt_prepro.fill_tab_Tweet_process_from_json_file(dataset, 'collecting_file.json')

dataset_sentences = [data.clean_text for data in dataset]

vectorizer = TfidfVectorizer(encoding='utf-8',
                             decode_error='strict',
                             strip_accents=None,
                             analyzer='char',
                             stop_words='english',
                             ngram_range=(2,4),
                             lowercase=True,
                             max_features=None,
                             binary=False,
                             norm=None,
                             use_idf=True,
                             smooth_idf=False,
                             min_df=0.1,
                             max_df=0.8,
                             sublinear_tf=True)

print(vectorizer.fit_transform(dataset_sentences))

print(vectorizer.get_feature_names())

print(vectorizer.vocabulary_)








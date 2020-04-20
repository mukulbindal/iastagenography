from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os
try:
    import nltk
    nltk.download('stopwords')
except:
    pass
from nltk.corpus import stopwords
import string

print(os.getcwd())
def process_text(text):
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)

    clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

    return clean_words


classifier_file = open("./Pickle/classifier.pickle", "rb")
classifier = pickle.load(classifier_file)
print(type(classifier))

vectorizer_file = open("./Pickle/vectorizer.pickle", "rb")
print(vectorizer_file)
vectorizer = pickle.load(vectorizer_file)

print(type(vectorizer))


def is_spam(text):
    mb = vectorizer.transform([text])
    # mb
    isspam = classifier.predict(mb)[0]

    if isspam == 1:
        return True
    else:
        return False

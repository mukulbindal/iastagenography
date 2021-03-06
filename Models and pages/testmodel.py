from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

from nltk.corpus import stopwords
import string
try:
    import nltk
    nltk.download('stopwords')
except:
    pass
def process_text(text):
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)

    clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

    return clean_words


classifier_file = open("classifier.pickle", "rb")
classifier = pickle.load(classifier_file)
print(type(classifier))

vectorizer_file = open("vectorizer.pickle", "rb")
vectorizer = pickle.load(vectorizer_file)

print(type(vectorizer))


def is_spam(message):
    mb = vectorizer.transform([text])
    # mb
    isspam = classifier.predict(mb)[0]

    if isspam == 1:
        return True
    else:
        return False


while True:

    text = input("Enter a message")

    mb = vectorizer.transform([text])
    # mb
    isspam = classifier.predict(mb)[0]

    if isspam==1:
      print("This message is spam")
    else:
      print("This message is not spam")


# -*- coding: utf-8 -*-
"""iasteganography-Decision Tree model

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13jAdI6SfhTc1rOuraHiNNvE2zHak49as
"""

import numpy as np 
import pandas as pd 
import nltk
from nltk.corpus import stopwords
import string

df = pd.read_csv('https://raw.githubusercontent.com/mukulbindal/Steganography/master/emails.csv') #read the CSV file
df.head(5)

df.shape

df.columns

df.drop_duplicates(inplace = True)

df.shape

df=pd.DataFrame(df).dropna()

df.isnull().sum()

nltk.download('stopwords')

def process_text(text):
    
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    
    
    clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    
    
    return clean_words

df['text'].head().apply(process_text)

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(analyzer=process_text)
messages_bow = vectorizer.fit_transform(df['text'])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(messages_bow, df['spam'], test_size = 0.20, random_state = 0)

messages_bow.shape

from sklearn import tree
classifier = tree.DecisionTreeClassifier().fit(X_train, y_train)

print(classifier.predict(X_train))
print(y_train.values)

from sklearn.metrics import classification_report,confusion_matrix, accuracy_score
pred = classifier.predict(X_train)
print(classification_report(y_train ,pred ))
print('Confusion Matrix: \n',confusion_matrix(y_train,pred))
print()
print('Accuracy: ', accuracy_score(y_train,pred))

print('Predicted value: ',classifier.predict(X_test))
print('Actual value: ',y_test.values)

from sklearn.metrics import classification_report,confusion_matrix, accuracy_score
pred = classifier.predict(X_test)
print(classification_report(y_test ,pred ))

print('Confusion Matrix: \n', confusion_matrix(y_test,pred))
print()
print('Accuracy: ', accuracy_score(y_test,pred))

text = input("Enter the input data ")

mb = vectorizer.transform([text])
# mb
isspam = classifier.predict(mb)[0]

if isspam==1:
  print("This message is spam")
else:
  print("This message is not spam")

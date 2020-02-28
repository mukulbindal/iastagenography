# -*- coding: utf-8 -*-
"""iasteganography-Decision Tree model

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13jAdI6SfhTc1rOuraHiNNvE2zHak49as
"""

#Import libraries
import numpy as np 
import pandas as pd 
import nltk
from nltk.corpus import stopwords
import string

df = pd.read_csv('https://raw.githubusercontent.com/mukulbindal/Steganography/master/emails.csv') #read the CSV file
df.head(5)

#Print the shape (Get the number of rows and cols)
df.shape

#Get the column names
df.columns

#Checking for duplicates and removing them
df.drop_duplicates(inplace = True)

#Show the new shape (number of rows & columns)
df.shape

#dropping the rows having any Nan/NaT values
df=pd.DataFrame(df).dropna()

#Show the number of missing (NAN, NaN, na) data for each column
df.isnull().sum()

#Need to download stopwords
nltk.download('stopwords')

def process_text(text):
    
    
    #1
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    
    #2
    clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
    
    #3
    return clean_words

#Show the Tokenization (a list of tokens )
df['text'].head().apply(process_text)

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(analyzer=process_text)
messages_bow = vectorizer.fit_transform(df['text'])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(messages_bow, df['spam'], test_size = 0.20, random_state = 0)

messages_bow.shape

#Create and train the Naive Bayes classifier
#The multinomial Naive Bayes classifier is suitable for classification with discrete features (e.g., word counts for text classification)
#from sklearn.naive_bayes import MultinomialNB
#classifier = MultinomialNB().fit(X_train, y_train)

#training the model using logistic regression
'''from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression().fit(X_train,y_train)'''

#training the model using linear regression
'''from sklearn.linear_model import LinearRegression
classifier = LinearRegression().fit(X_train, y_train)'''

#training the model using SVM
'''from sklearn import svm
classifier = svm.SVC().fit(X_train, y_train)'''

#training the model using decision tree
from sklearn import tree
classifier = tree.DecisionTreeClassifier().fit(X_train, y_train)

print(classifier.predict(X_train))

#Print the actual values
print(y_train.values)

#Evaluate the model on the training data set
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score
pred = classifier.predict(X_train)
print(classification_report(y_train ,pred ))
print('Confusion Matrix: \n',confusion_matrix(y_train,pred))
print()
print('Accuracy: ', accuracy_score(y_train,pred))

#Print the predictions
print('Predicted value: ',classifier.predict(X_test))

#Print Actual Label
print('Actual value: ',y_test.values)

#Evaluate the model on the test data set
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
# X_train
# df['text']
# type(messages_bow)
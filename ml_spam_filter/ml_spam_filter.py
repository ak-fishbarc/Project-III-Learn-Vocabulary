import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

from random import randint

from vocab import db
from vocab.models import VocabSet


###########################################################################
# Spam filter as found on:                                                #
# https://blog.logrocket.com/email-spam-detector-python-machine-learning/ #
# I'm using this example to learn about features of SVM for ML.           #
# In the future it could use card sets reported by users as spam or       #
# offensive material to train itself to filter out and block              #
# inappropriate card sets for clarification with the creator.             #
###########################################################################

headers = ['label', 'word']
words = []

correct = ['Good', 'Block', 'Swing', 'Ping', 'Food', 'Pot', 'Foot', 'Dock', 'Stock', 'Lock', 'Arm', 'Raw', 'Tool', 'Add']
wrong = ['adwadcz', 'fawfaw', 'sawdawda', 'gdfawfawfaw', 'aadzczsc', 'vmmadmadaw', 'sasadwa', 'ppodaowdaodma', 'padwaoadain', 'daczweet', 'aczvgh', 'awpepfo', 'ipawpwa', 'adawm']

while len(words) < 5000:
    chance = randint(0, 1)
    n = randint(0, len(correct)-1)
    chance2 = randint(0, 1)
    if chance == 1:
        words.append(['ham', correct[n]])
    if chance2 == 1:
        words.append(['spam', wrong[n]])


df = pd.DataFrame(words, columns=headers)

z = df['label']
y = df['word']

z_train, z_test, y_train, y_test = train_test_split(z, y, test_size=0.2)

cv = CountVectorizer()
features = cv.fit_transform(z_train)

model = svm.SVC()
model.fit(features, y_train)

features_test = cv.transform(z_test)
print("Accuracy: {}".format(model.score(features_test, y_test)))
print(model.score(features_test, y_test))

""" Blocked out until later

cardsets = VocabSet.query.all()
words = []

for sets in cardsets:
    collect = {}
    if 'French' in sets.name:
        classify = 'ham'
    else:
        classify = 'spam'
    collect['words'] = [sets.words, sets.words2]
    collect['label'] = [classify]

    words.append(collect)
"""
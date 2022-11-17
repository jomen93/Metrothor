import os
import time 
import numpy as np 
import re

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
stop = stopwords.words("english")

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier

import pyprind
import pickle


# functions definition to preprocessing steps
def tokenizer(text):
    """Use the regular expresipn to remove HTML and clean the text data
    and join with the emoticons. Remove stop-words and tokenize the text."""
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized

def stream_docs(path):
    """Generator function to read opinion and label in one line at once"""
    with open(path, 'r', encoding='utf-8') as csv:
        next(csv)
        for line in csv:
            text, label = line[:-3], int(line[-2])
            yield text, label
            

def get_minibatch(doc_stream, size):
    """Perform the minibatch to pass it into model"""
    docs, y = [], []
    try:
        for _ in range(size):
            text, label = next(doc_stream)
            docs.append(text)
            y.append(label)
    except StopIteration:
        return None, None
    return docs, y

    
vec = HashingVectorizer(
    decode_error="ignore",
    n_features=2**21,
    preprocessor=None,
    tokenizer=tokenizer)

# Classificator construction
clf = SGDClassifier(loss="log", random_state=11, max_iter=5)
print("Streaming docs ...")
doc_stream = stream_docs(path="movie_data.csv")

# Training step
pbar = pyprind.ProgBar(45)
classes = np.array([0,1])

print("Training the model ...")
for _ in range(45):
    X_train, y_train = get_minibatch(doc_stream, size=1000)
    if not X_train:
        break
    X_train = vec.transform(X_train)
    clf.partial_fit(X_train, y_train, classes=classes)
    pbar.update()
    
# Test the model output on the 5000 movies review
X_test, y_test = get_minibatch(doc_stream, size=5000)
X_test = vec.transform(X_test)

# Print results
print(f"Accuracy = {clf.score(X_test, y_test):.3f}")

clf = clf.partial_fit(X_test, y_test)
print("...trained!")

path_dest = "pkl_objects"
if not os.path.exists(path_dest):
    print("Creating directory for save pickling")
    os.makedirs(path_dest)

pickle.dump(stop,
    open(os.path.join(path_dest, "stopwords.pkl"),"wb"), pickle.HIGHEST_PROTOCOL)

pickle.dump(clf,
    open(os.path.join(path_dest, "classifier.pkl"), "wb"), pickle.HIGHEST_PROTOCOL)

print("Done!...")
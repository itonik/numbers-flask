# from ml import clf - use only this way!
# clf will be kinda of singleton - look at the end of the file

import pickle
import pandas as pd
import numpy as np
import cv2
from recognition_utils import reshape_to_fit

def train():
    from sklearn.decomposition import PCA
    from sklearn.svm import SVC
    from sklearn.pipeline import Pipeline # useful to tie the two together

    train = pd.read_csv('train.csv')
    target = train['label'].values
    train.drop('label', axis=1, inplace=True)
    train = train.values
    
    for i in range(len(train)):
        a = train[i].reshape(28,28).astype(np.uint8)
        a = reshape_to_fit(a)
        a = a.reshape(1,28*28)
        train[i] = a

    # setting up the components
    pca = ('pca', PCA(n_components = 100)) # I did play with the parameter
    svc = ('svc', SVC(kernel = 'poly'))

    # gluing into a pipe
    estimators = [ pca, svc ]
    clf = Pipeline(estimators)

    clf.fit(train, target)
    pickle.dump(clf, open("clf.p", "wb"))
    return clf

def load():
    return pickle.load(open("clf.p", "rb"))

try:
    clf = pickle.load(open("clf.p", "rb"))
except IOError:
    clf = train()
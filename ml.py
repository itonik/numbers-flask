# from ml import clf - use only this way!
# clf will be kinda of singleton

import pickle
import pandas as pd
import numpy as np
import cv2

def del_null_rows(im, bg_col = 255):
    null_row = [np.all(im[i,:] == bg_col) for i in range(im.shape[0])]
    if False in null_row:
        not_null_row_arg = null_row.index(False)
    else:
        not_null_row_arg = 0
    if False in list(reversed(null_row)):
        not_null_row_arg_end = list(reversed(null_row)).index(False)
        if not_null_row_arg_end == 0:
            not_null_row_arg_end = 1
    else:
        not_null_row_arg_end = 1
    im = im[not_null_row_arg:-not_null_row_arg_end,:]
    return im

def del_null_cols(im, bg_col = 255):
    null_col = [np.all(im[:,i] == bg_col) for i in range(im.shape[1])]   
    if False in null_col:
        not_null_col_arg = null_col.index(False)
    else:
        not_null_col_arg = 0
    if False in list(reversed(null_col)):
        not_null_col_arg_end = list(reversed(null_col)).index(False)
        if not_null_col_arg_end == 0:
            not_null_col_arg_end = 1
    else:
        not_null_col_arg_end = 1
    im = im[:,not_null_col_arg:-not_null_col_arg_end]
    return im

def to_mnist(im):
    if 255 in im:
        im[im == 0] = 1
        im[im == 255] = 0
    im = del_null_cols(im,0)
    im = del_null_rows(im,0)
    if im.shape[0]>im.shape[1]:
        n = im.shape[0] - im.shape[1]
        field = np.zeros((im.shape[0], int(n/2)))
        im = np.concatenate((field, im, field), axis=1)
        if im.shape[0]!= im.shape[1]:
            im = np.concatenate((im, np.zeros((im.shape[0], 1))), axis=1)
    else: 
        n = im.shape[1] - im.shape[0]
        field = np.zeros((int(n/2),im.shape[1]))
        im = np.concatenate((field, im, field), axis=0)
        if im.shape[0]!= im.shape[1]:
            im = np.concatenate((im, np.zeros((1,im.shape[1]))), axis=0)
    im = cv2.resize(im, (28,28))
    return im

try:
    clf = pickle.load(open("clf.p", "rb"))
except IOError:
    from sklearn.decomposition import PCA
    from sklearn.svm import SVC
    from sklearn.pipeline import Pipeline # useful to tie the two together

    train = pd.read_csv('train.csv')
    target = train['label'].values
    train.drop('label', axis=1, inplace=True)
    train = train.values
    for i in range(len(train)):
        a = train[i].reshape(28,28)
        a = del_null_rows(a,0)
        a = del_null_cols(a,0)
        a = to_mnist(a)
        a = a.reshape(1,784)
        train[i] = a

    # setting up the components
    pca = ('pca', PCA(n_components = 50)) # I did play with the parameter
    svc = ('svc', SVC(kernel = 'poly'))

    # gluing into a pipe
    estimators = [
        pca,
        svc
    ]

    clf = Pipeline(estimators)

    clf.fit(train, target)
    pickle.dump(clf, open("clf.p", "wb"))
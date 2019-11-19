import cv2
import numpy as np

# Shared code between recognition and ml package

def reshape_to_fit(image):
    f = cv2.findNonZero(image.astype(np.uint8))
    x, y, w, h = cv2.boundingRect(f)
    image = image[y:y+h, x:x+w]
    if w > h:
        image = cv2.resize(image, (28, int(28 * image.shape[0]/image.shape[1])))
        empty_t = int(np.floor((float(28) - image.shape[0]) / 2))
        new_image = np.zeros((28,28), dtype=np.uint8)
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                new_image[empty_t+y,x] = image[y,x]
        return new_image
    else:
        #print(image.shape, (int(28*image.shape[1]/image.shape[0]), 28))
        image = cv2.resize(image, (int(28*image.shape[1]/image.shape[0]), 28))
        empty_l = int(np.floor((float(28) - image.shape[1]) / 2))
        new_image = np.zeros((28,28), dtype=np.uint8)
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                new_image[y,empty_l+x] = image[y,x]
        return new_image
    return image

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
    ii = np.int8(((im.copy()+1) * 255))
    cv2.imwrite('gg.png', ii)
    return im
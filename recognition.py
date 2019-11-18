import cv2
import numpy as np
from ml import clf

def _backround_stats(image):
    top = np.min(image[0][:])
    bottom = np.min(image[-1][:])
    left = np.min(image[:][0])
    right = np.min(image[:][-1])
    return np.min([top, bottom, left, right])

def _contour_filter(contour):
    x, y, w, h = cv2.boundingRect(contour)
    if w * h < 20:
        return False
    else:
        return True

def filter(src_path, dst_path):
    # Read
    image = cv2.imread(src_path)
    # Resize to 1024 in width
    print(src_path)
    image = cv2.resize(image, (1024, int(1024 * image.shape[0]/image.shape[1])))
    # RGB -> GRAY
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Threshold
    image = cv2.GaussianBlur(image,(3,3),0)
    # Minimal brightness on edge
    m = _backround_stats(image)
    ret, image = cv2.threshold(image, m-15, 255, cv2.THRESH_BINARY)
    # Kernel for dilation and erosion
    # kernel = np.ones((7,7), np.float) / 3
    # Dilate
    #image = cv2.dilate(image, kernel, iterations=1)
    # Erode
    #image = cv2.erode(image, kernel, iterations=1)
    # Save
    cv2.imwrite(dst_path, image)

def _to_mnist(im):
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

def segment(src_path, contour_dst_path, segments_dst_path_builder):
    # Read
    image = cv2.imread(src_path)
    contours_image = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Contour
    working_image = (255-image.copy()) # cv2.findContours needs white objects on black background
    contours, hierarchy = cv2.findContours(working_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if _contour_filter(c)]
    # contours_image - image for demonstration
    contours_image = cv2.drawContours(contours_image, contours, -1, (0,255,0), 2, cv2.LINE_AA, hierarchy, 1)
    segments = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(contours_image, (x,y), (x+w,y+h), (0,0,255), 2)
        segments.append(image[y:y+h, x:x+w].copy())
    cv2.imwrite(contour_dst_path, contours_image)
    for (s, path) in zip(segments, segments_dst_path_builder(len(segments))):
        cv2.imwrite(path, s)

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

#def _number_recognition(src_path):
#    image = cv2.imread(src_path)
#    image = (255-image)

def numbers_recognition(src_paths):
    imgs = []
    for path in src_paths:
        imgs.append(_to_mnist(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)))
    test = np.zeros(shape=(len(imgs),784))
    for i, num in enumerate(imgs):
        num = np.reshape(num,784)
        test[i] = num * 255
        results = clf.predict(test)
    return results

        
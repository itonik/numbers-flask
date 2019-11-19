import cv2
import numpy as np
from ml import clf
from recognition_utils import del_null_cols, del_null_rows, to_mnist, reshape_to_fit

def _backround_stats(image):
    top = np.min(image[0][:])
    bottom = np.min(image[-1][:])
    left = np.min(image[:][0])
    right = np.min(image[:][-1])
    return np.min([top, bottom, left, right])

def _contour_filter(contour):
    x, y, w, h = cv2.boundingRect(contour)
    if w < 20 or h < 20:
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
    # image = cv2.dilate(image, kernel, iterations=1)
    # Erode
    # image = cv2.erode(image, kernel, iterations=1)
    # Save
    cv2.imwrite(dst_path, image)

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
    print(hierarchy)
    try:
        contours_image = cv2.drawContours(contours_image, contours, -1, (0,255,0), 2, cv2.LINE_AA, hierarchy, 1)
    except Exception:
        pass
    segments = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(contours_image, (x,y), (x+w,y+h), (0,0,255), 2)
        segments.append(image[y:y+h, x:x+w].copy())
    cv2.imwrite(contour_dst_path, contours_image)
    for (s, path) in zip(segments, segments_dst_path_builder(len(segments))):
        cv2.imwrite(path, s)

def numbers_recognition(src_paths):
    imgs = []
    #flatten = (lambda x: (reshape_to_fit(i)-255).reshape(1,28*28))
    imgs = np.zeros(shape=(len(src_paths),784))
    for i, path in enumerate(src_paths):
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) - 255
        img = reshape_to_fit(img)
        img = img.reshape(1,28*28)
        imgs[i] = img * 255 # WTF? Doesn`t work without it 
    #test = np.zeros(shape=(len(imgs),784))
    #test = np.array([])
    results = clf.predict(imgs)
    return results
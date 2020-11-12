import cv2
from PIL import Image
import matplotlib.pyplot as plt
from .align_images import align_images
from collections import namedtuple
import pytesseract
import numpy as np

def mark_region(invoice_img , template):
    
    #im = cv2.imread(image_path)
    im = invoice_img
    print("[INFO] loading images...")
    template = template
    #template = np.array(pages[1])[:2000,:,:]
    # align the images
    print("[INFO] aligning images...")
    im = align_images(im, template)

    image = np.copy(im)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    line_items_coordinates = []
    for c in cnts:
       
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        if y >= 20 and x <= 2000:
            if area > 100:
                line_items_coordinates.append([(x,y), (x+w, y+h)])

        if y >= 2400 and x<= 2000:
            line_items_coordinates.append([(x,y), (x+w , y+h)])

    out_index = None
    for i in range(len(line_items_coordinates)):

        # get co-ordinates to crop the image
        c = line_items_coordinates[i]
        # cropping image img = image[y0:y1, x0:x1]
        img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]    


        # convert the image to black and white for better OCR
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        edges = cv2.Canny(rgb,150,250)
        #ret,thresh1 = cv2.threshold(rgb,100,255,cv2.THRESH_BINARY)
        edges =np.concatenate([ edges[:,:,np.newaxis] for i in range(3)], axis=-1)
        dst = cv2.addWeighted(rgb,0.8,edges,0.2,0)

        #ret,thresh1 = cv2.threshold(img,100,255,cv2.THRESH_BINARY)

        # pytesseract image to string to get results
        text = str(pytesseract.image_to_string(dst , config='--psm 6 --oem 3  -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz'))

        if (any(map(lambda word: word in text, ["PREVIOUS BALANCE","PREVIOUS","NEW CHARGES" ]))):
            out_index = i

    return out_index , line_items_coordinates




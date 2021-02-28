import numpy as np
import cv2
import pickle

def textDisplay(curve,img):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, str(curve), ((img.shape[1]//2)-30, 40), font, 1, (255, 255, 0), 2, cv2.LINE_AA)
    directionText=' No lane '
    if curve > 10:
        directionText='Right'
    elif curve < -10:
        directionText='Left'
    elif curve <10 and curve > -10:
        directionText='Straight'
    elif curve == -1000000:
        directionText = 'No Lane Found'
    cv2.putText(img, directionText, ((img.shape[1]//2)-35,(img.shape[0])-20 ), font, 1, (0, 200, 200), 2, cv2.LINE_AA)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def drawLines(img,lane_curve):
    myWidth = img.shape[1]
    myHeight = img.shape[0]
    print(myWidth,myHeight)
    for x in range(-30, 30):
        w = myWidth // 20
        cv2.line(img, (w * x + int(lane_curve // 100), myHeight - 30),
                 (w * x + int(lane_curve // 100), myHeight), (0, 0, 255), 2)
    cv2.line(img, (int(lane_curve // 100) + myWidth // 2, myHeight - 30),
             (int(lane_curve // 100) + myWidth // 2, myHeight), (0, 255, 0), 3)
    cv2.line(img, (myWidth // 2, myHeight - 50), (myWidth // 2, myHeight), (0, 255, 255), 2)

    return img
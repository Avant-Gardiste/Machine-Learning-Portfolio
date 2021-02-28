import numpy as np
import cv2
import draw
import preprocessing

cameraFeed= False
videoPath = 'project_video.mp4'
cameraNo= 1
frameWidth= 520
frameHeight = 360

if cameraFeed:intialTracbarVals = [24,55,12,100] #  #wT,hT,wB,hB
else:intialTracbarVals = [42,63,14,87]   #wT,hT,wB,hB

if cameraFeed:
    cap = cv2.VideoCapture(cameraNo)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
else:
    cap = cv2.VideoCapture(videoPath)
count=0
noOfArrayValues =10
global arrayCurve, arrayCounter
arrayCounter=0
arrayCurve = np.zeros([noOfArrayValues])
myVals=[]
preprocessing.initializeTrackbars(intialTracbarVals)

while True:

    success, img = cap.read()
    if cameraFeed== False:img = cv2.resize(img, (frameWidth, frameHeight), None) 
    
    imgWarpPoints = img.copy()
    imgFinal = img.copy()
    imgCanny = img.copy()

    imgUndis = preprocessing.undistort(img)
    imgThres,imgCanny,imgColor = preprocessing.thresholding(imgUndis)
    src = preprocessing.valTrackbars()
    imgWarp = preprocessing.perspective_warp(imgThres, dst_size=(frameWidth, frameHeight), src=src)
    imgWarpPoints = preprocessing.drawPoints(imgWarpPoints, src)
    imgSliding, curves, lanes, ploty = preprocessing.sliding_window(imgWarp, draw_windows=True)

    try:
        curverad = preprocessing.get_curve(imgFinal, curves[0], curves[1])
        lane_curve = np.mean([curverad[0], curverad[1]])
        imgFinal = preprocessing.draw_lanes(img, curves[0], curves[1],frameWidth,frameHeight,src=src)

        #Average
        currentCurve = lane_curve // 50
        if  int(np.sum(arrayCurve)) == 0:averageCurve = currentCurve
        else:
            averageCurve = np.sum(arrayCurve) // arrayCurve.shape[0]
        if abs(averageCurve-currentCurve) >200: arrayCurve[arrayCounter] = averageCurve
        else :arrayCurve[arrayCounter] = currentCurve
        arrayCounter +=1
        if arrayCounter >=noOfArrayValues : arrayCounter=0
        cv2.putText(imgFinal, str(int(averageCurve)), (frameWidth//2-70, 70), cv2.FONT_HERSHEY_DUPLEX, 1.75, (0, 0, 255), 2, cv2.LINE_AA)

    except:
        lane_curve=00
        pass

    imgFinal= draw.drawLines(imgFinal,lane_curve)


    imgThres = cv2.cvtColor(imgThres,cv2.COLOR_GRAY2BGR)
    imgBlank = np.zeros_like(img)
    imgStacked = draw.stackImages(0.7, ([img,imgUndis,imgWarpPoints],
                                         [imgColor, imgCanny, imgThres],
                                         [imgWarp,imgSliding,imgFinal]
                                         ))

    cv2.imshow("Pipeline",imgStacked)
    cv2.imshow("Final Result", imgFinal)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
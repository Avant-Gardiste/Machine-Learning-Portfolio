import cv2
import numpy as np
from time import sleep

min_width = 80 # Minimum width of the rectangle
min_height = 80 # Minimum height of the rectangle
offset = 6 # Errors allowed between pixels  

line_pos = 550 # Counting Line Position 

delay= 60 # FPS of the video

detect = []
cars = 0
	
def center_handle(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture('video.mp4')
subtract = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret , frame1 = cap.read()
    temp = float(1/delay)
    sleep(temp) 
    gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),5)
    img_sub = subtract.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
    dilated = cv2.morphologyEx (dilated, cv2. MORPH_CLOSE , kernel)
    contour ,h = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame1, (25, line_pos), (1200, line_pos), (255,0,0), 2) 
    for(i,c) in enumerate(contour):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_contour = (w >= min_width) and (h >= min_height)
        if not validate_contour:
            continue

        # Draw a box around the car
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(10,255,40), 1)   
        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0,255), -2)

        for (x,y) in detect:
            if y < (line_pos + offset) and y > (line_pos - offset):
                cars += 1
                cv2.line(frame1, (25, line_pos), (1200, line_pos), (0,0,255), 2)  
                detect.remove((x,y))
                print("Car detected : " + str(cars))        
       
    # Display vehicle count
    cv2.putText(frame1, "Vehicles : "+str(cars), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),3)
    # Display the resulting image
    cv2.imshow("Final Video" , frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()
cap.release()

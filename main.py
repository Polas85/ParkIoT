import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture('http://192.168.3.3:8080/video')

def checkParkingSpace(imgPro):

    spaceCounter = 0

    for pos in posList:
        x,y= pos

        imgCrop=imgPro[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)

        if count <900:
            color =(0,255,0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))


with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 700, 300

while True:
    _, frame = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    Gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    Blur = cv2.GaussianBlur(Gray, (3, 3), 1)
    Threshold =cv2.adaptiveThreshold(Blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    Median = cv2.medianBlur(Threshold,5)
    kernel = np.ones((3,3),np.uint8)
    Dilate = cv2.dilate(Median,kernel, iterations=1)

    checkParkingSpace(Dilate )
    #for pos in posList:
    cv2.imshow("Image",img)
    #cv2.imshow("ImageBlur",imgBlur)
    #cv2.imshow("ImageThres",imgThreshold)

    cv2.waitKey(10)

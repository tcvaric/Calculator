import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import numpy as np
import math

width, height = 1280, 720

class Button:
    def __init__(self, pos, width, height, value):

        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (225, 255, 255), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (255, 191, 0), 3)

        cv2.putText(img, self.value, (self.pos[0] + 38, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (225, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (255, 191, 0), 3)

            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 75), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)
            return True
        else:
            return False


cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detector = HandDetector(detectionCon=0.8, maxHands=1)

#creating Buttons
buttonListValues = [['AC', '**', '%', '/', ''],
                    ['7', '8', '9', '*', ''],
                    ['4', '5', '6', '-', ''],
                    ['1', '2', '3', '+', ''],
                    ['0', '00', '.', '=', '']]

buttonList = []
for x in range(5):
    for y in range(5):
        xpos = x * 100 + 600
        ypos = y * 100 + 100
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

#Variables
myEquation = ''
delayCounter = 0

while True:
    #Get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #Detection Hand
    hands, img = detector.findHands(img, flipType=False)

    #Draw all buttons
    cv2.rectangle(img, (600, 20), (600 + 500, 70 + 100),
                  (225, 255, 255), cv2.FILLED)
    cv2.rectangle(img, (600, 20), (600 + 500, 70 + 100),
                  (255, 191, 0), 3)

    for button in buttonList:
        button.draw(img)

    #Check for Hand
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        x, y = lmList[8]
        if length < 50:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    myValue = buttonListValues[int(i % 5)][int(i / 5)]
                    if myValue == "=":
                        myEquation = str(eval(myEquation))
                    elif myValue == "AC":
                        myEquation = ''
                    elif myValue == "%":
                        myEquation = str(eval(myEquation)/100)
                    else:
                        myEquation += myValue
                    delayCounter = 1

    #Avoid Duplicates
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0


    #Display Equation
    cv2.putText(img, myEquation, (610, 85), cv2.FONT_HERSHEY_PLAIN,
                3, (50, 50, 50), 3)


    #Display Image
    cv2.imshow("Calculator", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
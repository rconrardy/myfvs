import copy
import cv2
import os

def haarFaceDetectSetup(self):
    haarcascades = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cascade'))
    self.models['haarFace'] = cv2.CascadeClassifier(haarcascades + "\\haarcascade_frontalface_default.xml")
    self.models['haarEye'] = cv2.CascadeClassifier(haarcascades + "\\haarcascade_eye.xml")
    print(haarcascades)

def haarFaceDetectFunction(self, original):
    copyFrame = copy.deepcopy(self.frames['curr'])
    grayImage = cv2.cvtColor(copyFrame, cv2.COLOR_BGR2GRAY)
    faces = self.models['haarFace'].detectMultiScale(grayImage, 1.1, 2)
    for (x, y, w, h) in faces:
        self.frames['curr'] = cv2.rectangle(self.frames['curr'], (x,y), (x+w,y+h), (255,0,0), 2)
    print(faces)
    cv2.imshow(str(self.ratio), self.frames['curr'])



    # copyFrame = copy.deepcopy(original)
    # grayImage = cv2.cvtColor(copyFrame, cv2.COLOR_BGR2GRAY)
    # faces = self.models['haarFace'].detectMultiScale(grayImage, 1.3, 5)
    # for (x, y, w, h) in faces:
    #     original = cv2.rectangle(original, (x,y), (x+w,y+h), (255,0,0), 2)
    # cv2.imshow(str(self.ratio), original)

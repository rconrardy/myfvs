import fvs
import time
import cv2




myfvs = fvs.System()

myfvs[0] = fvs.Device(0)
myfvs[0][0] = fvs.Vision(ratio=6, size=64, resize="area")
myfvs[0][1] = fvs.Vision(ratio=4, size=64, resize="area")
myfvs[0][2] = fvs.Vision(ratio=2, size=64, resize="area")
myfvs[0][3] = fvs.Vision(ratio=1, size=64, resize="area")

myfvs.update()


# def setup(self):
#     haarcascades = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fvs\\cascade'))
#     self.models['haarFace'] = cv2.CascadeClassifier(haarcascades + "\\haarcascade_frontalface_default.xml")
#     self.models['haarEye'] = cv2.CascadeClassifier(haarcascades + "\\haarcascade_eye.xml")
# def detectfaces(self, original):
#     # copyFrame = copy.deepcopy(self.frames['curr'])
#     # grayImage = cv2.cvtColor(copyFrame, cv2.COLOR_BGR2GRAY)
#     # faces = self.models['haarFace'].detectMultiScale(grayImage, 1.3, 5)
#     # for (x, y, w, h) in faces:
#     #     self.frames['curr'] = cv2.rectangle(self.frames['curr'], (x,y), (x+w,y+h), (255,0,0), 2)
#     # cv2.imshow(str(self.ratio), self.frames['curr'])
#     copyFrame = copy.deepcopy(original)
#     grayImage = cv2.cvtColor(copyFrame, cv2.COLOR_BGR2GRAY)
#     faces = self.models['haarFace'].detectMultiScale(grayImage, 1.3, 5)
#     for (x, y, w, h) in faces:
#         original = cv2.rectangle(original, (x,y), (x+w,y+h), (255,0,0), 2)
#     cv2.imshow(str(self.ratio), original)

setup = fvs.haarFaceDetectSetup
funct = fvs.haarFaceDetectFunction

myfvs[0][0].function(setup, funct)
myfvs[0][1].function(setup, funct)
myfvs[0][2].function(setup, funct)
myfvs[0][3].function(setup, funct)

# myfvs[1] = fvs.Device(1)
# myfvs[1][0] = fvs.Vision(ratio=8, size=32, resize="random")
# myfvs[1][1] = fvs.Vision(ratio=4, size=32, resize="random")
# myfvs[1][2] = fvs.Vision(ratio=2, size=32, resize="random")
# myfvs[1][3] = fvs.Vision(ratio=1, size=32, resize="random")

# myfvs[0] = fvs.Device(0)
# myfvs[0][0] = fvs.Region(ratio=1/2, size=32, resize="cubic")
# myfvs[0][1] = fvs.Region(ratio=1/4, size=32, resize="cubic")
# myfvs[0][2] = fvs.Region(ratio=1/8, size=32, resize="cubic")
# myfvs[0][3] = fvs.Region(ratio=1/16, size=32, resize="cubic")

# myfvs[1] = fvs.Device(1)
# myfvs[1][0] = fvs.Region(ratio=1/2, size=32, resize="linear")
# myfvs[1][1] = fvs.Region(ratio=1/4, size=32, resize="linear")
# myfvs[1][2] = fvs.Region(ratio=1/8, size=32, resize="linear")
# myfvs[1][3] = fvs.Region(ratio=1/16, size=32, resize="linear")

# fps = fvs.fps()
# fps.start()
# while True:
#     myfvs.update()
#     fps.update()
#     print(fps.fps())

myapp = fvs.Application(myfvs)
myapp.mainloop()

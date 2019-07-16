import PIL.Image, PIL.ImageTk
import tkinter
import math
import cv2
import fvs

from .vision import Vision
from .region import Region

class Application(tkinter.Tk):
    def __init__(self, system, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title("Foveated Vision System")
        self.configure(bg="black", width=1000, height=840)
        self.resizable(width=True, height=True)

        self._system = system

        self._appFrames = {}
        self._appOption = {}
        self._appChoice = {}
        self._appString = {}
        self._appTracer = {}
        self._appCanvas = {}
        self._pilFrames = {}

        self._appString["device"] = tkinter.StringVar(self)
        self._appChoice["device"] = [choice[0] for choice in self._system]
        self._appString["device"].set(self._appChoice["device"][0])

        self._appString["vision"] = tkinter.StringVar(self)
        self._appChoice["vision"] = [choice[0] for choice in self._system[self._appString["device"].get()]]
        self._appString["vision"].set(self._appChoice["vision"][0])

        self._appString["frame"] = tkinter.StringVar(self)
        self._appChoice["frame"] = [choice[0] for choice in self._system[self._appString["device"].get()][self._appString["vision"].get()]]
        self._appString["frame"].set(self._appChoice["frame"][0])

        self._appFrames["west"] = tkinter.Frame(self, bd=20, width=320, height=640, bg="white")
        self._appFrames["cent"] = tkinter.Frame(self, bd=20, width=150, height=640, bg="white")
        self._appFrames["east"] = tkinter.Frame(self, bd=20, width=320, height=640, bg="white")

        self.bind('<Left>', self.leftKey)
        self.bind('<Right>', self.rightKey)
        self.bind('<Up>', self.upKey)
        self.bind('<Down>', self.downKey)

        self._appFrames["west"].pack(side="left", fill="both", expand=True)
        self._appFrames["cent"].pack(side="left", fill="both", expand=True)
        self._appFrames["east"].pack(side="left", fill="both", expand=True)

        self._appCanvas["control"] = tkinter.Canvas(self._appFrames["west"], bd=-2, width=320, height=640, bg="white")
        self._appCanvas["layered"] = tkinter.Canvas(self._appFrames["east"], bd=-2, width=320, height=470, bg="white")
        self._appCanvas["stacked"] = tkinter.Canvas(self._appFrames["cent"], bd=-2, width=150, height=640, bg="white")

        self._appCanvas["control"].pack(side="left", fill="both", expand=True)
        self._appCanvas["stacked"].pack(side="left", fill="both", expand=True)
        self._appCanvas["layered"].pack(side="top", fill="x", expand=False)

        self._appCanvas["focalpt"] = tkinter.Label(self._appFrames["east"], height=2, width=30, text="sample")
        self._appCanvas["focalpt"].pack(side="top", fill="both", expand=False)


        self.fps = fvs.fps()
        self.fps.start()
        self.update()

    def update(self):
        self._system.update()
        self.fps.update()
        print(self.fps.fps())

        focalpoint = self._system[self._appString["device"].get()].focalpoint

        self._appCanvas["focalpt"].config(text=str(focalpoint))

        control = PIL.Image.new('RGBA', (320, 240), (0, 0, 0, 255))
        stacked = PIL.Image.new('RGBA', (150, 2000), (255, 255, 255, 0))
        layered = PIL.Image.new('RGBA', (320, 240), (0, 0, 0, 255))

        visionList = [(visionKey, vision) for visionKey, vision in self._system[self._appString["device"].get()]]
        boxes = []
        for i, (visionKey, vision) in enumerate(visionList):
            frameList = [frame for frameKey, frame in vision if frameKey==self._appString["frame"].get()]
            for frame in frameList:
                ratio, size = vision.ratio, vision.size
                rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                boxes.append([])
                width, height, channels = rgbFrame.shape
                imgFrame = PIL.Image.fromarray(cv2.resize(rgbFrame, (150, 150)))
                stacked.paste(imgFrame, (0, 160 * i))
                if type(vision) == Vision:
                    imgFrame = PIL.Image.fromarray(cv2.resize(rgbFrame, (int((size*ratio)//2), int((size*ratio)//2))))
                    offset = [160 - (size*ratio)//4, 120 - (size*ratio)//4]
                    layered.paste(imgFrame, (int(offset[0] + (focalpoint[0])//2), int(offset[1] - (focalpoint[1])//2)))
                else:
                    imgFrame = PIL.Image.fromarray(cv2.resize(rgbFrame, (int(240 * ratio), int(240 * ratio))))
                    offset = [160 - (120*ratio)//1, 120 - (120*ratio)//1]
                    layered.paste(imgFrame, (int(offset[0] + (focalpoint[0])//2), int(offset[1] - (focalpoint[1])//2)))

        self._pilFrames["stacked"] = PIL.ImageTk.PhotoImage(image=stacked)
        self._appCanvas["stacked"].create_image(0, 10, image=self._pilFrames["stacked"], anchor=tkinter.NW)

        self._pilFrames["layered"] = PIL.ImageTk.PhotoImage(image=layered)
        self._appCanvas["layered"].create_image(0, 225, image=self._pilFrames["layered"], anchor=tkinter.NW)

        frame = self._system[self._appString["device"].get()].original
        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        self.drawRectangles(visionList, rgbFrame, focalpoint)
        imgFrame = PIL.Image.fromarray(cv2.resize(rgbFrame, (320, 240)))
        self._pilFrames["control"] = PIL.ImageTk.PhotoImage(image=imgFrame)
        self._appCanvas["control"].create_image(0, 225, image=self._pilFrames["control"], anchor=tkinter.NW)

        self.after(15, self.update)

    def drawRectangles(self, visionList, rgbFrame, focalpoint):
        height, width, channels = rgbFrame.shape
        corrected_focalpoint = [(width//2) + focalpoint[0], (height//2) - focalpoint[1]]
        for visionTuple in visionList:
            vision = visionTuple[1]
            ratio, size = vision.ratio, vision.size

            if type(vision) == Vision:
                offset = (size//2) * ratio
            else:
                offset = int(min((width*ratio)//2, (height*ratio)//2))

            crop_x = [corrected_focalpoint[0] - offset, corrected_focalpoint[0] + offset]
            crop_y = [corrected_focalpoint[1] - offset, corrected_focalpoint[1] + offset]

            if crop_y[0] <= 0:
                crop_y[0] = 0
            elif crop_y[1] > height:
                crop_y[1] = height

            if crop_x[0] < 0:
                crop_x[0] = 0
            elif crop_x[1] > width:
                crop_x[1] = width

            cv2.rectangle(rgbFrame, (crop_x[0], crop_y[0]), (crop_x[1], crop_y[1]), (0, 225, 0), 3)

    def leftKey(self, event):
        focalpoint = self._system[self._appString["device"].get()].focalpoint
        focalpoint[0] -= 1

    def rightKey(self, event):
        focalpoint = self._system[self._appString["device"].get()].focalpoint
        focalpoint[0] += 1

    def upKey(self, event):
        focalpoint = self._system[self._appString["device"].get()].focalpoint
        focalpoint[1] += 1

    def downKey(self, event):
        focalpoint = self._system[self._appString["device"].get()].focalpoint
        focalpoint[1] -= 1

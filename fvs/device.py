import time
import cv2

class Device(cv2.VideoCapture):
    def __init__(self, index, *args, **kwargs):
        cv2.VideoCapture.__init__(self, index, *args, **kwargs)
        self.focalpoint = [0, 0]
        self.original = None
        self.visions = {}

    def __repr__(self):
        visions = ', '.join(str(key) for key in self.visions.keys())
        return '{}({})'.format(type(self), visions)

    def __len__(self):
        return len(self.visions)

    def __setitem__(self, key, val):
        self.visions[str(key)] = val

    def __getitem__(self, key):
        return self.visions[str(key)]

    def __iter__(self):
        return iter(self.visions.items())

    def update(self):
        self.original = self.read()[1]
        print(self.original.shape)
        height, width, channels = self.original.shape
        corrected_focalpoint = [(width//2) + self.focalpoint[0], (height//2) - self.focalpoint[1]]
        start = time.time()
        for vision in self.visions.values():
            vision.update(self.original, corrected_focalpoint, width, height, channels)
        print("update time:", time.time() - start)

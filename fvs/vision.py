import cv2
import fvs

class Vision():

    def __init__(self, ratio=None, size=None, resize="linear"):
        self.ratio = ratio
        self.size = size
        self.resize = resize
        self.offset = (self.size//2) * self.ratio
        self.frames = {"curr": None}

    def __repr__(self):
        frames = ', '.join(str(key) for key in self.frames.keys())
        return '{}({})'.format(type(self), frames)

    def __len__(self):
        return len(self.frames)

    def __setitem__(self, key, val):
        self.frames[str(key)] = val

    def __getitem__(self, key):
        return self.frames[str(key)]

    def __iter__(self):
        return iter(self.frames.items())

    def update(self, original, focalpoint, width, height, channels):
        frame = original[
            focalpoint[1]-self.offset:focalpoint[1]+self.offset,
            focalpoint[0]-self.offset:focalpoint[0]+self.offset]
        self.frames["curr"] = fvs.resize(frame, (self.size, self.size), self.resize)
        return self.frames["curr"]

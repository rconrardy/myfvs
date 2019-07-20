import numpy
import time
import cv2

def resize(frame, size, type):
    if type=="linear":
        frame = cv2.resize(frame, size, interpolation=cv2.INTER_LINEAR)
    elif type=="nearest":
        frame = cv2.resize(frame, size, interpolation=cv2.INTER_NEAREST)
    elif type=="area":
        frame = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    elif type=="cubic":
        frame = cv2.resize(frame, size, interpolation=cv2.INTER_CUBIC)
    elif type=="lanczos":
        frame = cv2.resize(frame, size, interpolation=cv2.INTER_LANCZOS4)
    elif type=="subsampling":
        frame = subsampling(frame, size)
    return frame

def subsampling(frame, size):
    height, width, channels = frame.shape
    count = numpy.array([height / size[0], width / size[1]])
    ret_rows = numpy.array([0, count[0]])
    new_frame = numpy.zeros((size[0], size[1], 3), dtype=numpy.uint8)
    for row in range(size[0]):
        ret_cols = numpy.array([0, count[1]])
        for col in range(size[1]):
            x = numpy.random.randint(ret_cols[0], ret_cols[1])
            y = numpy.random.randint(ret_rows[0], ret_rows[1])
            ret_cols += count[1]
            new_frame[row, col] = frame[y, x, :]
        ret_rows += count[0]
    return new_frame

class fps:
    def __init__(self):
        self.start_time = None
        self.curr_time = None
        self.num_frames = 0

    def start(self):
        self.start_time = time.time()

    def update(self):
        self.curr_time = time.time()
        self.num_frames += 1

    def elapsed(self):
        return self.curr_time - self.start_time

    def fps(self):
        return self.num_frames / self.elapsed()

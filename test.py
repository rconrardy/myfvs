import fvs
import time
import cv2

myfvs = fvs.System()

myfvs[1] = fvs.Device(1)
myfvs[1][0] = fvs.Vision(ratio=8, size=32, resize="area")
myfvs[1][1] = fvs.Vision(ratio=4, size=32, resize="area")
myfvs[1][2] = fvs.Vision(ratio=2, size=32, resize="area")
myfvs[1][3] = fvs.Vision(ratio=1, size=32, resize="area")

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

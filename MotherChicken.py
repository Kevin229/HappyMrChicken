# Build class for mother chicken (hen)
import time
import random
import _thread


class MotherChicken:
    def __init__(self,
                 icon_up_path,
                 icon_down_path,
                 icon_width,
                 icon_height,
                 pos_width,
                 pos_height
                 ):
        self.mIconUpPath = str(icon_up_path)
        self.mIconDownPath = str(icon_down_path)
        self.mIconWidth = int(icon_width)
        self.mIconHeight = int(icon_height)
        self.mPosWidth = int(pos_width)
        self.mPosHeight = int(pos_height)
        self.mStart = False
        # self.build_Icon()
        pass

    def build_Icon(self):
        start_time = time.time()
        print(self.mStart)
        while self.mStart:
            y_val = self.mPosHeight
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 1:
                start_time = current_time
                self.mPosHeight = random.randrange(y_val - 20, y_val + 20)
                print(self.mPosHeight)
        pass


import cv2
import numpy as np
import random

class FrameOperator:
    def __init__(self, op_type):
        self.op_type = op_type
    
    def apply_operation(self, frame):
        if frame is not None:
            if self.op_type == "random_rotation":
                height, width = frame.shape[:2]
                angle = random.randint(0, 180)
                matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
                img = cv2.warpAffine(frame, matrix, (width,height))
            elif self.op_type == "flip":
                img = cv2.flip(frame, 1)
            elif self.op_type == "noise":
                noise = np.zeros(frame.shape, np.uint8)
                cv2.randn(noise, (0,0,0), (100,100,100))
                img = cv2.add(frame, noise)
            elif self.op_type == "grayscale":
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                raise Exception("Invalid operation.")            
            return img
        else:
            print("Frame is empty!")

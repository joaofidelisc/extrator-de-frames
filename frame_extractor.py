import cv2

class FrameExtractor:
    def __init__(self, video_path, frame_seconds_index):
        self.video_path = video_path
        self.frame_seconds_index = frame_seconds_index

        
    def extract_frame(self):
        video = cv2.VideoCapture(self.video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        duration_sec = (int(video.get(cv2.CAP_PROP_FRAME_COUNT)))/fps
        if (self.frame_seconds_index >= duration_sec):
           self.frame_seconds_index = duration_sec-1
        video.set(cv2.CAP_PROP_POS_MSEC, self.frame_seconds_index * 1000)
        sucess, frame = video.read()
        if not sucess:
            print("Error while reading frame")
            return None
        return frame
       

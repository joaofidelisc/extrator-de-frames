import os
import cv2
from frame_extractor import FrameExtractor
from frame_operator import FrameOperator
from RabbitMQ.consumer_rabbitMQ import MessageConsumer
from RabbitMQ.producer_rabbitMQ import MessageProducer


class VideoProcessing:
    def __init__(self):
        self.json_path = os.path.abspath("Payload/payload.json")
        self.producer = MessageProducer('frameExtractorProperties', self.json_path)
        self.consumer = MessageConsumer('frameExtractorProperties', self)
        self.index = 1

    def start(self):
        self.producer.send_message()
        self.consumer.consume()

    def on_message_received(self, video_ref, frame_seconds_index, op_type):
        extractor = FrameExtractor(f'Videos/{video_ref}', frame_seconds_index)
        frame = extractor.extract_frame()
        list_op = op_type.split("|") 
        file_name = op_type.replace("|", "_")
        for item in list_op:
            operator = FrameOperator(f'{item}')
            frame = operator.apply_operation(frame)
        cv2.imwrite(f"Operation_Results/result_{file_name}_{self.index}.png", frame)        
        self.index += 1

if __name__ == '__main__':
    video_processing = VideoProcessing()
    video_processing.start()


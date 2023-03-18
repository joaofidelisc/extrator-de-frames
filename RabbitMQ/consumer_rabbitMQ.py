import pika
import json
from frame_extractor import FrameExtractor

class MessageConsumer:
    def __init__(self, queue_name, video_processing):
        self.connection = pika.BlockingConnection()
        self.queue_name = queue_name
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue_name)
        self.video_processing = video_processing

    def callback(self, channel, method_frame, properties, body):
        message = json.loads(body)

        video_ref = message['video_ref']
        frame_seconds_index = message['frame_seconds_index']
        op_type = message['op_type']
        
        self.video_processing.on_message_received(video_ref, frame_seconds_index, op_type)

        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def consume(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.queue_name, self.callback)
        self.channel.start_consuming()

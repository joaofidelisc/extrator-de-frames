import pika
import json


class MessageProducer:
    def __init__(self, queue_name, json_file):
        self.queue_name = queue_name
        self.json_file = json_file
        self.credentials = pika.PlainCredentials("guest", "guest")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost",
                port="5672",
                credentials=self.credentials
            )
        )

    def send_message(self):
        with open(self.json_file) as payload:
            data = json.load(payload)

        channel = self.connection.channel()
        channel.queue_declare(queue='frameExtractorProperties')
        for obj in data:
            video_ref = obj['video_ref']
            frame_seconds_index = obj['frame_seconds_index']
            op_type = obj['op_type']
            message = {
                "video_ref": video_ref,
                "frame_seconds_index": frame_seconds_index,
                "op_type": op_type
            }
            channel.basic_publish(exchange='',
                                routing_key='frameExtractorProperties',
                                body=json.dumps(message))
            
        self.connection.close()
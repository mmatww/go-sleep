import argparse
import grpc
import json
import uuid
from datetime import datetime

import sleep_pb2_grpc
from sleep_pb2 import SleepRequest

DEFAULT_LABEL = 'test'
DEFAULT_SLEEP = '100'
DEFAULT_ADDRESS = 'localhost:7777'
DEFAULT_SSL = True


def run(address, label, sleep, ssl):
    channel = grpc.insecure_channel(address)
    if ssl:
        channel = grpc.secure_channel(
            address, grpc.ssl_channel_credentials())
    stub = sleep_pb2_grpc.GoSleepStub(channel)
    while True:
        timestamp = datetime.utcnow().ctime()
        id = str(uuid.uuid4())
        print(json.dumps({"request": {"id": id, "label": label, "sleep": sleep, "timestamp": timestamp}}))
        response = stub.Sleep(SleepRequest(label=label, sleep=sleep), metadata=[
                              ('x-request-id', id)])
        if response.timestamp:
            print(json.dumps({"response": {"id": response.id, "label": response.label, "sleep": response.sleep, "timestamp": response.timestamp}}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', default=DEFAULT_ADDRESS)
    parser.add_argument('--label', default=DEFAULT_LABEL)
    parser.add_argument('--sleep', default=DEFAULT_SLEEP, type=int)
    parser.add_argument('--ssl', default=DEFAULT_SSL, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    run(**vars(args))

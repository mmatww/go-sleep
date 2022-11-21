import argparse
import grpc
import json
import os
import random
import sys
import time
import uuid
from datetime import datetime

import sleep_pb2_grpc
from sleep_pb2 import SleepRequest

DEFAULT_CONFIG = {
    "label": "test",
    "endpoints": [
        { 
            "label": "local",
            "address": "localhost:7777",
            "ssl": False
        }
    ],
    "sleep": {
        "min": 0,
        "max": 100
    },
    "pause": 0.0,
    "requests": 1
}

def run(**kwargs):
    request_max = kwargs.get("requests", DEFAULT_CONFIG["requests"])
    endpoints = kwargs.get("endpoints", DEFAULT_CONFIG["endpoints"])
    label = kwargs.get("label", DEFAULT_CONFIG["label"])
    sleep_min = max(0, kwargs.get("sleep", DEFAULT_CONFIG["sleep"]).get("min", DEFAULT_CONFIG["sleep"]["min"]))
    sleep_max = max(sleep_min, kwargs.get("sleep", DEFAULT_CONFIG["sleep"]).get("max", DEFAULT_CONFIG["sleep"]["max"]))
    pause = kwargs.get("pause", DEFAULT_CONFIG["pause"])
    for endpoint in endpoints:
        if endpoint.get("ssl", True):
            endpoint["channel"] = grpc.secure_channel(endpoint["address"], grpc.ssl_channel_credentials())
        else:
            endpoint["channel"] = grpc.insecure_channel(endpoint["address"])
        endpoint["stub"] = sleep_pb2_grpc.GoSleepStub(endpoint["channel"])
        if not endpoint.get("label"):
            endpoint["label"] = endpoint["address"].replace(":", "-")
    request_count = 0
    while request_max == 0 or request_count < request_max:
        make_request(endpoints, label, request_count, random.randint(sleep_min, sleep_max))
        request_count += 1
        if pause > 0:
            time.sleep(pause)

def make_request(endpoints, label, counter, sleep):
    request_id = str(uuid.uuid4())
    random.shuffle(endpoints)
    for endpoint in endpoints:
        request_label = f"{label}-{endpoint['label']}"
        try:
            start_stamp = datetime.now()
            response = endpoint["stub"].Sleep(SleepRequest(label=request_label, sleep=sleep), metadata=[("x-request-id", request_id)])
        except grpc.RpcError as err:
            status = str(err.code()).replace("StatusCode.", "")
        else:
            status = "OK"
        finally:
            end_stamp = datetime.now()
            total_time_ms = int((end_stamp - start_stamp).total_seconds() * 1000)
            print(json.dumps({
                "id": request_id,
                "counter": counter,
                "label": request_label,
                "sleep_ms": sleep,
                "total_ms": total_time_ms,
                "net_ms": total_time_ms - sleep,
                "start_time": str(start_stamp),
                "end_time": str(end_stamp),
                "response_status": status,
            }), file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-path", default=os.getenv("CONFIG_PATH"))
    args = parser.parse_args()
    config = DEFAULT_CONFIG
    if args.config_path:
        with open(args.config_path) as ff:
            config = json.load(ff)
    run(**config)

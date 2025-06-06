# This is runpod_wrapper.py file
import runpod
from typing import Any, Literal, TypedDict
import requests
import sys

class HandlerInput(TypedDict):
    method_name: Literal["generate"]
    input: Any


class HandlerJob(TypedDict):
    input: HandlerInput


def handler(job: HandlerJob):
    base_url = "http://0.0.0.0:11434"
    input = job["input"]

    # Streaming is not supported in serverless mode
    input["input"]["stream"] = False
    # Get the model name from arguements
    model = sys.argv[1]
    input["input"]["model"] = model

    response = requests.post(
        url=f"{base_url}/api/{input['method_name']}/",
        headers={"Content-Type": "application/json"},
        json=input["input"],
    )
    response.encoding = "utf-8"

    return response.json()


runpod.serverless.start({"handler": handler})

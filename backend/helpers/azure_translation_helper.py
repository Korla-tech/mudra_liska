import json
import requests
import uuid

with open("key.json") as f:
    key = json.load(f)["translate_key"]

endpoint = "https://api.cognitive.microsofttranslator.com"

location = "germanywestcentral"

path = '/translate'
constructed_url = endpoint + path


def translate(direction: str, text: str):

    params = {
        'api-version': '3.0',
        'from': direction.split("_")[0],
        'to': direction.split("_")[1]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': text
    }]

    request = requests.post(
        constructed_url, params=params, headers=headers, json=body)
    return request.json()[0]["translations"][0]["text"]

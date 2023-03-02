import requests


def translate(text, direction) -> str:
    r = requests.post("https://sotra.app/?uri=/ws/translate/&_version=2.0.24", json={
                      "direction": direction, "warnings": False, "translationtype": "lsf", "text": text})
    return r.json()["output_text"].replace("¶", " ").replace("┊", " ")

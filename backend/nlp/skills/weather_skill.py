from nlp.skills.base_skills import Skill
import requests
from datetime import datetime, timedelta

lat = 51.237190
lon = 14.196007


def get_forecast():
    r = requests.get(
        f"https://api.brightsky.dev/weather?date={datetime.now() + timedelta(days=1)}&last_date={datetime.now() + timedelta(days=1)}&lat={lat}&lon={lon}&tz=Europe%2FBerlin")
    print(r.json())


get_forecast()


class Wheater_skill(Skill):
    def __init__(self, pattern) -> None:
        super().__init__(pattern)

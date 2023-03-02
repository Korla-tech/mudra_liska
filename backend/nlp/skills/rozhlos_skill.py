from nlp.skills.base_skills import Skill
import subprocess
import helpers.bamorak
import threading


class Rozhlos_skill(Skill):
    def __init__(self, pattern) -> None:
        def misc():
            global p
            helpers.bamorak.play_sync("raju serbski rozhłos.")
            p = subprocess.Popen(
                "exec ffplay http://mdr-990100-0.cast.mdr.de/mdr/990100/0/mp3/high/stream.mp3 -nodisp -autoexit", shell=True, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)

        def play_rozhlos(prompt):
            x = threading.Thread(target=misc)
            x.start()
            return {
                "prompt": prompt,
                "output": "Raju serbski rozhłos."
            }

        def kill_rozhlos(prompt):
            global p
            p.kill()
            helpers.bamorak.play_async("prošu jara")
            return {
                "prompt": prompt,
                "output": "prošu jara"
            }
        super().__init__(pattern, play_rozhlos, stop_func=kill_rozhlos)

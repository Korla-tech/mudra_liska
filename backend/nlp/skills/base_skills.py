import random
from helpers import bamorak, azure_translation_helper, openaihelper, config_helper


class Skill():
    def __init__(self, pattern, func, stop_func=None) -> None:
        self.pattern = pattern
        self.func = func
        if stop_func == None:
            self.isStopable = False
            self.stop_func = lambda *args: None
        else:
            self.isStopable = True
            self.stop_func = stop_func

    def check_match(self, prompt):
        for pattern in self.pattern:
            if prompt[-1] == "." or prompt[-1] == "!" or prompt[-1] == "?":
                prompt = prompt[:-1]
            if prompt == pattern:
                return True
        else:
            return False

    def call(self, prompt) -> dict:
        if config_helper.current_skill != None:
            print("stopping old skill", config_helper.current_skill)
            config_helper.current_skill.stop(prompt)
        out = self.func(prompt)
        if self.isStopable:
            config_helper.current_skill = self
        return out

    def stop(self, prompt):
        if self.stop_func != None:
            return self.stop_func(prompt)
        else:
            return "Skill can not be stopped!"


class Simple_skill(Skill):
    def __init__(self, pattern, output) -> None:
        def call_function(prompt, output=output):
            if isinstance(output, list):
                txt = random.choice(output)
            else:
                txt = output
            bamorak.play_async(txt)
            return {
                "prompt": prompt,
                "output": txt
            }
        super().__init__(pattern, call_function)


class Stop_skill(Skill):
    def __init__(self, pattern) -> None:
        def stop(prompt):
            print(config_helper.current_skill)
            if config_helper.current_skill != None:
                if config_helper.current_skill.isStopable:
                    out = config_helper.current_skill.stop(prompt)
                    config_helper.current_skill = None
                    return out
                else:
                    bamorak.play_async("Njeda so ničo hasnyć.")
                    return {
                        "prompt": prompt,
                        "output": "Njeda so ničo hasnyć."
                    }
            else:
                bamorak.play_async("Njeda so ničo hasnyć.")
                return {
                    "prompt": prompt,
                    "output": "Njeda so ničo hasnyć."
                }
        super().__init__(pattern, stop)


class OpenAI_skill(Skill):

    def __init__(self, pattern, debug) -> None:
        def call_function(prompt, debug=debug):
            if debug:
                translated_prompt = "Who is Napoleon?"
            else:
                translated_prompt = azure_translation_helper.translate(
                    direction="hsb_en", text=prompt)
            print(f"translated promt: {translated_prompt}")
            if debug:
                generated_text = "Napoleon is big"
            else:
                generated_text = openaihelper.generate(translated_prompt)
            print(f"generated text: {generated_text}")
            if debug:
                translated_output = "Napoleon je wulki."
            else:
                translated_output = azure_translation_helper.translate(
                    direction="en_hsb", text=generated_text)
            bamorak.play_async(translated_output)
            return {
                "prompt": prompt,
                "output": translated_output
            }
        self.debug = debug
        super().__init__(pattern, call_function)

# TODO: implement error logging
import helpers.bamorak


class nothingRecognized():
    def __init__(self, details) -> None:
        self.details = details
        helpers.bamorak.synthesize("njesym ničo zhrozumił!")

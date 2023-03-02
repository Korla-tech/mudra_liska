import azure.cognitiveservices.speech as speechsdk
import json
from error_classes import nothingRecognized, recognitionCanceled, recognitionError
from helpers import improve_recognition
import type_classes
from nlp import proccesor

with open("./key.json") as f:
    key = json.load(f)

speech_config = speechsdk.SpeechConfig(
    subscription=key["mskey"], region="westeurope")
speech_config.endpoint_id = "1d604f4b-212c-4f2f-8c94-6047286c1df7"

audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config, audio_config=audio_config)

DEBUG = False


def main(inputArgs: type_classes.InputArgs) -> dict:

    def recognize_from_microphone():
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return speech_recognition_result.text
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            return nothingRecognized.nothingRecognized(speech_recognition_result.no_match_details)
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                return recognitionCanceled.recognitionCanceled(cancellation_details.error_details)
            else:
                return recognitionError.recognitionError(speech_recognition_result.cancellation_details)
    if inputArgs.inputType == "mic":
        if DEBUG:
            out = "što je napoleon?"
        else:
            out = recognize_from_microphone()
            out = improve_recognition.process_text(out)
    else:
        out = inputArgs.text
    print(f"recognized: {out}")

    return proccesor.process(text=out, debug=DEBUG)

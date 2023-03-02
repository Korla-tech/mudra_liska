import os
import random
import string
import requests
import threading
import subprocess
import sentence_splitter

BATCH_SIZE: int = 2

finished = False


def play_thread_function(wav_key):
    played_wavs = []
    wavs = wav_ids[wav_key]
    while len(played_wavs) != batch_len:
        for wav in list(set(wavs) - set(played_wavs)):
            if len(played_wavs) == 0 or wavs.index(played_wavs[-1])+1 == wavs.index(wav):
                print(f"playing: {wav}")
                subprocess.run(["ffplay", f"temp/{wav}.mp3", "-nodisp", "-autoexit"], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                played_wavs.append(wav)
            if len(played_wavs) == batch_len:
                print("break")

    global finished
    finished = True

    for wav in wavs:
        print(f"deleting: {wav}")
        os.remove(f"./temp/{wav}.mp3")


def synthesize_thread_function(sentence_batch,):
    global wav_ids
    global batch_len
    wav_key = get_random_string(20)
    wav_ids = {
        wav_key: []
    }
    batch_len = len(sentence_batch)
    play_thread = threading.Thread(
        target=play_thread_function, args=(wav_key,))
    play_thread.start()
    for batch in sentence_batch:
        wav_ids[wav_key].append(synthesize(batch))


def get_sentence_batch(text: str):
    splitter = sentence_splitter.SentenceSplitter(language="de")
    sentences = splitter.split(text)
    sentence_batch = []
    for i, sentece in enumerate(sentences):
        if i == 0 or (i+1) % BATCH_SIZE == 0:
            if BATCH_SIZE > 1:
                if i != 0:
                    sentence_batch.append(" ".join(
                        [sentece]+sentences[i+1:i+(BATCH_SIZE)]))
                else:
                    sentence_batch.append(sentece)
            else:
                sentence_batch.append(sentece)
    return sentence_batch


def play_async(text: str):
    sentence_batch = get_sentence_batch(text)
    synthesize_thread = threading.Thread(
        target=synthesize_thread_function, args=(sentence_batch,))
    synthesize_thread.start()


def play_sync(text: str):
    global finished
    finished = False
    sentence_batch = get_sentence_batch(text)
    synthesize_thread = threading.Thread(
        target=synthesize_thread_function, args=(sentence_batch,))
    synthesize_thread.start()
    while not finished:
        pass


def get_random_string(length):

    chars = string.ascii_letters + string.digits

    result_str = ''.join(random.choice(chars) for i in range(length))
    return result_str


def synthesize(text: str):
    r = requests.post("http://localhost:8080/api/tts", json={
        "speaker_id": "korlaglowtts",
        "text": text
    })
    wav_id = get_random_string(20)
    with open(f"temp/{wav_id}.mp3", "wb") as f:
        f.write(r.content)

    return wav_id

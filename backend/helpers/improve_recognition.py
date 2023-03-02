import subprocess

cz_to_hsb_chars = [
    ["á", "a"],
    ["ď", "d"],
    ["é", "e"],
    ["í", "i"],
    ["ň", "n"],
    ["ť", "t"],
    ["ú", "u"],
    ["ů", "u"],
    ["ý", "y"],
]


def check_spelling(word) -> list:
    output: str = subprocess.run(f"echo {word} | hunspell -d hsb", stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL, shell=True).stdout.decode("utf-8")
    output = output.splitlines()[1]
    print(output)
    if output[0] != "&":
        return [word, True]
    else:
        correction_start: int = output.find(":")
        correction_end: int = output.find(",")
        return [output[correction_start+2:correction_end], False]


def process_text(text: str):
    text = text.lower()
    for chars in cz_to_hsb_chars:
        text = text.replace(chars[0], chars[1])
    words = text.split(" ")
    print(words)
    corrected_words = []
    for word in words:
        corrected_word = check_spelling(word)
        if not corrected_word[1]:
            if check_spelling(word.capitalize())[1]:
                corrected_word = check_spelling(word.capitalize())
        corrected_words.append(corrected_word[0])

    return " ".join(corrected_words)

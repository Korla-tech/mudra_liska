from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sorbian_to_german_chars = [
    ["ć", "c"],
    ["č", "c"],
    ["ě", "e"],
    ["ń", "n"],
    ["ł", "l"],
    ["ó", "o"],
    ["ř", "r"],
    ["š", "s"],
    ["ž", "z"],
    ["ź", "z"],
]


def process_text(text: str) -> str:
    for replacement in sorbian_to_german_chars:
        text = text.replace(replacement[0], replacement[1])
    if text[-1] == "." or text[-1] == "!" or text[-1] == "?":
        text = text[:-1]
    return text


def cosine_similarity_text(t1: str, t2: str, text_processing: bool = True) -> int:
    if text_processing:
        t1 = process_text(t1)
        t2 = process_text(t2)
    data = [t1, t2]
    count_vectorizer = CountVectorizer()
    vector_matrix = count_vectorizer.fit_transform(data)
    vector_matrix.toarray()
    return cosine_similarity(vector_matrix)[0][1]

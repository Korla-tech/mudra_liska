import nlp.main as skill
from nlp.skill_helpers import similarity

no_input_skill = skill.Simple_skill(
    pattern=[], output="Dyrbiš něšto zapodać.")

last_skill = None


def process(text: str, debug: bool = False) -> dict:

    text = text.lower().strip()

    if text == "":
        return no_input_skill.call(text)

    for skill1 in list(skill.skills.values()):
        if skill1.check_match(text):
            return skill1.call(text)
    similarities = {}
    for skill_id in skill.skills:
        skill1 = skill.skills[skill_id]
        best_similarity = 0
        for pattern in skill1.pattern:
            current_similarity = similarity.cosine_similarity_text(
                text, pattern)
            if current_similarity > best_similarity:
                best_similarity = current_similarity
        similarities[skill_id] = best_similarity

    best_similarity = 0
    best_skill = ""
    for skill_id in similarities:
        skill_similarity = similarities[skill_id]
        if skill_similarity > best_similarity:
            best_similarity = skill_similarity
            best_skill = skill_id

    if best_similarity > 0.6:
        return skill.skills[best_skill].call(prompt=text)
    else:
        return skill.skills["x"].call(prompt=text)

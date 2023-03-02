from nlp.skills import rozhlos_skill, weather_skill
from nlp.skills.base_skills import Simple_skill, OpenAI_skill, Stop_skill

# TODO:
# pc control -> wočin firefox
# płaćizny tankwnje
# akcije
# zastupny plan
# support za smóratka
# automatiska aktiwacija
# matematika
# hudźba
# üudźak
# přełožić
# gramatika
# lampa
# dobre ranje rutina

skills = {
    "0": Simple_skill(pattern=["kak rěkaš", "kak rěkaš ty", "kak rěkaće", "što je twojem mjeno", "što je waše mjeno", "štó sy", "štó sy ty"], output="Ja sym mudra liška."),
    "1": Simple_skill(pattern=["što je tebje wuwił", "kak rěkar twój programěrowar", "što je tebje stworił", "kak rěka twój stworićel"], output="Mje je Korla Baier wuwił."),
    "2": Simple_skill(pattern=["powědaj mi žort", "žort prošu", "powědaj mi směšk", "směšk prošu"], output=["to je směšny žort.", "to njeje směšny žort."]),
    "3": rozhlos_skill.Rozhlos_skill(pattern=["zawěć rozhłos", "zawěć serbski rozhłos", "zawěć serbske radio", "zawěć radio", "radio prošu", "radio", "rozhłos prošu", "rozhłos", "serbske radio", "serbske radio prošu"]),
    "s": Stop_skill(pattern=["stop", "štop", "hasnyć", "prošu hasnyć"]),
    "x": OpenAI_skill(pattern=[], debug=True)
}

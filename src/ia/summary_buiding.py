import ollama
from src.config import SYSTEM_SUMMARY, SUMMARY_RATIO, MIN_WORDS
from src.ia.split_text_into_sections import split_text_into_sections

def build_summary_messages(section_text, target_words, system_prompt=SYSTEM_SUMMARY):
    return [
        {"role": "system", "content": system_prompt.format(target_words=target_words)},
        {"role": "user", "content": f"Extrait à résumer :\n\n{section_text}"},
    ]

def get_summary(model, document_content, ratio=SUMMARY_RATIO):
    sections = split_text_into_sections(document_content)
    summaries = []

    for i, section in enumerate(sections, start=1):
        if not section.strip():
            continue

        target_words = max(MIN_WORDS, round(len(section.split()) * ratio))  #on calcule le nombre de mots à résumer en fonction du ratio et on s'assure qu'il est au moins égal à MIN_WORDS
        print(f"Résumé de la section {i}/{len(sections)}...")

        response = ollama.chat(
            model=model,
            messages=build_summary_messages(section, target_words),
            think=False,
            options={"temperature": 0.3},
        )
        summaries.append(response["message"]["content"].strip())

    return "\n\n".join(summaries)
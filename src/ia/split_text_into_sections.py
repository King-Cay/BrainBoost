import re
from config import MAX_SECTION_LENGTH

def split_text_into_sections(markdown,max_section_length=MAX_SECTION_LENGTH):
    """
    Split the given markdown text into sections based on headings and a maximum section length.

    Args:
        markdown (str): The markdown text to be split.
        max_section_length (int): The maximum length of each section.
    """
    parts = re.split(r"(?m)^(?=#{1,3})", markdown)
    sections = []

    current_section = ""
    for part in parts:
        if len(current_section) + len(part) > max_section_length:
            sections.append(current_section)
            current_section = ""
        current_section += part

    if current_section.strip():
        sections.append(current_section)

    return sections

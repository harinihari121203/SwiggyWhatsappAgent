import re

def detect_intent(message: str) -> str:
    if re.fullmatch(r"\d{10}", message):
        return "MOBILE_NUMBER"
    return "QUESTION"

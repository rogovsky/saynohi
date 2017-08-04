import re

_known_greetings = ("hi", "hello", "greetings", "hi there", "hi how are you", "salut",
                    "привет", "хай", "здарова", "здорово", "привет как дела", "салют", "хопчик", "прив")
_punctuation_pattern = r"[.,:;()!?/\-\\]"


class HiDetector:
    @staticmethod
    def is_greeting(message):
        pure_message = HiDetector._extract_pure_text(message)
        return pure_message in _known_greetings

    @staticmethod
    def _extract_pure_text(message):
        (message, _) = re.subn(_punctuation_pattern,
                               "",
                               message)
        message = message.strip().lower()
        return message

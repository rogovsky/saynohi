import re

_known_greetings = ("hi", "hello", "greetings", "hi there", "hi how are you", "salut",
                    "привет", "хай", "здарова", "здорово", "привет как дела")
_punctuation_pattern = r"[.,:;()!?/\-\\]"


class HiDetector:
    @staticmethod
    def is_greeting(message):
        raw_message = HiDetector._strip_from_punctuation(message)
        return raw_message in _known_greetings

    @staticmethod
    def _strip_from_punctuation(message):
        (message, _) = re.subn(_punctuation_pattern,
                               "",
                               message)
        message = message.strip().lower()
        return message

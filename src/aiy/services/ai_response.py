class RecognitionResult:
    def __init__(self, text = None, success = True):
        self.text = text
        self.success = success

class TranslationResult:
    def __init__(self, text) -> None:
        self.text = text

class EntityRecognitionResult:
    def __init__(self, intents = [], success = True) -> None:
        self.intents = intents
        self.success = success
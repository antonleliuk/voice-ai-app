from .ai_response import RecognitionResult, TranslationResult, EntityRecognitionResult

class UnknownAiService:
    @staticmethod
    def ai_service_code() -> str:
        return "unknown"
    
    def speech_recognition(self, filename) -> EntityRecognitionResult:
        raise NotImplementedError()
    
    def text_recognition(self, text) -> EntityRecognitionResult:
        raise NotImplementedError()

    def dictation(self, filename) -> RecognitionResult:
        raise NotImplementedError()
    
    def translation(self, original_text, from_lang='ru', to_lang='ru') -> TranslationResult:
        raise NotImplementedError()
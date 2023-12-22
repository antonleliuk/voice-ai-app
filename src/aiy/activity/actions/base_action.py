import logging
import voice.pyttsx as voice_service
from services.ai_response import RecognitionResult
import services.ai_service as ai_service

from .stop import StopActivity

class BaseActivity:
    def __init__(self, activity_code) -> None:
        self.activity_code = activity_code

    def _did_get(self, text) -> bool:
        if not text:
            logging.warn("Didn't get what are you saying")
            voice_service.say("Извините, я вас не понял")
            return True
        return False
    
    def _should_proceed(self, response: RecognitionResult) -> bool:
        if self._did_get(response.text):
            return False
        
        recognition = ai_service.get_service().text_recognition(response.text)
        
        for intent in recognition.intents:
            logging.info("Should process intent is: " + str(intent))
            if intent == StopActivity.activity_code():
                logging.info("Detected stopping current activity: " + self.activity_code)
                StopActivity().handleActivity(response)
                return False
        return True
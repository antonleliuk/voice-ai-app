import logging
import services.ai_service as ai_service
import activity.service.activity_service as activity_service
import voice.pyttsx as voice_service

from services.ai_response import RecognitionResult
from aiy.voice import tts

from .base_action import BaseActivity

class PlayTranslateActivity(BaseActivity):
    def __init__(self) -> None:
        super().__init__(PlayTranslateActivity.activity_code())

    @staticmethod
    def activity_code():
        return "play_translate"
    def startSpeech(self):
        return "Произнесите слова для перевода"
    def startActivity(self, intent, action=None):
        # insert or update activity
        logging.info("Start translate activity")
        activity_service.startActivity(intent=intent, action=action)
        voice_service.say("Давай! Говори, а я переведу")

    def handleActivity(self, response: RecognitionResult):
        # check stop word
        if self._should_proceed(response):
            spoken_text = response.text
            logging.info("Trying to translate: " + str(spoken_text))
            # send request to translate
            result = ai_service.get_service().translation(spoken_text)
            if result.text:
                logging.info("Translated text: " + result.text)
                # speak what was translated
                tts.say(text = result.text, volume = 40)
        
    
import logging
import json
import activity.service.activity_service as activity_service
import voice.pyttsx as voice_service

from mq.message_service import connection_factory
from services.ai_response import RecognitionResult
from .base_action import BaseActivity

class DrawActivity(BaseActivity):
    
    def __init__(self) -> None:
        super().__init__(DrawActivity.activity_code())

    @staticmethod
    def activity_code():
        return "draw"
    def startSpeech(self):
        return "Скажите, чтобы Вы хотели нарисовать"
    def startActivity(self, intent, action=None):
        # insert or update activity
        logging.info("Start draw activity")
        activity_service.startActivity(intent, action)
        voice_service.say("Давай! Говори, что нарисовать")
    def handleActivity(self, response: RecognitionResult):
        # get image from speech
        if self._should_proceed(response):
            # send message to draw image
            logging.info(f"Sending message to draw image: {response.text}")
            connection_factory.send_message("draw", payload=json.dumps({"text": response.text}))
            # say something
            voice_service.say(f"Рисую - {response.text}")
import logging
import voice.pyttsx as voice_service

from services.ai_response import RecognitionResult

class UnknownActivity:
    @staticmethod
    def activity_code():
        return "unknown"
    def startSpeech(self):
        return "Говорите, а затем нажмите еще раз, чтобы обработать"
    def startActivity(self, intent = None, action = None):
        # say something that we cannot get what you want
        logging.warn("Couldn't understand activity with intent: " + str(intent) + ", action: " + str(action))
        voice_service.say(text="Извините, я вас не понял")
    
    def handleActivity(self, response: RecognitionResult):
        voice_service.say(text="Извините, я вас не понял")
        pass
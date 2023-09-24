import logging
import activity.service.activity_service as activity_service

class StopActivity:
    @staticmethod
    def activity_code():
        return "stop"
    def startSpeech(self):
        return "Говорите, а затем нажмите еще раз, чтобы обработать"
    def startActivity(self, intent, action):
        self._stopActivity()

    def handleActivity(self, response):
        self._stopActivity()

    def _stopActivity(self):
        logging.info("Stopping current activity")
        activity_service.stopActivity()
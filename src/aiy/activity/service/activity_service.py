import activity.service.activity_db_service as activity_db_service
import logging

import voice.pyttsx as voice_service
import services.ai_service as ai_service

from activity.service.activity_factory import ActivityFactory
from activity.service.activity_context import ActivityContext
from services.ai_response import RecognitionResult, EntityRecognitionResult
from activity.domain.activity import ActivityModel
from typing import Optional
from datetime import datetime

_activityFactory = ActivityFactory()

def startSpeech(activityModel: Optional[ActivityModel]):
    logging.info('Start speech for activity: ' + str(activityModel))
    code = "" if activityModel is None else activityModel.activity_code()
    activity = _activityFactory.resolve_activity(code)
    voice_service.say(text = activity.startSpeech())

def processAudio(audio_file_path):
    # trying to guess if user say - stop
    # text = speech_recognition.recognize(audio_file_path)
    # logging.info("Text from local recognition is: " + str(text))
    # speech-to-text
    # send request to wit.ai
    current = activity_db_service.get_current_activity()
    aiService = ai_service.get_service()
    if current is not None:
        response = aiService.dictation(audio_file_path)
        _activityFactory.resolve_activity(current.activity_code()).handleActivity(response)
    else:
        context = _resolveActivity(aiService.speech_recognition(audio_file_path))
        context.activity.startActivity(context.intent)

def _resolveActivity(response: EntityRecognitionResult) -> ActivityContext:
    if response.intents:
        for intent in response.intents:
            activity = _activityFactory.resolve_activity(intent)
            return ActivityContext(activity, intent)
    
    activity = _activityFactory.resolve_activity(None)
    return ActivityContext(activity)

def getCurrentActivity() -> Optional[ActivityModel]:
    return activity_db_service.get_current_activity()

def startActivity(intent, action=None):
    current = activity_db_service.get_current_activity()
    if current is None:
        current = ActivityModel(id = None, intent=intent, action=action)
    else:
        current.intent = intent
        current.action = action
        current.request_date = datetime.now()

    logging.info("Saving or updating activity")
    activity_db_service.save(current)


def stopActivity():
    current = activity_db_service.get_current_activity()
    if current is not None:
        logging.info("Delete activity with id: " + str(current.id))
        activity_db_service.delete(current)
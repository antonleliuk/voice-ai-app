import logging
import os
import requests

from wit import Wit
from .http_exception import HttpException
from .ai_response import RecognitionResult, TranslationResult, EntityRecognitionResult
from variables import variables

access_token = variables.wit_ai_access_token()

client = Wit(access_token)
client.logger.setLevel(logging.DEBUG)

# copied from original wit.py
def _req(meth, path, params, **kwargs):
    full_url = variables.wit_ai_host() + path
    client.logger.debug("%s %s %s", meth, full_url, params)
    headers = {
        "authorization": "Bearer " + str(client.access_token),
        "accept": "application/vnd.wit." + variables.wit_ai_api_version() + "+json",
    }
    headers.update(kwargs.pop("headers", {}))
    rsp = requests.request(meth, full_url, headers=headers, params=params, **kwargs)
    if rsp.status_code > 200:
        raise HttpException(
            "Wit responded with status: "
            + str(rsp.status_code)
            + " ("
            + rsp.reason
            + ")"
        )
    client.logger.info("Raw response is: " + str(rsp.content.decode('utf-8')))
    json = rsp.json()
    if "error" in json:
        raise HttpException("Wit responded with an error: " + json["error"])

    client.logger.debug("%s %s %s", meth, full_url, json)
    return json

class WitAiService:
    @staticmethod
    def ai_service_code():
        return "wit_ai"

    def speech_recognition(self, filename) -> EntityRecognitionResult:
        resp = None
        logging.info('Sending speech-to-text request')
        with open(filename, 'rb') as f:
            resp = client.speech(audio_file=f, headers={'Content-Type':'audio/wav'}, verbose=True)
        logging.info('Response is: ' + str(resp))
        return resp

    def text_recognition(self, text) -> EntityRecognitionResult:
        raise NotImplementedError()

    def dictation(self, filename) -> RecognitionResult:
        raise NotImplementedError()
        # resp = None
        # logging.info("Sending dictation request")
        # with open(filename, 'rb') as f:
        #     # ;encoding=unsigned-integer;bits=16;rate=8000;endian=litte
        #     params = {"verbose": True}
        #     headers={'Content-Type':'audio/wav'}
        #     _req("POST", "/dictation", params, data=f, headers = headers)
    
    def translation(self, original_text, from_lang='ru', to_lang='ru') -> TranslationResult:
        raise NotImplementedError()
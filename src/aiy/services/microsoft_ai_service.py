import requests
import logging
import uuid
import time

from requests import Response
from .http_exception import HttpException
from .ai_response import RecognitionResult, TranslationResult, EntityRecognitionResult
from variables import variables

speech_url = f"https://{variables.ms_speech_region()}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=ru-RU&format=detailed"
speech_headers = {
    "Ocp-Apim-Subscription-Key": variables.ms_speech_key(),
    "Content-Type": "audio/wav",
}

translate_url = "https://api.cognitive.microsofttranslator.com/translate"
translate_headers = {
    'Ocp-Apim-Subscription-Key': variables.ms_translate_secret_key(),
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': variables.ms_translate_region(),
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

luis_url_submit_job = f"https://{variables.ms_luis_endpoint()}.cognitiveservices.azure.com/language/analyze-text/jobs?api-version=2022-10-01-preview"
luis_headers = {
    'Ocp-Apim-Subscription-Key': variables.ms_luis_key(),
    'Content-Type': 'application/json'
}

class MicrosoftAiService:
    @staticmethod
    def ai_service_code():
        return "microsoft"
    
    # https://voice-ai-luis.cognitiveservices.azure.com/
    def speech_recognition(self, filename) -> EntityRecognitionResult:
        logging.info('Sending speech-to-text request')
        dictation_result = self.dictation(filename)
        if dictation_result.success:
            return self.text_recognition(dictation_result.text)
        return EntityRecognitionResult(success=False)
    
    def text_recognition(self, text) -> EntityRecognitionResult:
        logging.info('Sending text recognition requests')

        rsp = requests.post(luis_url_submit_job, headers=luis_headers, json = 
                                {
                                    'tasks': [
                                        {
                                            'kind': "CustomEntityRecognition",
                                            'parameters': {
                                                'projectName': variables.ms_luis_project_name(),
                                                'deploymentName': variables.ms_luis_deployment_name()
                                            }
                                        }
                                    ],
                                    'displayName': 'CustomTextPortal_CustomEntityRecognition',
                                    'analysisInput': {
                                        'documents': [
                                            {
                                                'id': 'document_CustomEntityRecognition',
                                                'text': text,
                                                'language': 'ru'
                                            }
                                        ]
                                    }
                                })
        self._print_response(rsp)
        if rsp.status_code == 202:
            start = time.monotonic()
            while True:
                duration = time.monotonic() - start
                if duration >= 5.00:
                    logging.warn("Entity recognition couldn't process in 5 seconds")
                    break

                logging.info('Sending entity recognition request')
                get_rsp = requests.get(rsp.headers['Operation-Location'], headers=luis_headers)
                self._print_response(get_rsp)
                if get_rsp.status_code == 200:
                    err = EntityRecognitionResult()
                    processed = False
                    get_rsp_json = get_rsp.json()
                    if get_rsp_json["status"] == 'succeeded':
                        tasks = get_rsp_json["tasks"]
                        if tasks["completed"] == 1:
                            for item in tasks["items"]:
                                if item["status"] == 'succeeded':
                                    results = item["results"]
                                    for document in results["documents"]:
                                        for entity in document["entities"]:
                                            if entity["confidenceScore"] >= 0.5:
                                                err.intents.append(entity["category"])
                                                processed = True

                    if processed:
                        return err
                    elif get_rsp.status_code == 202:
                        continue
                    else:
                        self._handle_rest_exception(get_rsp)
                    
                logging.info('Sleep recognition for 1 seconds before next try')
                time.sleep(1)
        elif rsp.status_code == 200:
            pass
        else: 
            self._handle_rest_exception(rsp)
        
        return EntityRecognitionResult(success=False)

    def dictation(self, filename) -> RecognitionResult:
        resp = None
        logging.info('Sending dictation request')
        with open(filename, 'rb') as f:
            rsp = requests.post(speech_url, headers=speech_headers, data=f)
        self._print_response(rsp)
        self._handle_rest_exception(rsp)
        _json = rsp.json()
        if _json["RecognitionStatus"] == "Success":
            return RecognitionResult(text = _json["DisplayText"])
        
        return RecognitionResult(success=False)

    def translation(self, original_text, from_lang='ru', to_lang='en') -> TranslationResult:
        resp = None
        logging.info('Sending translation request')
        rsp = requests.post(translate_url, headers=translate_headers, 
                            params={'api-version': '3.0', 'from': from_lang, 'to': to_lang}, 
                            json=[{ 'text': original_text }])
        self._print_response(rsp)
        self._handle_rest_exception(rsp)
        _json = rsp.json()
        for entity in _json:
            for translation in entity["translations"]:
                return TranslationResult(translation["text"])
        return TranslationResult("")


    def _handle_rest_exception(self, rsp: Response):
        if rsp.status_code > 200:
                raise HttpException(
                    "Response with status: "
                    + str(rsp.status_code)
                    + " ("
                    + rsp.reason
                    + ")"
                )
    def _print_response(self, rsp: Response):
        logging.info("Raw response is: " + str(rsp.content.decode('utf-8')))

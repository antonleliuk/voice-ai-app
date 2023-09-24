import os
from dotenv import load_dotenv
from typing import Any
from singleton_factory import SingletonMeta
    

class Variables(metaclass=SingletonMeta):
    def __init__(self) -> None:
        load_dotenv()

    def wit_ai_access_token(self): 
        return os.getenv("WIT_AI_ACCESS_TOKEN")
    
    def wit_ai_host(self):
        return os.getenv("WIT_URL", "https://api.wit.ai")
    
    def wit_ai_api_version(self):
        return os.getenv("WIT_API_VERSION", "20200513")
    
    def ms_translate_secret_key(self):
        return os.getenv("MS_TRANSLATE_SECRET_KEY")

    def ms_translate_region(self): 
        return os.getenv("MS_TRANSLATE_REGION")

    def ms_speech_key(self):
        return os.getenv("MS_SPEECH_KEY")

    def ms_speech_region(self):
        return os.getenv("MS_SPEECH_REGION")

    def ms_luis_key(self):
        return os.getenv("MS_LUIS_KEY")

    def ms_luis_region(self):
        return os.getenv("MS_LUIS_REGION")

    def ms_luis_endpoint(self):
        return os.getenv("MS_LUIS_ENDPOINT")
    
    def ms_luis_project_name(self):
        return os.getenv("MS_LUIS_PROJECT_NAME")
    
    def ms_luis_deployment_name(self):
        return os.getenv("MS_LUIS_DEPLOYMENT_NAME")

    def ai_service(self):
        return os.getenv("AI_SERVICE", "microsoft")
    
    def mq_host(self) -> str:
        return os.getenv("MQ_HOST", "localhost")
    
variables = Variables()
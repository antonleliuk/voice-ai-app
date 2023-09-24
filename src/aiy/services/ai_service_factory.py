import os
from services.wit_ai_service import WitAiService
from services.microsoft_ai_service import MicrosoftAiService
from services.unknown_ai_service import UnknownAiService
from variables import variables

class AiServiceFactory:
    def __init__(self) -> None:
        self.factories = {
            WitAiService.ai_service_code(): WitAiService(),
            MicrosoftAiService.ai_service_code(): MicrosoftAiService()
        }

    def resolve_factory(self):
        return self.factories.get(variables.ai_service(), UnknownAiService())
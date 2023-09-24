from .ai_service_factory import AiServiceFactory

_aiServiceFactory = AiServiceFactory()

def get_service():
    return _aiServiceFactory.resolve_factory()
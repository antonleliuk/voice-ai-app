from datetime import datetime

class ActivityModel:
    def __init__(self, id, intent, action):
        self.id = id
        self.intent = intent
        self.action = action
        self.request_date = datetime.now()

    def __str__(self):
        return f"ActivityModel(id={self.id}, intent={self.intent}, action={self.action})"
    
    def activity_code(self):
        return self.intent
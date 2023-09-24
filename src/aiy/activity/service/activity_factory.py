from activity.actions.play_translate import PlayTranslateActivity
from activity.actions.draw import DrawActivity
from activity.actions.stop import StopActivity
from activity.actions.unknown_activity import UnknownActivity

class ActivityFactory:
    
    def __init__(self) -> None:
        self.activities = {
            PlayTranslateActivity.activity_code(): PlayTranslateActivity(),
            DrawActivity.activity_code(): DrawActivity(),
            StopActivity.activity_code(): StopActivity()
        }
    
    def resolve_activity(self, code):
        return self.activities.get(code, UnknownActivity())
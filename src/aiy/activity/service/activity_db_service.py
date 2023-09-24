import db_service
import logging
from activity.domain.activity import ActivityModel
from typing import Optional

def init_schema():
    logging.info("Initializing schema...")
    # db_service.execute("DROP TABLE IF EXISTS activity")
    db_service.execute("""
                       CREATE TABLE IF NOT EXISTS activity(
                        id INTEGER PRIMARY KEY,
                        action VARCHAR(20) NULL,
                        intent VARCHAR(20) NOT NULL UNIQUE,
                        request_date DATETIME NOT NULL
                       )
                       """)
    logging.info("Schema initialized")
    
def get_current_activity() -> Optional[ActivityModel]:
    current = db_service.select("SELECT id AS id, action AS action, intent AS intent FROM activity LIMIT 1", _activity_code_row_factory)
    logging.info("Current activity is: " + str(current))
    if current is not None:
        return current
    else:
        return None   

def save(activity: ActivityModel):
    db_service.save("INSERT OR REPLACE INTO activity (id, intent, action, request_date) VALUES(?, ?, ?, ?)", 
                    (activity.id, activity.intent, activity.action, activity.request_date))
     
def delete(activity: ActivityModel):
    db_service.delete("DELETE FROM activity WHERE id = ?", (activity.id, ))

def _activity_code_row_factory(cursor, row) -> ActivityModel:
    return ActivityModel(row[0], row[2], row[1])
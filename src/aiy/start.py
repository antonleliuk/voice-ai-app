import logging
import sys
import activity.service.activity_db_service as activity_db_service

from background_task import BackgroupProcess
from mq.message_service import connection_factory

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    process = None
    try:
        logging.info("start")
        activity_db_service.init_schema()
        process = BackgroupProcess()
        process.start()
        connection_factory.start()
        logging.info('working...')
        while True:
            pass
    except KeyboardInterrupt:
        print("\nCtrl+C detected in the main thread. Stopping worker thread...")
        if process is not None:
            process.stop()
        if connection_factory is not None:
            connection_factory.stop()
        sys.exit(0)
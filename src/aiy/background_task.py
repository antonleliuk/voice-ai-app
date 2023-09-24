import threading
import time
import logging
import os

import activity.service.activity_service as activity_service

from board import Board, Led
from voice.audio import AudioFormat, record_file
from typing import Optional
from activity.domain.activity import ActivityModel

audio_file = "data/voice_ai_recording.wav"

class BackgroupProcess:
    def __init__(self) -> None:
        self._task = threading.Thread(target=self._run_task)
        self._board = Board()
        self.stopping = threading.Event()
        
    def start(self):
        """
        Starts the assistant event loop and begins stopping events.
        """
        try:
            self._task.start()
        except KeyboardInterrupt:
            logging.info("Closing background task")
    
    def stop(self):
        logging.info("Closing...")
        self.stopping.set()
        self._releaseButtonEvents(self._board.button._pressed_queue)
        self._releaseButtonEvents(self._board.button._released_queue)
        self._board.close()

    def _releaseButtonEvents(self, events):
        while not events.empty():
            event = events.get_nowait()
            event.set()        

    def _run_task(self):
        try:
            while not self.stopping.is_set():
                self._update_led(Led.DECAY, 0.1)
                self._board.button.wait_for_press()
                if not self.stopping.is_set():
                    done = threading.Event()
                    self._board.button.when_pressed = done.set
                    # record audio

                    if os.path.exists(audio_file):
                        os.remove(audio_file)

                    self._startSpeech()
                    def wait():
                        start = time.monotonic()
                        self._update_led(Led.BLINK, 0.1) # recording :-)
                        while not done.is_set() and not self.stopping.is_set():
                            duration = time.monotonic() - start
                            if duration >= 5.00:
                                done.set()
                                break
                            print('Recording: %.02f seconds [Press button to stop]' % duration)
                            time.sleep(0.5)

                    record_file(AudioFormat.CD, filename=audio_file, wait=wait, filetype='wav')
                    if not self.stopping.is_set():    
                        # get the audio
                        logging.info('Getting audio to process speech-to-text')
                        
                        # process audio file
                        activity_service.processAudio(audio_file)
            logging.info('Working done')
            return
        except KeyboardInterrupt:
            logging.info('stopping...')

    def _startSpeech(self) -> Optional[ActivityModel]:
        activity = activity_service.getCurrentActivity()
        activity_service.startSpeech(activity)
        return activity
    
    def _update_led(self, state, brightness):
        self._board.led.state = state
        self._board.led.brightness = brightness
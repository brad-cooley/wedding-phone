import logging
import os
import os.path
import queue
import sys
import uuid

from threading import Thread, Event

import pygame
import asyncio
import sounddevice as sd
import soundfile as sf


class RecordingThread(Thread):

    def __init__(self, subtype='PCM_16', channels=1, frame_rate=44100, chunk=1024, device_index='USB Audio Device', save_dir=os.path.dirname(__file__)):
        super().__init__()
        self.__SUBTYPE = subtype
        self.__CHANNELS = channels
        self.__FRAME_RATE = frame_rate
        self.__CHUNK = chunk
        self.__DEVICE_INDEX = device_index
        self.__SAVE_DIR = save_dir

        self.__id = uuid.uuid1()
        self.__filename = str(self.__id) + ".wav"
        self.__filepath = os.path.join(self.__SAVE_DIR, self.__filename)
        self.__recording = False

        pygame.mixer.init()
        self.__VOICE_MESSAGE = pygame.mixer.Sound('VoiceMessage.wav')
        self.__MESSAGE_TONE = pygame.mixer.Sound('beep.wav')
        
        self.__stop_event = Event()

    def get_id_as_str(self):
        return str(self.__id)
    
    def get_filepath(self):
        return self.__filepath

    async def __play_voice_message(self):
        logging.info("Playing voicemail message")
        pygame.time.wait(500)
        self.__VOICE_MESSAGE.play()
        while pygame.mixer.get_busy():
            if self.__stop_event.is_set():
                pygame.mixer.stop()
                break
            pass

    def __play_message_tone(self):
        logging.info("Playing beep")
        self.__MESSAGE_TONE.play()
        while pygame.mixer.get_busy():
            if self.__stop_event.is_set():
                pygame.mixer.stop()
                break
            pass
        pygame.time.wait(200)

    def run(self):

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            q.put(indata.copy())

        async def inner_run():
            # Create and gather all the asynchronous tasks
            tasks = [
                self.__play_voice_message()
            ]

            # Wait for all the tasks to complete
            await asyncio.gather(*tasks)

            # Now, you can play the beep sound or perform any other action
            if not self.__stop_event.is_set():
                logging.info("All tasks completed, safe to play beep")
                self.__play_message_tone()

        asyncio.run(inner_run())
        q = queue.Queue()

        if not self.__stop_event.is_set():

            # Make sure the file is opened before recording anything:
            with sf.SoundFile(file=self.__filepath,
                              mode='x',
                              samplerate=self.__FRAME_RATE,
                              channels=self.__CHANNELS,
                              subtype=self.__SUBTYPE
                              ) as file:

                logging.info('File {} successfully created'.format(file.name))

                with sd.InputStream(samplerate=self.__FRAME_RATE,
                                    device=self.__DEVICE_INDEX,
                                    channels=self.__CHANNELS,
                                    callback=callback):

                    logging.info('Recording...')
                    self.__recording = True

                    while self.__recording:
                        if self.__stop_event.is_set():
                            break
                        file.write(q.get())

    def stop(self):
        if self.__recording:
            logging.info('Recording stopped. File saved to {}'.format(self.__filepath))
        else:
            logging.warning('Receiver hung up before recording started.')
            
        self.__recording = False
        # make a statement that actually checks for file and contents on disk to confirm it was saved
        self.__stop_event.set()

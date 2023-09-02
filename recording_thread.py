import uuid
import os
import os.path
import logging

from threading import Thread, Event
import pygame
import asyncio

import sounddevice as sd
import soundfile as sf
import queue
import sys

class RecordingThread(Thread):

    def __init__(self, channels=1, frame_rate=44100, chunk=4096, device_index=1):
        super().__init__()
        self.__CHANNELS = channels
        self.__FRAME_RATE = frame_rate
        self.__CHUNK = chunk
        self.__DEVICE_INDEX = device_index

        self.__SUBTYPE = 'PCM_16'

        self.__id = uuid.uuid1()
        __root_dir = os.path.dirname(__file__)
        self.__filename = str(self.__id) + ".wav"
        self.__filepath = os.path.join(__root_dir, 'audio_files', self.__filename)
        self.__recording = False

        pygame.mixer.init()
        self.__VOICE_MESSAGE = pygame.mixer.Sound('/home/phone/Documents/wedding-phone/mysound.wav')

        self.__STREAM = None
        self.__frames = []
        
        self.__stop_event = Event()

    def get_id_as_str(self):
        return str(self.__id)
    
    def get_filepath(self):
        return self.__filepath

    async def __play_voice_message(self):
        logging.info("Playing voicemail message")
        pygame.time.wait(1000)
        self.__VOICE_MESSAGE.play()
        while pygame.mixer.get_busy():
            pass

    def run(self):
        async def inner_run():
            # Create and gather all the asynchronous tasks
            tasks = [
                #self.__create_file(),
                self.__play_voice_message()
                #self.__setup_stream()
            ]

            # Wait for all the tasks to complete
            await asyncio.gather(*tasks)

            # Now, you can play the beep sound or perform any other action
            logging.info("All tasks completed, playing beep")

        asyncio.run(inner_run())

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            q.put(indata.copy())


        q = queue.Queue()

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(self.__filepath, mode='x', samplerate=self.__FRAME_RATE,
                          channels=self.__CHANNELS, subtype=self.__SUBTYPE) as file:
            logging.debug('File {} successfully created'.format(file.name))
            with sd.InputStream(samplerate=self.__FRAME_RATE, device=self.__DEVICE_INDEX,
                                channels=self.__CHANNELS, callback=callback):
                logging.info('Recording...')
                self.__recording = True
                while self.__recording:
                    if self.__stop_event.is_set():
                        break
                    file.write(q.get())

    def stop(self):
        self.__recording = False
        logging.info('Recording stopped. Saving...')
        self.__stop_event.set()

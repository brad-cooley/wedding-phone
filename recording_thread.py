import uuid
import os
import os.path
import logging

import wave
import pyaudio
from threading import Thread, Event
import pygame
import asyncio

P = pyaudio.PyAudio()


class RecordingThread(Thread):

    def __init__(self, sample_format=pyaudio.paInt16, channels=1, frame_rate=44100, chunk=4096, device_index=2):
        super().__init__()
        self.__SAMPLE_FORMAT = sample_format
        self.__CHANNELS = channels
        self.__FRAME_RATE = frame_rate
        self.__CHUNK = chunk
        self.__DEVICE_INDEX = device_index

        self.__id = uuid.uuid1()
        __root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.__filename = str(self.__id) + ".wav"
        self.__filepath = os.path.join(__root_dir, 'phone/audio_files', self.__filename)
        self.__recording = False

        pygame.mixer.init()
        self.__VOICE_MESSAGE = pygame.mixer.Sound('/home/phone/Documents/wedding-phone/mysound.wav')

        self.__STREAM = None
        self.__frames = []
        
        self.__stop_event = Event()

    def get_id_as_str(self):
        return str(self.__id)

    async def __create_file(self):
        logging.info("Creating file")
        os.mknod(self.__filename)

    async def __play_voice_message(self):
        logging.info("Playing voicemail message")
        pygame.time.wait(1000)
        self.__VOICE_MESSAGE.play()
        while pygame.mixer.get_busy():
            pass

    async def __setup_stream(self):
        logging.info("Setting up stream")
        self.__STREAM = P.open(format=self.__SAMPLE_FORMAT,
                               channels=self.__CHANNELS,
                               rate=self.__FRAME_RATE,
                               input_device_index=self.__DEVICE_INDEX,
                               frames_per_buffer=self.__CHUNK,
                               input=True)

    def run(self):
        async def inner_run():
            # Create and gather all the asynchronous tasks
            tasks = [
                self.__create_file(),
                self.__play_voice_message(),
                self.__setup_stream()
            ]

            # Wait for all the tasks to complete
            await asyncio.gather(*tasks)

            # Now, you can play the beep sound or perform any other action
            logging.info("All tasks completed, playing beep")

        asyncio.run(inner_run())

        self.__recording = True
        logging.info("Recording {}".format(self.__filename))
    
        while not self.__stop_event.is_set():
            data = self.__STREAM.read(self.__CHUNK)
            self.__frames.append(data)

        self.__STREAM.stop_stream()
        self.__STREAM.close()
        P.terminate()

        logging.info("Finished recording")

        wf = wave.open(self.__filepath, 'wb')
        wf.setnchannels(self.__CHANNELS)
        wf.setsampwidth(P.get_sample_size(self.__SAMPLE_FORMAT))
        wf.setframerate(self.__FRAME_RATE)
        wf.writeframes(b''.join(self.__frames))
        wf.close()

    def stop(self):
        self.__recording = False
        self.__stop_event.set()

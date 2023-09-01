import pyaudio
import wave

import os
import os.path
import uuid
import logging

class AudioRecording(object):
    def __init__(self):
        self.__id = uuid.uuid1()
        __root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.__filename = str(self.__id) + ".wav"
        self.__filepath = os.path.join(__root_dir, 'phone/audio_files', self.__filename)

    def get_id_as_str(self):
        return str(self.__id)

    def get_filepath_as_str(self):
        return str(self.__filepath)

    def get_filename_as_str(self):
        return str(self.__filename)

    def audio_test(self):
        CHUNK = 4096
        SAMPLE_FORMAT = pyaudio.paInt16
        CHANNELS = 1
        FRAME_RATE = 44100
        SECONDS = 3
        DEV_INDEX = 2

        with open(self.get_filepath_as_str(), 'w'):
            pass

        p = pyaudio.PyAudio()

        logging.info("Recording {}".format(self.__filename))

        stream = p.open(format=SAMPLE_FORMAT,
                        channels=CHANNELS,
                        rate=FRAME_RATE,
                        input_device_index=DEV_INDEX,
                        frames_per_buffer=CHUNK,
                        input=True)

        frames = []

        for i in range(0, int((FRAME_RATE / CHUNK) * SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        logging.info("Finished recording")

        wf = wave.open(self.__filepath, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(FRAME_RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

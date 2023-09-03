import logging
import os
import time
import sys

import RPi.GPIO as GPIO
from recording_thread import RecordingThread

recording_thread: RecordingThread or None = None
save_directory = '/home/phone/Documents/wedding_voicemail_audio_files'
logging.basicConfig(level=logging.INFO)


def phone_picked_up():
	logging.info('Receiver picked up')
	global recording_thread

	recording_thread = RecordingThread(save_dir=save_directory)
	recording_thread.start()


def phone_hung_up():
	logging.info('Receiver hung up')
	global recording_thread
	
	if recording_thread:
		recording_thread.stop()
		recording_thread = None


def listen_for_hook_state_change():
	pin_number = 12
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	try:
		while True:
			pin_current = GPIO.input(pin_number)
			if pin_current == 0:
				phone_picked_up()
			else:
				phone_hung_up()
			while GPIO.input(pin_number) == pin_current:
				time.sleep(0.1)
	except KeyboardInterrupt:
		print('Exiting...')
		GPIO.cleanup()


if __name__ == "__main__":
	save_path = sys.argv[1] if len(sys.argv) > 1 else save_dir
	logging.info('Using path {}'.format(save_path))
	if not os.path.exists(save_path):
        os.mkdir(save_path)
        logging.info('Given path doesn\'t exist. Path created')
        
	listen_for_hook_state_change()

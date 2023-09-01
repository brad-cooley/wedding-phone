import RPi.GPIO as GPIO
import time
import logging

logging.basicConfig(level=logging.INFO)

def phone_picked_up():
	logging.info('Receiver picked up')

def phone_hung_up():
	logging.info('Receiver hung up')

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
	listen_for_hook_state_change()

.PHONY: install
install:
	@cd deployment && bash install.sh

.PHONY: run
run:
	@cd src && python app.py '/home/phone/Documents/wedding_voicemail_audio_files'

.PHONY: configure-audio
configure-audio:
	@cd deployment && bash configure_usb_audio.sh

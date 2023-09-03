PI_IP_ADDRESS=10.0.0.10 #update this
PI_USERNAME=pi #update this


.PHONY: copy
copy:
	@rsync -a $(shell pwd) --exclude env $(PI_USERNAME)@$(PI_IP_ADDRESS):/home/$(PI_USERNAME)

.PHONY: install
install:
	@cd deployment && bash install.sh

.PHONY: run
run:
	@. env/bin/activate && cd src && python app.py '/home/phone/Documents/wedding_voicemail_audio_files'

.PHONY: test
test:
	@echo "Say Something for the next 5 seconds"
	@arecord -D plughw:1,0 --duration=5 test.wav
	@echo "You should hear your voice back"
	@aplay test.wav
	@rm -rf test.wav

.PHONY: shell
shell:
	@ssh $(PI_USERNAME)@$(PI_IP_ADDRESS)

.PHONY: configure-audio
configure-audio:
	@cd deployment && bash configure_usb_audio.sh

.PHONY: configure-on-boot
configure-on-boot:
	@echo "Configuring /etc/rc.local"
	@cd deployment && bash configure_on_boot.sh
BASE_DIR	:= /media/$(USER)
TARGET		:= $(BASE_DIR)/CIRCUITPY

deploy:
	cp *.py $(TARGET)
	cp the_sign/*.py $(TARGET)/the_sign/
	cp the_sign/animations/*.py $(TARGET)/the_sign/animations/

watch:
	while inotifywait -e close_write *.py the_sign/*.py the_sign/animations/*.py; do \
		make deploy; \
	done
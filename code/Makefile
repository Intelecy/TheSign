BASE_DIR	:= /media/$(USER)
TARGET		:= $(BASE_DIR)/CIRCUITPY

deploy:
	rsync -urvh -W --inplace --no-compress --exclude='__pycache__/' --exclude='*.pyc' code.py the_sign /run/media/jonathan/CIRCUITPY
#	cp *.py $(TARGET)
#	cp the_sign/*.py $(TARGET)/the_sign/
#	cp the_sign/animations/*.py $(TARGET)/the_sign/animations/
#	cp the_sign/images/*.py $(TARGET)/the_sign/images/

watch:
	while inotifywait -e close_write *.py the_sign/*.py the_sign/animations/*.py the_sign/images/*.py; do \
		make deploy; \
	done
XVFB_S=:1 -screen 0 1024x768x24 -ac +extension GLX +render -noreset &> xvfb.log
DISPLAY_S=:1

install:
	poetry install

update:
	poetry update

run:
	./gradlew run > /tmp/log_grandle.log & \
	poetry run python main.py

run_game:
	poetry run python main.py

virtual_display:
	Xvfb ${XVFB_S} & \
	export DISPLAY=${DISPLAY_S}

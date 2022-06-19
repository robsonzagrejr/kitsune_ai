install:
	poetry install

update:
	poetry update

run:
	./gradlew run > /tmp/log_grandle.log & \
	poetry run python main.py

run_game:
	poetry run python main.py
	

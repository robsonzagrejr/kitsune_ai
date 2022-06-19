install:
	poetry install

update:
	poetry update

run:
	./gradlew run & \
	poetry run python main.py

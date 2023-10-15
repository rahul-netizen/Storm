help:
	@echo "Available command"
	@echo "- pytest.      : Run tests "
	@echo "- format       : Format python scripts using black & isort"
	@echo "- type	      : Perform type check using mypy"
	@echo "- lint         : Lint the code using flake8"
	@echo "- secure       : Perform security vulnerabilities in files"
	@echo "- deps	      : Install required dependency for the project"
	@echo "- ci	      	  : Perform CI steps using format, type, line & secure"
	@echo "- perms        : Set rwx permission & change group to dev for all files in the project"

.PHONY:  ci

perms:
	sudo chgrp dev Manage && sudo chmod -R u=rwx,g=rwx Manage

pytest:
	python3 -m pytest --log-cli-level info -p no:warnings -v ./tests

format:
		python3 -m isort .
		python3 -m black -S .

# type:
# 		python3 -m mypy .

lint:
		python3 -m flake8 .

secure:
		python3 -m bandit -r .
deps:
	pip3 install -r requirements.txt

ci : format lint secure

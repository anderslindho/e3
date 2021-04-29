.DEFAULT_GOAL :=

init:
	pip3 install -r requirements.txt --user

test:
	python3 -m pytest --verbose

.PHONY: clean
clean:
	@rm -rf modules
	@rm -rf build
	@rm -rf *.tmp
	@rm -rf *.tmp.*
	@rm -rf specifications/*.tmp.*

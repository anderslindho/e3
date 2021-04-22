.DEFAULT_GOAL :=

init:
    pip3 install -r requirements.txt --user

test:
    pytest --verbose

.PHONY: clean
clean:
	@rm -rf modules
	@rm -rf build
	@rm -rf *.tmp
	@rm -rf *.tmp.*
	@rm -rf specifications/*.tmp.*

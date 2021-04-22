.DEFAULT_GOAL :=

.PHONY: clean
clean:
	@rm -rf modules
	@rm -rf build
	@rm -rf *.tmp
	@rm -rf *.tmp.*
	@rm -rf specifications/*.tmp.*

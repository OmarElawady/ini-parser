MAIN_SCRIPT = "parser.py"
TEST_SCRIPT = "parser_test.py"
use:
	python $(MAIN_SCRIPT)
test:
	python $(TEST_SCRIPT)


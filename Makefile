MAIN_SCRIPT = "parser.py"
PARSER_TEST_SCRIPT = "parser_test.py"
PARSER_UNIT_TESTS = "parser_unit_tests.py"
CONFIGDATA_TESTS = "test_config_data.py"
use:
	python $(MAIN_SCRIPT)
test: clean-pyc
	python $(PARSER_TEST_SCRIPT)
	python $(PARSER_UNIT_TESTS)
	py.test test_config_data.py
clean-pyc:
	rm *.pyc

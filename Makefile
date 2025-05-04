run:
	python app.py

test-all:
	PYTHONPATH=. pytest -v --tb=short tests/

test-cli:
	PYTHONPATH=. pytest -v --tb=short tests/test_agent_cli.py::test_list_agents_and_exit

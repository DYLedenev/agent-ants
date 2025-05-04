run:
	python app.py

test-all:
	PYTHONPATH=. pytest -v --tb=short tests/

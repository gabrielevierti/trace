.PHONY: test demo

test:
	python -m pytest -q

demo:
	python examples/generate_demo.py

PY ?= .venv/bin/python

CHAPTER_SCRIPTS := $(wildcard src/viz/ch*.py)

.PHONY: help venv test figures video $(CHAPTER_SCRIPTS:src/viz/%.py=%)

help:
	@echo "make venv      create .venv and install the package + dev deps"
	@echo "make test      re-verify every mathematical claim in the guide"
	@echo "make figures   re-render every figure and GIF in guide/"
	@echo "make ch07_jacobian   re-render a single chapter's figures"
	@echo "make video     stitch all guide figures+GIFs into video/*.mp4 (needs ffmpeg)"

venv:
	python3 -m venv .venv
	.venv/bin/pip install -e ".[dev]"

test:
	$(PY) -m pytest tests/ -q

figures:
	@set -e; for f in $(CHAPTER_SCRIPTS); do \
		echo "== $$f"; (cd src/viz && ../../$(PY) $$(basename $$f)); done

video:
	cd src/viz && ../../$(PY) make_video.py

# `make ch05_linear_determinant` etc.
ch%:
	cd src/viz && ../../$(PY) ch$*.py

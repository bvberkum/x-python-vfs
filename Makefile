default:

run: A := -h
run:
	PYTHONPATH=src:$$PYTHONPATH ./x-fuse.py $(A)

test: run
	PYTHONPATH=src:$$PYTHONPATH sh ./tools/ci/parts/test.sh

.PHONY: default run test

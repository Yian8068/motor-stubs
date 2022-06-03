build:
	poetry build

setup: build
	mkdir output; tar -C ./output -zxvf ./dist/*.tar.gz; cp ./output/motor*/setup.py setup.py

clean:
	rm -rf output dist

.PHONY: build setup clean

inventory.csv: data inventory_grabber.py
	python inventory_grabber.py

data:
	rm -rf data && mkdir data && scp login.eecs.berkeley.edu:/project/eecs/fearing/wiki/wiki.d/INV.* data/

.PHONY: data

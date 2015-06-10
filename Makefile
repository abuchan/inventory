inventory.csv: data inventory_grabber.py
	python inventory_grabber.py

data:
	scp login.eecs.berkeley.edu:/project/eecs/fearing/wiki/wiki.d/INV.* data

.PHONY: data

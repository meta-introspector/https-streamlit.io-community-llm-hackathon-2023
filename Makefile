test3:
	python ./src/streamlit_app.py
test2:
	git cat-file --batch --batch-all-objects -p > all2.txt

test:
	python ./readcat.py


# GHCND README
1. set the `self.start_year`, `self.end_year` in utils.py(~lines 19-20)
2. Run download.py
3. run clean.py
4. run transform.py
5. the data is placed at `$HOME/capstone-data`
6. the finalized tables are at `$HOME/capstone-data/curated/combined` These can be accessed via a dataset instance as in the jupyter notebook ghcnd_tutorial.ipynb

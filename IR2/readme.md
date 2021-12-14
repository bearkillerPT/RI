```
All modules can be ran without parameters to show the usage.

The searcher searches for the token on multiple documents wich are not included within this repo as they are too big.  Only a small example is included: text.csv.

Usage example:
python3 Searcher.py ok --min-length-filter 2 --stop-word-list [of, the] --no-porter-stemmer
Note: the token "of" has min_lenght 2 so it wouldn't be excluded from the index and so we add it to the stop-words-list paramether.

The indexer creates the index throughout blocks, with size/postings limit, and then merges them into the final index. Creating the final index with the postings lists is extremely slower with this technique and so, as of this version, only the index with term frequency is being built (during merge). It is extremly slow compared to just building the entire index on the fly, thanks to the MMU. Probably I misunderstood the need for builindg blocks.

```
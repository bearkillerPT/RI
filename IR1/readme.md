```
All modules can be ran without parameters to show the usage.

The searcher searches for the token on multiple documents wich are not included within this repo as they are too big.  Only a small example is included: text.csv.

Usage example:
python3 Searcher.py ok --min-length-filter 2 --stop-word-list [of, the] --no-porter-stemmer
Note: the token "of" has min_lenght 2 so it wouldn't be excluded from the index and so we add it to the stop-words-list paramether.

The indexer creates the index throughout blocks and then merges them into the final index. This, as of this version, is extremly slow compared to just building the entire index on the fly. Porbably my bad.

```
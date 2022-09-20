from .index import Index
from typing import Iterable
from .postings import Posting


class InvertedIndex(Index):
    """Implements InvertedIndex extending index"""
    def __init__(self):
        self._index={}
    
    def addTerm(self, term : str, doc_id : int):
        try:
            if (self._index[term][-1].doc_id != doc_id):
                self._index[term].append(Posting(doc_id))
        except KeyError:
            self._index[term] = [Posting(doc_id)]

    def vocabulary(self) -> Iterable[str]:
        vocabulary = list(self._index.keys())
        vocabulary.sort()
        return vocabulary

    def get_postings(self, term : str):
        return self._index[term]
from .index import Index
from typing import Iterable
from .postings import Posting


class InvertedIndex(Index):
    """Implements InvertedIndex extending index"""
    def __init__(self):
        self._index={}
    
    def addTerm(self, term : str, doc_id : int):
        if term not in self._index:
            self._index[term] = [doc_id]
            return
        if (self._index[term][-1] == doc_id):
            pass
        else:
            self._index[term].append(doc_id)

    def vocabulary(self) -> Iterable[str]:
        vocabulary = list(self._index.keys())
        vocabulary.sort()
        return vocabulary

    def get_postings(self, term : str):
        return [Posting(p) for p in self._index[term]]
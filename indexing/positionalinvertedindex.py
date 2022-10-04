from .index import Index
from typing import Iterable
from .postings import Posting


class PositionalInvertedIndex(Index):
    """Implements InvertedIndex extending index"""
    def __init__(self):
        self._index={}
    
    def addTerm(self, term : str, doc_id : int, position : int):
        try:
            last_posting = self._index[term][-1]
            if (last_posting.doc_id != doc_id):
                # Add document, and position
                self._index[term].append(Posting(doc_id,position))
            # This doesn't need to be wrapped in a try block because we
            # never create postings that don't have at least one position.
            elif (last_posting.doc_id == doc_id and last_posting.positions[-1] != position):
                last_posting.positions.append(position)
        # This code is only used on the first Posting that is added
        # TODO: Might be worth just checking len() is 0 for the first one.
        except KeyError:
            self._index[term] = [Posting(doc_id, position)]

    def vocabulary(self) -> Iterable[str]:
        vocabulary = list(self._index.keys())
        vocabulary.sort()
        return vocabulary

    def get_postings(self, term : str):
        return self._index[term]
    
    def __eq__(self,other):
        if not isinstance(other, PositionalInvertedIndex):
            return NotImplemented
        return self._index == other._index

import math
from indexing.postings import Posting
from .querycomponent import QueryComponent
from text import TokenProcessor
from math import log
from queue import PriorityQueue

class RankedQuery(QueryComponent):
    """
    A RankedTermLiteral represents a single term in a subquery.
    """

    def __init__(self, term : str, processor : TokenProcessor, corpus_size):
        self.processor = processor
        self.term = self.processor.process_token_keep_hyphen(term)
        self.corpus_size = corpus_size

    def get_postings(self, index) -> list[Posting]:
        terms = self.term.split(" ")
        [self.processor.process_token_keep_hyphen(x) for x in terms]
        Ad = {}
        results = PriorityQueue()
        for term in terms:
            postings = index.get_postings_no_pos(term)
            dft = len(postings)
            Num = self.corpus_size
            wqt = math.log(1 + (Num/dft))
            for post in postings:
                tftd = post.tftd
                wdt = 1 + math.log(tftd)
                try:
                    Ad[post.doc_id] += wdt*wqt
                except KeyError:
                    Ad[post.doc_id] = wdt*wqt
        for key,val in Ad.items():
            Ld = index.get_doc_weight(key)
            weight = val / Ld
            results.put((-weight,[key,val,Ld,wqt,dft]))
        for x in range(9):
            print(results.get())
        
        return postings

    def __str__(self) -> str:
        return self.term
    
    def __eq__(self, other) -> bool:
        return self.term == other.term
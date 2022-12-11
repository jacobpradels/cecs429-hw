from collections import defaultdict
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

    def __init__(self, term : str, processor : TokenProcessor):
        self.processor = processor
        self.term = term
    def get_postings(self, index) -> list[Posting]:
        threshhold = 1.75
        old_terms = self.term.split(" ")        
        terms = [self.processor.process_token_keep_hyphen(x) for x in old_terms]
        Ad = defaultdict(int)
        Num = index.get_doc_count()
        results = PriorityQueue()
        for term in terms:
            postings = index.get_postings_no_pos(term)
            dft = len(postings)
            if dft > 0:
                wqt = math.log(1 + (Num/dft))
            else:
                wqt = 0
            # print(wqt)
            # print("{:.2f}".format(wqt),end=" ")
            if wqt < threshhold:
                continue
            for post in postings:
                wdt = post.wdt
                Ad[post.doc_id] += wdt*wqt
        for key,val in Ad.items():
            Ld = index.get_doc_weight(key)
            weight = val / Ld
            results.put((-weight,key))
        top_docs = []
        count = 50
        if results.qsize() < count:
            count = results.qsize()
        for x in range(count):
            doc = results.get()
            top_docs.append(Posting(doc[1],score=doc[0]))

        return top_docs

    def __str__(self) -> str:
        return self.term
    
    def __eq__(self, other) -> bool:
        return self.term == other.term
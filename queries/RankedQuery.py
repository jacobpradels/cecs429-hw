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
        self.term = self.processor.process_token_keep_hyphen(term)

    def get_postings(self, index) -> list[Posting]:
        terms = self.term.split(" ")
        [self.processor.process_token_keep_hyphen(x) for x in terms]
        Ad = {}
        Num = index.get_doc_count()
        results = PriorityQueue()
        for term in terms:
            postings = index.get_postings_no_pos(term)
            dft = len(postings)
            wqt = math.log(1 + (Num/dft))
            for post in postings:
                wdt = post.wdt
                print(f"wdt({post.doc_id}) -- {wdt}") 
                try:
                    Ad[post.doc_id] += wdt*wqt
                except KeyError:
                    Ad[post.doc_id] = wdt*wqt
        for key,val in Ad.items():
            Ld = index.get_doc_weight(key)
            print(f"Ld({key} -- {Ld}")
            weight = val / Ld
            results.put((-weight,key))
        top_docs = []
        count = 10
        if results.qsize() < 10:
            count = results.qsize()
        for x in range(count):
            print(results)
            doc = results.get()
            top_docs.append(Posting(doc[1],tftd=doc[0]))

        return top_docs

    def __str__(self) -> str:
        return self.term
    
    def __eq__(self, other) -> bool:
        return self.term == other.term
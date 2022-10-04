from indexing.postings import Posting
from text import TokenProcessor
from .querycomponent import QueryComponent

class PhraseLiteral(QueryComponent):
    """
    Represents a phrase literal consisting of one or more terms that must occur in sequence.
    """

    def __init__(self, terms : list[str], processor : TokenProcessor):
        self.processor = processor
        self.terms = [self.processor.process_token_keep_hyphen(s) for s in terms]

    def get_postings(self, index) -> list[Posting]:
        
        result = [index.get_postings(s) for s in self.terms]
        offset = 1
        while (len(result) > 1):
            new_result = []
            postings1 = result[0]
            postings2 = result[1]
            first = 0
            second = 0
            # While we haven't run off the end of either list
            while first < len(postings1) and second < len(postings2):
                d1 = postings1[first].doc_id
                d2 = postings2[second].doc_id
                if d1 < d2:
                    first += 1
                elif d2 < d1:
                    second += 1
                elif d1 == d2:
                    merged_positions = merge_positions(postings1[first].positions,postings2[second].positions,offset)
                    new_result.append(Posting(d1,merged_positions))
                    first += 1
                    second += 1
            offset += 1
            result[0:2] = [new_result]
        return result[0]

        # TODO: program this method. Retrieve the postings for the individual terms in the phrase,
		# and positional merge them together.
        

    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'
    
    def __eq__(self,other) -> bool:
        return self.terms == other.terms

def merge_positions(pos1, pos2, offset):
    out = []
    first = 0
    second = 0
    while first < len(pos1) and second < len(pos2):
        first_pos = pos1[first]
        second_pos = pos2[second] - offset
        if first_pos < second_pos:
            first += 1
        elif first_pos > second_pos:
            second += 1
        else:
            out.append(pos1[first])
            first += 1
            second += 1
    return out
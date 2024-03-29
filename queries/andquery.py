from .querycomponent import QueryComponent
from indexing import Index, Posting

from queries import querycomponent 

class AndQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    def get_postings(self, index : Index) -> list[Posting]:
        result = [x.get_postings(index) for x in self.components]
        # TODO: program the merge for an AndQuery, by gathering the postings of the composed QueryComponents and
		# intersecting the resulting postings.
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
                    new_result.append(Posting(d1))
                    first += 1
                    second += 1
            result[0:2] = [new_result]
            
        return result[0]

    def __str__(self):
        return " AND ".join(map(str, self.components))


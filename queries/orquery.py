from .querycomponent import QueryComponent
from indexing import Index, Posting

from queries import querycomponent 

class OrQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    
    def get_postings(self, index : Index) -> list[Posting]:
        result = []
        # TODO: program the merge for an OrQuery, by gathering the postings of the composed QueryComponents and
		# merging the resulting postings.
        for component in self.components:
            new_result = []
            postings = component.get_postings(index)
            first = 0
            second = 0
            while first < len(result) and second < len(postings):
                if result[first].doc_id < postings[second].doc_id:
                    new_result.append(result[first])
                    first += 1
                elif result[first].doc_id > postings[second].doc_id:
                    new_result.append(postings[second])
                    second += 1
                elif result[first].doc_id == postings[second].doc_id:
                    new_result.append(result[first])
                    first += 1
                    second += 1
            if (first >= len(result)):
                new_result = new_result + postings[second:]
            elif (second >= len(postings)):
                new_result = new_result + result[first:]
            result = new_result.copy()
                

        return result

    def __str__(self):
        return "(" + " OR ".join(map(str, self.components)) + ")"

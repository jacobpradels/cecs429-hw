from queries.termliteral import TermLiteral
from queries.RankedQuery import RankedQuery
from . import QueryComponent
class RankedRetrievalParser:
    def parse_query(self, query : str, processor, corpus_size) -> QueryComponent:
        query = RankedQuery(query,processor, corpus_size)
        return query
        # print(components)
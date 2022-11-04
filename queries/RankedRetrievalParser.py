from queries.termliteral import TermLiteral
from queries.RankedQuery import RankedQuery
from . import QueryComponent
class RankedRetrievalParser:
    def parse_query(self, query : str, processor) -> QueryComponent:
        query = RankedQuery(query,processor)
        return query
        # print(components)
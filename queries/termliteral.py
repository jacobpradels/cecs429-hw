from indexing.postings import Posting
from .querycomponent import QueryComponent
from text import TokenProcessor

class TermLiteral(QueryComponent):
    """
    A TermLiteral represents a single term in a subquery.
    """

    def __init__(self, term : str, processor : TokenProcessor):
        self.processor = processor
        self.term = self.processor.process_token_keep_hyphen(term)

    def get_postings(self, index) -> list[Posting]:
        return index.get_postings_no_pos(self.term)

    def __str__(self) -> str:
        return self.term
    
    def __eq__(self, other) -> bool:
        return self.term == other.term
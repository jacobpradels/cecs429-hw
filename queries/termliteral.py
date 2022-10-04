from indexing.postings import Posting
from .querycomponent import QueryComponent
from text.bettertokenprocessor import BetterTokenProcessor

class TermLiteral(QueryComponent):
    """
    A TermLiteral represents a single term in a subquery.
    """

    def __init__(self, term : str):
        token_processor = BetterTokenProcessor()
        self.term = token_processor.process_token_keep_hyphen(term)

    def get_postings(self, index) -> list[Posting]:
        return index.get_postings(self.term)

    def __str__(self) -> str:
        return self.term
    
    def __eq__(self, other) -> bool:
        return self.term == other.term
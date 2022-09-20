class Posting:
    """A Posting encapulates a document ID associated with a search query component."""
    def __init__(self, doc_id : int):
        self.doc_id = doc_id

    def __eq__(self, other):
        if not isinstance(other, Posting):
            return NotImplemented
        return self.doc_id == other.doc_id

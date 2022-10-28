from typing import Type


class Posting:
    """A Posting encapulates a document ID associated with a search query component."""
    def __init__(self, doc_id : int, position=-1, tftd=None):
        self.doc_id = doc_id
        self.tftd = tftd
        if isinstance(position,int):
            self.positions = [position]
        elif isinstance(position,list):
            self.positions = position
        else:
            raise(TypeError(f"Inappropriate argument type. Expected int or list[int] received {type(position)}"))
    
    def add_position(self, position : int):
        self.positions.append(position)

    def __eq__(self, other):
        if not isinstance(other, Posting):
            return NotImplemented
        return self.doc_id == other.doc_id and self.positions == other.positions

    def __str__(self):
        if (self.positions != [-1]):
            return f"({self.doc_id} : {self.positions})"
        else:
            return f"({self.doc_id} : tftd: {self.tftd})"
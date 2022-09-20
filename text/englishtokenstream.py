from email.generator import Generator
from typing import Iterator
from .tokenstream import TokenStream

class EnglishTokenStream(TokenStream):
    def __init__(self, source):
        """Constructs a stream over a TextIOWrapper of text"""
        self.source = source
        self._open = False

    def __iter__(self) -> Iterator[str]:
        """Returns an iterator over the tokens in the stream."""
        # The source iterator probably returns lines of text, not words.
        # Get the next line, then yield each token from it.
        words_seen = 0
        for token in self.source:
            # Used to determine position
            words_on_line = token.split(" ")
            # Removing all empty strings so they don't mess up position
            words_on_line = [x for x in words_on_line if len(x) > 0]
            for position, t in enumerate(words_on_line):
                tok = t.strip()
                yield (tok,position + words_seen)
            words_seen += len(words_on_line)


    # Resource management functions.
    def __enter__(self):
        self.source.__enter__()

    def __exit__(self):
        if self._open:
            self._open = False
            self.source.__exit__()

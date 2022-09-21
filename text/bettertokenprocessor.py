from typing import Iterator
from .tokenprocessor import TokenProcessor
import re
from porter2stemmer import Porter2Stemmer


class BetterTokenProcessor(TokenProcessor):
    """A BetterTokenProcessor creates terms from tokens by:

    1. Removing all non-alphanumeric characters from the beginning and end of the token
    2. Remove all apostrophes or quotation marks (single or double) from anywhere in the string
    3. For hypens in words, do both:
        1. Remove the hyphens from the token and then proceed with the modified token.
        2. Split the original hyphenated token into multiple tokens without a hyphen, and proceed with all 
        split tokens.
    4. Convert the token to lowercase
    5. Stem the token using an implementation of Porter2 stemmer."""
    whitespace_re = re.compile(r"\W+")
    not_alphanum_re = re.compile(r"^[^\w]+|([^\w]*$)")

    stemmer = Porter2Stemmer()
    
    def strip_non_alphanum(self, token : str) -> str:
        token = re.sub(self.not_alphanum_re,"", token)
        return token
    
    def strip_quotes(self, token : str) -> str:
        token = token.strip("'").strip("\"")
        return token
    
    def strip_hyphens(self, token : str) -> Iterator[str]:
        full_token = re.sub('-','',token)
        seperate_tokens = []
        if ("-" in token):
            seperate_tokens = token.split("-")
        return [full_token] + seperate_tokens

    def process_token(self, token : str) -> Iterator[str]:
        # 1. Removing all non-alphanumeric characters from the beginning and end of the token
        out = self.strip_non_alphanum(token)
        # 2. Remove all apostrophes or quotation marks (single or double) from anywhere in the string
        out = self.strip_quotes(out)
        # 3. For hypens
        out_list = self.strip_hyphens(out)
        # 4. Convert the token to lowercase
        out_list = [token.lower() for token in out_list]
        # 5. Stem the token using an implementation of Porter2 stemmer
        out_list = [self.stemmer.stem(token) for token in out_list]
        return out_list

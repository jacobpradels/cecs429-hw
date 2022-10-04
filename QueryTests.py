from lib2to3.pgen2 import token
from unittest import TestCase
from unittest.mock import MagicMock
import unittest.main
from unittest.mock import MagicMock
from indexing import Posting
from indexing.positionalinvertedindex import PositionalInvertedIndex
from documents import DirectoryCorpus
from text.englishtokenstream import EnglishTokenStream
from pathlib import Path
from queries import BooleanQueryParser, booleanqueryparser
from text.bettertokenprocessor import BetterTokenProcessor
class QueryOutputTests(unittest.TestCase):

    d = DirectoryCorpus.load_text_directory(Path("tests/test_corpus"),".txt")
    inverted_index = PositionalInvertedIndex()
    token_processor = BetterTokenProcessor()
    for document in d:
        stream = EnglishTokenStream(document.get_content())
        for position,term in enumerate(stream):
            for processed_term in token_processor.process_token(term):
                inverted_index.addTerm(processed_term, document.id, position)
    boolqueryparser = BooleanQueryParser()
    def test_or_query(self):
        # ARRANGE
        query_string = "apple + mango"
        query = self.boolqueryparser.parse_query(query_string)
        expected_postings = [Posting(1,[2,3,4]),Posting(2,[1]),Posting(3,0)]
        # ACT
        test_postings = query.get_postings(self.inverted_index)

        # ASSERT
        self.assertEqual(expected_postings,test_postings)
    
    def test_and_query(self):
        # ARRANGE
        query_string = "apple mango"
        query = self.boolqueryparser.parse_query(query_string)
        expected_postings = [Posting(1,[2,3])]
        # ACT
        test_postings = query.get_postings(self.inverted_index)

        # ASSERT
        self.assertEqual(expected_postings,test_postings)
    
    def test_phrase_query(self):
        # ARRANGE
        query_string = "\"apple mango\""
        query = self.boolqueryparser.parse_query(query_string)
        expected_postings = [Posting(1,3)]
        # ACT
        test_postings = query.get_postings(self.inverted_index)

        # ASSERT
        self.assertEqual(expected_postings,test_postings)

unittest.main()
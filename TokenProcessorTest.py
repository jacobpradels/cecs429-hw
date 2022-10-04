import unittest.main
from documents.directorycorpus import DirectoryCorpus
from indexing.invertedindex import InvertedIndex
from indexing.postings import Posting
from text.basictokenprocessor import BasicTokenProcessor
from text.bettertokenprocessor import BetterTokenProcessor
from text.englishtokenstream import EnglishTokenStream
from pathlib import Path


class TestTokenProcessorMethods(unittest.TestCase):
    token_processor = BetterTokenProcessor()

    def test_strip_quotes_quotes(self):
        expected_output = "test"
        test_string = "\"" + expected_output + "\""
        test_output = self.token_processor.strip_quotes(test_string)
        self.assertEqual(test_output,expected_output)
    
    def test_strip_quotation_apostrophe(self):
        expected_output = "test"
        test_string = "'" + expected_output + "'"
        test_output = self.token_processor.strip_quotes(test_string)
        self.assertEqual(test_output,expected_output)
    
    def test_strip_hyphens(self):
        expected_output = ["testword","test","word"]
        test_string = "test-word"
        test_output = self.token_processor.strip_hyphens(test_string)
        self.assertEqual(test_output,expected_output)
    
    def test_strip_non_alpha_num(self):
        # Leading whitespace
        expected_output = "word"
        test_string = "  word"
        test_output = self.token_processor.strip_non_alphanum(test_string)
        self.assertEqual(test_output,expected_output)

        # Trailing whitespace
        test_string = "word  "
        test_output = self.token_processor.strip_non_alphanum(test_string)
        self.assertEqual(test_output,expected_output)

        # Trailing whitespace
        expected_output = "192.168.1.1"
        test_string = "192.168.1.1"
        test_output = self.token_processor.strip_non_alphanum(test_string)
        self.assertEqual(test_output,expected_output)

        expected_output = "test-word.com"
        test_string = "!@#$test-word.com$$"
        test_output = self.token_processor.strip_non_alphanum(test_string)
        self.assertEqual(test_output,expected_output)
    
    def test_process_token(self):
        expected_output = ["testword.com","test","word.com"]
        test_string = "!@#$test-word.com!@$!@"
        test_output = self.token_processor.process_token(test_string)
        self.assertEqual(test_output,expected_output)
        
    

unittest.main()
import unittest.main
from documents.directorycorpus import DirectoryCorpus
from indexing.invertedindex import InvertedIndex
from indexing.postings import Posting
from text.basictokenprocessor import BasicTokenProcessor
from text.englishtokenstream import EnglishTokenStream
from pathlib import Path


class TestStringMethods(unittest.TestCase):
    def test_index(self):
        corpus = DirectoryCorpus.load_text_directory(Path("./tests/test_corpus"), ".txt")
        token_processor = BasicTokenProcessor()
        inverted_index = InvertedIndex()

        for d in corpus:
            processor = EnglishTokenStream(d.get_content())
            for term in processor:
                inverted_index.addTerm(token_processor.process_token(term),d.id)
        test_output = inverted_index.get_postings("apple")
        expected_output = [Posting(1),Posting(2),Posting(3)]
        self.assertEqual(test_output, expected_output)

unittest.main()
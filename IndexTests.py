from operator import index
import unittest.main
from unittest.mock import MagicMock
from indexing import Posting
from indexing.DiskIndexWriter import DiskIndexWriter
from indexing.positionalinvertedindex import PositionalInvertedIndex
from indexing.DiskPositionalIndex import DiskPositionalIndex
from documents import DirectoryCorpus
from text.englishtokenstream import EnglishTokenStream
from pathlib import Path

class PositionalInvertedIndexTests(unittest.TestCase):
    expected_index = {
        'lemon':[Posting(0,0),Posting(2,2),Posting(4,2)],
        'lime':[Posting(0,1),Posting(3,1),Posting(4,0)],
        'dragonfruit':[Posting(0,2),Posting(1,0)],
        'pineapple':[Posting(0,3)],
        'strawberry':[Posting(1,1),Posting(2,0),Posting(4,1)],
        'apple':[Posting(1,[2,3]),Posting(2,1),Posting(3,0)],
        'mango':[Posting(1,4)],
        'grape':[Posting(2,3)],
        'guava':[Posting(3,2)],
        'kiwi':[Posting(3,3)],
        'orange':[Posting(4,3)]
    }

    def test_construct_index(self):
        # ARRANGE
        d = DirectoryCorpus.load_text_directory(Path("tests/test_corpus"),".txt")
        inverted_index = PositionalInvertedIndex()

        expected_index = PositionalInvertedIndex()
        expected_index._index = self.expected_index

        # ACT
        for document in d:
            processor = EnglishTokenStream(document.get_content())
            for position,term in enumerate(processor):
                inverted_index.addTerm(term, document.id, position)
        
        # ASSERT
        # Test that the two indexes are equal
        self.assertEqual(expected_index,inverted_index)

        # Test that postings for apple are the same
        expected_postings = expected_index.get_postings('apple')
        test_postings = inverted_index.get_postings('apple')
        for p in test_postings:
            print(p)
        self.assertEqual(expected_postings,test_postings)

        # Test that postings for strawberry are the same
        expected_postings = expected_index.get_postings('strawberry')
        test_postings = inverted_index.get_postings('strawberry')
        self.assertEqual(expected_postings,test_postings)
        
        # Test that vocabulary is the same for each index
        expected_vocabulary = expected_index.vocabulary()
        test_vocabulary = inverted_index.vocabulary()
        self.assertEqual(expected_vocabulary,test_vocabulary)

        # Test that index can return list without postings
        expected_vocabulary = expected_index.get_postings_no_pos('strawberry')
        test_vocabulary = inverted_index.get_postings_no_pos('strawberry')
    
    # def test_disk_write_index(self):
    #     d = DirectoryCorpus.load_text_directory(Path("tests/test_corpus"),".txt")
    #     inverted_index = PositionalInvertedIndex()

    #     expected_index = PositionalInvertedIndex()
    #     expected_index._index = self.expected_index

    #     # ACT
    #     for document in d:
    #         processor = EnglishTokenStream(document.get_content())
    #         for position,term in enumerate(processor):
    #             inverted_index.addTerm(term, document.id, position)
        
    #     index_writer = DiskIndexWriter()
    #     index_writer.writeIndex(inverted_index,Path("./postings.bin"))
    
    def test_disk_read_index(self):
        index = DiskPositionalIndex()
        test_postings = index.get_postings_no_pos("appl")
        vocab = index.vocabulary()
        # print(vocab)

        # for p in test_postings:
            # print(p)
        
        
unittest.main()

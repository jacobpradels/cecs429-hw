import unittest.main
from unittest.mock import MagicMock
from queries import *
from indexing import Posting
from queries import orquery
from porter2stemmer import Porter2Stemmer
from text.bettertokenprocessor import BetterTokenProcessor


class BooleanQueryParserTests(unittest.TestCase):
    processor = BetterTokenProcessor()
    def test_term_literal(self):
        expected_output = BooleanQueryParser._Literal(BooleanQueryParser._StringBounds(0,4),TermLiteral("dog_asdf"))
        test_output = BooleanQueryParser._find_next_literal("   dog_asdf",0,self.processor)
        self.assertEqual(test_output.literal_component,expected_output.literal_component)


    def test_phrase_literal(self):
        expected_output = BooleanQueryParser._Literal(BooleanQueryParser._StringBounds(0,4),PhraseLiteral(["national","park"],self.processor))
        test_output = BooleanQueryParser._find_next_literal("\"national park\"",0, self.processor)
        print(f"test : {test_output.literal_component} \nexpected : {expected_output.literal_component}")
        self.assertEqual(test_output.literal_component,expected_output.literal_component)
    
class OrQueryTests(unittest.TestCase):
    processor = BetterTokenProcessor()
    def test_merge_positions(self):
        pos1 = [1,3,6]
        pos2 = [2,3,5,9,18]
        expected_output = [1,2,3,5,6,9,18]
        test_output = orquery.merge_positions(pos1,pos2)
        self.assertEqual(expected_output,test_output)
    
    

    def test_orquery_get_postings(self):
        # ARRANGE
        # MOCK DATA
        def test_orquery_get_postings_helper(input):
            if input == "jacob":
                return [Posting(1,[15,111]),Posting(2,32),Posting(4,22)]
            elif input == "hello":
                return [Posting(1,17),Posting(3,32),Posting(5,15)]
            elif input == "applesauc":
                return [Posting(2,17),Posting(5,32),Posting(7,15)]
        mock_index = MagicMock()
        mock_index.get_postings = MagicMock(side_effect=test_orquery_get_postings_helper)
        components = [TermLiteral("jacob",self.processor),TermLiteral("Hello",self.processor),TermLiteral("Applesauce",self.processor)]

        posting_1 = Posting(1,[15,17,111])
        posting_2 = Posting(2,[17,32])
        posting_3 = Posting(3,32)
        posting_4 = Posting(4,22)
        posting_5 = Posting(5,[15,32])
        posting_7 = Posting(7,15)

        expected_postings = [posting_1,posting_2,posting_3,posting_4,posting_5,posting_7]    
        # ACT
        query = OrQuery(components)
        test_postings = query.get_postings(mock_index)

        # ASSERT
        self.assertEqual(expected_postings,test_postings)

    def test_andquery_get_postings(self):
        # ARRANGE
        # MOCK DATA
        def test_andquery_get_postings_helper(input):
            if input == "jacob":
                return [Posting(1,[15,111]),Posting(2,[17,32]),Posting(4,22)]
            elif input == "hello":
                return [Posting(1,[9,15,22]),Posting(2,[17,32]),Posting(5,[15,32])]

        mock_index = MagicMock()
        mock_index.get_postings = MagicMock(side_effect=test_andquery_get_postings_helper)
        components = [TermLiteral("jacob",self.processor),TermLiteral("Hello",self.processor)]

        posting_1 = Posting(1,15)
        posting_2 = Posting(2,[17,32])

        expected_postings = [posting_1,posting_2]    
        # ACT
        query = AndQuery(components)
        test_postings = query.get_postings(mock_index)

        # ASSERT
        self.assertEqual(expected_postings,test_postings)
    
    def test_phrasequery_get_postings(self):
        # ARRANGE
        stemmer = Porter2Stemmer()
        # MOCK DATA
        def test_andquery_get_postings_helper(input):
            if input == stemmer.stem("jacob"):
                return [Posting(1,[15])]
            elif input == stemmer.stem("hello"):
                return [Posting(1,[14])]
            elif input == stemmer.stem("ryan"):
                return [Posting(1,[16])]

        mock_index = MagicMock()
        mock_index.get_postings = MagicMock(side_effect=test_andquery_get_postings_helper)
        components = [PhraseLiteral(["Hello","jacob","ryan"],self.processor)]

        posting_1 = Posting(1,14)

        expected_postings = [posting_1]    
        # ACT
        query = AndQuery(components)
        test_postings = query.get_postings(mock_index)

        # print("".join(map(str,expected_postings)))
        # print("".join(map(str,test_postings)))
        # ASSERT
        self.assertEqual(expected_postings,test_postings)
    
    

unittest.main()

pos1 = [1,3,6]
pos2 = [2,3,5,9,18]
expected_output = [1,2,3,5,6,9,18]
test_output = orquery.merge_positions(pos1,pos2)
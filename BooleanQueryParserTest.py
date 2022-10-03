import unittest.main
from queries import *
from indexing import Posting
from queries import orquery

class BooleanQueryParserTests(unittest.TestCase):

    def test_term_literal(self):
        expected_output = BooleanQueryParser._Literal(BooleanQueryParser._StringBounds(0,4),TermLiteral("dog_asdf"))
        test_output = BooleanQueryParser._find_next_literal("   dog_asdf",0)
        self.assertEqual(test_output.literal_component,expected_output.literal_component)


    def test_phrase_literal(self):
        expected_output = BooleanQueryParser._Literal(BooleanQueryParser._StringBounds(0,4),PhraseLiteral(["padres","win"]))
        test_output = BooleanQueryParser._find_next_literal("     \"padres win\"       ",0)
        print(f"test : {test_output.literal_component} \nexpected : {expected_output.literal_component}")
        self.assertEqual(test_output.literal_component,expected_output.literal_component)

class OrQueryTests(unittest.TestCase):

    # def test_or_query(self):
    #     test_Posting1 = Posting(1,2)
    #     test_Posting1.add_position(3)
    #     test_Posting2 = Posting(1,4)
    #     test_Posting3 = Posting(2,3)
    #     test_Posting4 = Posting(3,2)

    #     expected_Posting1 = Posting(1,2)
    #     expected_Posting1.add_position(3)
    #     expected_Posting1.add_position(4)
    #     expected_Posting2 = Posting(2,3)
    #     expected_Posting3 = Posting(3,2)


    #     expected_output = [expected_Posting1]
    #     test_output = OrQuery.or_reduce_postings([test_Posting1],[test_Posting2])
    #     print(f"test : {test_output[0]} \nexpected : {expected_output[0]}")
    #     self.assertEqual(expected_output,test_output)

    def test_merge_positions(self):
        pos1 = [1,3,6]
        pos2 = [2,3,5,9,18]
        expected_output = [1,2,3,5,6,9,18]
        test_output = orquery.merge_positions(pos1,pos2)
        self.assertEqual(expected_output,test_output)
unittest.main()

pos1 = [1,3,6]
pos2 = [2,3,5,9,18]
expected_output = [1,2,3,5,6,9,18]
test_output = orquery.merge_positions(pos1,pos2)
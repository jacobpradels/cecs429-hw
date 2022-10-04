from configparser import BasicInterpolation
from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus, jsonfiledocument
from indexing import Index, TermDocumentIndex
from text import BasicTokenProcessor, englishtokenstream
from text import bettertokenprocessor
from indexing.invertedindex import InvertedIndex
from indexing.positionalinvertedindex import PositionalInvertedIndex
from queries import *

def index_corpus(corpus : DocumentCorpus) -> Index:
    token_processor = bettertokenprocessor.BetterTokenProcessor()
    inverted_index = PositionalInvertedIndex()

    for d in corpus:
        processor = englishtokenstream.EnglishTokenStream(d.get_content())
        for position,term in enumerate(processor):
            for processed_term in token_processor.process_token(term):
                inverted_index.addTerm(processed_term,d.id, position)

    return(inverted_index)
def main():
    corpus_path = Path("./test_nps")
    # corpus_path = Path("./nps_sites")
    d = DirectoryCorpus.load_json_directory(corpus_path, ".json")

    # Build the index over this directory.
    index = index_corpus(d)

    bqp = BooleanQueryParser()
    query_string = input("Enter query ")
    while (query_string != ""):
        query = bqp.parse_query(query_string)
        postings = query.get_postings(index)
        for p in postings:
            print(p.doc_id,end="->[")
            for pos in p.positions:
                print(pos,end=",")
            print("]")
        query_string = input("Enter query ")
main()

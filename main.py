from configparser import BasicInterpolation
from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus, jsonfiledocument
from indexing import Index, TermDocumentIndex
from text import BasicTokenProcessor, englishtokenstream
from text import bettertokenprocessor
from indexing.invertedindex import InvertedIndex
from indexing.positionalinvertedindex import PositionalInvertedIndex
from queries import *
from porter2stemmer import Porter2Stemmer
import time


def index_corpus(corpus : DocumentCorpus) -> Index:
    token_processor = bettertokenprocessor.BetterTokenProcessor()
    inverted_index = PositionalInvertedIndex()
    print("Indexing...")
    for d in corpus:
        processor = englishtokenstream.EnglishTokenStream(d.get_content())
        for position,term in enumerate(processor):
            for processed_term in token_processor.process_token(term):
                inverted_index.addTerm(processed_term,d.id, position)
    print("Done")
    print(f"Found {len(corpus)} documents")

    return(inverted_index)



def main():
    stemmer = Porter2Stemmer()
    corpus = input("Enter corpus path: ")
    corpus_path = Path(corpus)
    d = DirectoryCorpus.load_json_directory(corpus_path, ".json")

    # Build the index over this directory, recording time taken.
    start = time.time()
    index = index_corpus(d)
    end = time.time()
    print("Time to index = {:.2f} seconds".format(end-start))

    booleanqueryparser = BooleanQueryParser()
    query_string = ""

    while (query_string != ":q"):
        query_string = input("> ")

        if (query_string == ":q"):
            return
        elif (query_string[0:5] == ":stem"):
            
            print(stemmer.stem(query_string[6:]))
        elif (query_string[0:6] == ":index"):
            corpus = query_string[7:]
            d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
            start = time.time()
            index = index_corpus(d)
            end = time.time()
            print("Time to index = {:.2f} seconds".format(end-start))
        else:
            query = booleanqueryparser.parse_query(query_string)
            postings = query.get_postings(index)
            for post in postings:
                document = d.get_document(post.doc_id)
                print(document)
            print(f"{len(postings)} documents")
            chosen_document = eval(input("Enter document id to view (-1 to skip viewing) "))
            if (chosen_document != -1):
                for line in d.get_document(chosen_document).get_content():
                    print(line)
main()

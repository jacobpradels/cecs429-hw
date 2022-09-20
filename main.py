from configparser import BasicInterpolation
from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus, jsonfiledocument
from indexing import Index, TermDocumentIndex
from text import BasicTokenProcessor, englishtokenstream
from indexing.invertedindex import InvertedIndex

def index_corpus(corpus : DocumentCorpus) -> Index:
    token_processor = BasicTokenProcessor()
    inverted_index = InvertedIndex()

    for d in corpus:
        processor = englishtokenstream.EnglishTokenStream(d.get_content())
        for term in processor:
            inverted_index.addTerm(token_processor.process_token(term),d.id)

    return(inverted_index)
def main():
    # corpus_path = Path()
    corpus_path = Path("./nps_sites")
    # corpus_path = Path("./test_nps")
    # d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")
    d = DirectoryCorpus.load_json_directory(corpus_path, ".json")

    # Build the index over this directory.
    index = index_corpus(d)

    # We aren't ready to use a full query parser;
    # for now, we'll only support single-term queries.
    query = "national" # hard-coded search for "whale"
    for p in index.get_postings(query):
        doc = d.get_document(p.doc_id)
        print(doc.title)

main()

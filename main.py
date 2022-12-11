from configparser import BasicInterpolation
from lib2to3.pgen2 import token
import math
from pathlib import Path
import struct
from documents import DocumentCorpus, DirectoryCorpus, jsonfiledocument
from indexing import Index, TermDocumentIndex
from text import BasicTokenProcessor, englishtokenstream
from text.bettertokenprocessor import BetterTokenProcessor
from indexing.invertedindex import InvertedIndex
from indexing.positionalinvertedindex import PositionalInvertedIndex
from indexing.DiskIndexWriter import DiskIndexWriter
from indexing.DiskPositionalIndex import DiskPositionalIndex
from queries import RankedRetrievalParser
from queries import *
from porter2stemmer import Porter2Stemmer
from matplotlib import pyplot as plt
from fractions import Fraction
import numpy as np
import time


def index_corpus(corpus : DocumentCorpus) -> Index:
    token_processor = BetterTokenProcessor()
    inverted_index = PositionalInvertedIndex()
    print("Indexing...")
    with open("doc_Weights.bin","wb") as file:
        for d in corpus:
            total = 0
            stream = englishtokenstream.EnglishTokenStream(d.get_content())
            term_count = {}
            for position,term in enumerate(stream):
                for processed_term in token_processor.process_token(term):
                    inverted_index.addTerm(processed_term,d.id, position)
                    try:
                        term_count[processed_term] += 1
                    except KeyError:
                        term_count[processed_term] = 1
            for key,val in term_count.items():
                # print(f'[{key} - {val}]')
                wdt = 1 + math.log(val)
                total += (wdt**2)
            Ld = math.sqrt(total)
            file.write(struct.pack('>d',Ld))
    
    print("Done")
    print(f"Found {len(corpus)} documents")
    index_writer = DiskIndexWriter()
    index_writer.writeIndex(inverted_index,Path("./postings.bin"))
    return(inverted_index)



def main():
    stemmer = Porter2Stemmer()
    token_processor = BetterTokenProcessor()
    index = None
    corpus = input("Enter corpus path: ")
    corpus_path = Path(corpus)
    choice = eval(input("1.Build an index\n2.Query an index\n"))
    d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
    if (len(d.documents()) == 0):
        d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")
    N = 0
    if choice == 1:
        # Build the index over this directory, recording time taken.
        start = time.time()
        mem_index = index_corpus(d)
        index = DiskPositionalIndex(token_processor)
        end = time.time()
        print("Time to index = {:.2f} seconds".format(end-start))
    else:
        index = DiskPositionalIndex(token_processor)

    mode = eval(input("1. Boolean Query Mode\n2. Ranked Retrieval Mode\n"))
    if mode == 1:
        queryparser = BooleanQueryParser()
    elif mode == 2:
        queryparser = RankedRetrievalParser.RankedRetrievalParser()
    else:
        print('Invalid option.')
        exit()
    query_string = ""

    while (query_string != ":q"):
        # Get input
        query_string = input("> ")

        # Close program
        if (query_string == ":q"):
            break
        # Run stemmer
        elif (query_string[0:5] == ":stem"):
            print(stemmer.stem(query_string[6:]))
        
        # Index new corpus
        elif (query_string[0:6] == ":index"):
            corpus_path = query_string[7:]
            d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
            if (len(d.documents()) == 0):
                d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")
            start = time.time()
            index = index_corpus(d)
            end = time.time()
            print("Time to index = {:.2f} seconds".format(end-start))
        
        # Display vocabulary
        elif (query_string == ":vocab"):
            for word in index.vocabulary()[:1001]:
                print(word)
            print(f"Vocabulary has {len(index.vocabulary())} words")
        elif (query_string ==  ":map"):
            if (mode == 1):
                print("Map only available in ranked retrieval mode.")
                continue
            start = time.time()
            listOfQueries = []
            listOfRelevant = []
            queryText = ""
            relevantDocuments = []
            with open("relevant/relevance/queries","r") as queries:
                listOfQueries = queries.readlines()
            with open("relevant/relevance/qrel","r") as qrel:
                listOfRelevant = qrel.readlines()
            
            listOfQueries = [x.strip() for x in listOfQueries]
            AveragePrecisionAccumulator = 0
            for queryText,relevantDocuments in zip(listOfQueries,listOfRelevant):
                relevantDocuments = relevantDocuments.split()
                relevantDocuments = [eval(x) for x in relevantDocuments]
                query = queryparser.parse_query(queryText, token_processor)
                postings = query.get_postings(index)
                relCount = 0
                PrecisionAccumulator = 0
                for i,post in enumerate(postings):
                    doc = d.get_document(post.doc_id)
                    # print(doc.path)
                    # docNumber = eval(str(doc.path)[9:-5])
                    if doc.id in relevantDocuments:
                        # print("rel:",doc.id)
                        relCount += 1
                        PrecisionAccumulator += relCount / (i + 1)
                    # else:
                        # print("nr",docNumber)
                try:
                    AP = PrecisionAccumulator/relCount
                except ZeroDivisionError:
                    AP = 0
                AveragePrecisionAccumulator += AP
            end = time.time()
            MAP = AveragePrecisionAccumulator / len(listOfQueries)
            throughput = len(listOfQueries)/(end - start)
            responseTime = (end-start)/len(listOfQueries)
            out = [
                ["Throughput",throughput,"queries/second"],
                ["Response Time",responseTime,"seconds"],
                ["MAP",MAP,""]
            ]
            for line in out:
                print("{0:<15} {1:<8.4f} {2:<8}".format(*line))
        elif (query_string == ":thr"):
            if (mode == 1):
                print("Map only available in ranked retrieval mode.")
                continue
            start = time.time()
            for x in range(1):
                queryText = ""
                relevantDocuments = []
                with open("relevant/relevance/queries","r") as queries:
                    queryText = queries.readlines()[0]
                with open("relevant/relevance/qrel","r") as qrel:
                    relevantDocuments = qrel.readlines()[1]
                
                query = queryparser.parse_query(queryText, token_processor)
                postings = query.get_postings(index)
                PrecisionAccumulator = 0
                relCount = 0
                for i,post in enumerate(postings):
                        doc = d.get_document(post.doc_id)
                        # print(doc.path)
                        # docNumber = eval(str(doc.path)[9:-5])
                        if str(doc.id) in relevantDocuments:
                            print("{} - {:.4f} {}".format(doc,-post.score,"Relevant"))
                            # print(doc," -- ",-post.score,"Relevant")
                            relCount += 1
                            PrecisionAccumulator += relCount / (i + 1)
                        else:
                            print("{} - {:.4f} {}".format(doc,-post.score,"Not relevant"))
                            # print(doc," -- ",-post.score,"Not relevant")
                try:
                    AP = PrecisionAccumulator/relCount
                except ZeroDivisionError:
                    AP = 0
                # print(len(postings))
                # print(AP)
            end = time.time()
            duration = end - start
            throughput = 30/duration
            print(throughput)
        elif (query_string == ":graph"):
            queryText = ""
            relevantDocuments = []
            with open("relevant/relevance/queries","r") as queries:
                queryText = queries.readlines()[0]
            with open("relevant/relevance/qrel","r") as qrel:
                relevantDocuments = qrel.readlines()[1]
            
            query = queryparser.parse_query(queryText, token_processor)
            postings = query.get_postings(index)
            PrecisionAccumulator = 0
            prec_count = 0
            precision = []
            recall = []
            for i,post in enumerate(postings):
                doc = d.get_document(post.doc_id)
                if str(doc.id) in relevantDocuments:
                    prec_count += 1
                precision.append(prec_count/(i + 1))
                recall.append(prec_count/len(relevantDocuments))
            precision_frac = [Fraction(x).limit_denominator() for x in precision]
            plt.plot(recall,precision)
            plt.xlabel("Recall")
            plt.ylabel("Precision")
            plt.show()

        else:
            # Parse query
            query = queryparser.parse_query(query_string, token_processor)
            postings = query.get_postings(index)
            for post in postings:
                document = d.get_document(post.doc_id)
                if (mode == 1):
                    print(document)
                elif (mode == 2):
                    print(document," -- ",-post.score)
            print(f"{len(postings)} documents")
            chosen_document = eval(input("Enter document id to view (-1 to skip viewing) "))
            if (chosen_document != -1):
                for line in d.get_document(chosen_document).get_content():
                    print(line)
main()

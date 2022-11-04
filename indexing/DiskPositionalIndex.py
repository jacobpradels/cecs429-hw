# from bdb import GENERATOR_AND_COROUTINE_FLAGS
import sqlite3
import struct
from .index import Index
from typing import Iterable
from .postings import Posting

class DiskPositionalIndex(Index):
    
    def __init__(self, processor):
        self.processor = processor
        self.postings = None
        with open("postings.bin","rb") as file:
            self.postings = file.read()
    ########## HELPER FUNCTIONS ##########

    def read_next(self, postings, offset):
        """ Reads byte in postings file and advances offset variable """
        value = struct.unpack(">i",postings[offset:offset+4])[0]
        offset = offset + 4
        return value,offset
    
    def skip(self, n : int, offset : int):
        """
        Skips the offset tracker n 4 byte ints in postings.bin file
        """
        offset = offset + 4 * n
        return offset 

    def get_document(self, postings, offset):
        """
        Helper function for reading document postings on disk.
        Returns a tuple of form ({doc_id:List[Positions]},updated_offset)
        """
        positions = []
        doc_id,offset = self.read_next(postings, offset)
        tftd,offset = self.read_next(postings,offset)
        for x in range(tftd):
            next_gapped,offset = self.read_next(postings,offset)
            if positions:
                positions.append(next_gapped + positions[-1])
            else:
                positions.append(next_gapped)

        return ((doc_id,positions),offset)
    
    def get_document_no_pos(self, postings, offset):
        """
        Helper function for reading document postings on disk
        without positions.
        Returns a tuple of form (doc_id,updated_offset)
        """
        doc_id,offset = self.read_next(postings,offset)
        wdt = struct.unpack(">d",postings[offset:offset+8])[0]
        offset = offset + 8
        tftd,offset = self.read_next(postings,offset)
        offset = self.skip(tftd,offset)

        return (doc_id,offset,tftd,wdt)
    

    
    def get_term_position(self, term):
        """
        Get the position a term starts in postings.bin from the
        term_positions database.
        """
        term = self.processor.process_token_keep_hyphen(term)
        # Connect to the database
        con = sqlite3.connect("term_positions.db")
        cur = con.cursor()
        # Query database for location of term in postings.bin
        res = cur.execute("SELECT key,byte FROM term WHERE key=?",[term])
        position = res.fetchone()[1]
        # Convert position to decimal
        position = int(position[2:],16)
        return position

    def get_doc_weight(self, doc_id):
        with open("doc_Weights.bin","rb") as weights_file:
            weights = weights_file.read()
            position = (doc_id) * 8
            value = struct.unpack(">d",weights[position:position+8])[0]
            return value
    
    def get_doc_count(self):
        with open("doc_Weights.bin","rb") as weights_file:
            weights = weights_file.read()
            doc_count = len(weights)/8
            return doc_count

    ########## INHERITED FUNCTIONS ##########

    # dft - number of documents containing term
    # id - document id
    # tftd - number of times term appears in document
    # pi - position i in document
    def get_postings(self, term : str) -> Iterable[Posting]:
        final_postings = []
        position = self.get_term_position(term)

        # Open postings.bin
        # with open("postings.bin","rb") as postings_file:
        # postings = postings_file.read()
        # Find how many documents to cover and update position
        dft,position = self.read_next(self.postings, position)
        # Used to remove gap
        last_document = 0
        for document in range(dft):
            # Use helper function to get all positions in document
            tftd = self.get_document(self.postings, position)
            # Update the position for reading next int
            position = tftd[1]

            # Process and add to dictionary
            doc_id = tftd[0][0]
            term_positions = tftd[0][1]
            final_postings.append(Posting(doc_id + last_document,term_positions))
            last_document = doc_id + last_document
        return final_postings
    
    def get_postings_no_pos(self, term: str) -> Iterable[Posting]:
        final_postings = []
        position = self.get_term_position(term)

        # Open postings.bin
        # with open("postings.bin","rb") as postings_file:
        # postings = postings_file.read()
        # Find how many documents to cover
        dft,position = self.read_next(self.postings, position)

        # Used to remove gap
        last_document = 0
        for document in range(dft):
            # Use helper function to get all positions in document
            doc_info = self.get_document_no_pos(self.postings, position)
            # Update the position for reading next int
            position = doc_info[1]
            # Process and add to dictionary
            doc_id = doc_info[0]
            wdt = doc_info[3]
            final_postings.append(Posting(doc_id + last_document,tftd=doc_info[2],wdt=wdt))
            last_document = doc_id + last_document
        return final_postings
            


    def vocabulary(self) -> list[str]:
        # Connect to the database
        con = sqlite3.connect("term_positions.db")
        cur = con.cursor()
        # Query database for location of term in postings.bin
        res = cur.execute("SELECT key FROM term")
        vocab = [x[0] for x in res]
        print('vocab len',len(vocab))
        return vocab

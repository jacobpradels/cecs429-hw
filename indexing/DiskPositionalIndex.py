from bdb import GENERATOR_AND_COROUTINE_FLAGS
import sqlite3
import struct
from .index import Index
from typing import Iterable
from .postings import Posting

class DiskPositionalIndex(Index):
    
    def get_document(self, postings, offset):
        """
        Helper function for reading document postings on disk.
        Returns a tuple of form ({doc_id:List[Positions]},updated_offset)
        """
        positions = []
        doc_id = struct.unpack(">i",postings[offset:offset+4])[0]
        offset += 4
        tftd = struct.unpack(">i", postings[offset:offset+4])[0]
        offset += 4
        for x in range(tftd):
            next_gapped = struct.unpack(">i",postings[offset:offset+4])[0]
            if positions:
                positions.append(next_gapped + positions[-1])
            else:
                positions.append(next_gapped)
            offset = offset+4

        return ((doc_id,positions),offset)

    # dft - number of documents containing term
    # id - document id
    # tftd - number of times term appears in document
    # pi - position i in document
    def get_postings(self, term : str) -> Iterable[Posting]:
        final_postings = []
        # Connect to the database
        con = sqlite3.connect("term_positions.db")
        cur = con.cursor()
        # Query database for location of term in postings.bin
        res = cur.execute("SELECT key,byte FROM term WHERE key=?",[term])
        position = res.fetchone()[1]
        # Convert position to decimal
        position = int(position[2:],16)

        # Open postings.bin
        with open("postings.bin","rb") as postings_file:
            postings = postings_file.read()
            # Find how many documents to cover
            dft = struct.unpack(">i",postings[position:position+4])[0]
            # Increment position because we read that byte
            position = position + 4
            
            # Used to remove gap
            last_document = 0
            for document in range(dft):
                # Use helper function to get all positions in document
                tftd = self.get_document(postings, position)
                # Update the position for reading next int
                position = tftd[1]

                # Process and add to dictionary
                doc_id = tftd[0][0]
                term_positions = tftd[0][1]
                final_postings.append(Posting(doc_id + last_document,term_positions))
                last_document = doc_id + last_document
        return final_postings
            
            


    def vocabulary(self) -> list[str]:
        pass
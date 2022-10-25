from pathlib import Path
import struct
from indexing.positionalinvertedindex import PositionalInvertedIndex
import sqlite3


class DiskIndexWriter:

    def write(self,file, text):
        file.write(struct.pack(self.pack_format,text))
        self.byte_position += 4


    def writeIndex(self, index : PositionalInvertedIndex, path : Path):
        # Method variables
        self.byte_position = 0
        self.pack_format = '>i'

        count=0
        # Set up database
        con = sqlite3.connect("term_positions.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS term(key text, byte text)")
        con.commit()

        # Write to file
        with open(path, "wb") as file:
            vocab = index.vocabulary()
            for term in vocab:
                # Insert into database term and hex location in index
                cur.execute("INSERT INTO term VALUES (?,?)",[term,hex(self.byte_position)])
                con.commit()
                
                # Get postings for that term
                postings_list = index.get_postings(term)
                # print(f"----------{term}----------")
                # dft = # of documents containing term
                dft=len(postings_list)
                self.write(file,dft)
                # print(f"dft={dft}")

                # Track id and prev_id for gap
                id = 0
                prev_id = 0
                for posting in postings_list:
                    # Calculate gap
                    id = posting.doc_id - prev_id
                    # Store prev_id for next gap
                    prev_id = posting.doc_id

                    # Id = gapped document id
                    self.write(file,id)
                    # print(f"id={id}")

                    # tftd = # of times term occurs in document
                    tftd = len(posting.positions)
                    self.write(file,tftd)
                    # print(f"tftd={tftd}")

                    pos = 0
                    prev_pos = 0
                    for pi in posting.positions:
                        # pi = position of term in document
                        gap_pos = pi - prev_pos
                        prev_pos = pi
                        self.write(file,gap_pos)
                        # print(f"pi={gap_pos}")


                    # print(posting)
        # This is just here for debugging output
        # res = cur.execute("SELECT key,byte FROM term")
        # print(res.fetchall())
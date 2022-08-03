import json
import logging
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class amino_acid_count:
    """
    This is a class for the Amino Acid count functions

    Attributes:
        dna (str): Specify DNA strand sequence.
    """

    def __init__(self, dna: str):
        """
        The constructor for the class
        """
        self.DATA_PATH = os.path.join(BASE_DIR, "codon.json")
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()
        self.counter = dict()
        self.total = 0
        self.dna = dna.upper()

    def load_json(self):
        """
        The function to load the database content.

        Returns:
            codon_codes: An object that contains the contents of the database
        """
        try:
            with open(self.DATA_PATH, "r") as database:
                codon_codes = json.loads(database.read())
            return codon_codes
        except FileNotFoundError:
            print("Database not found")
            sys.exit(1)
        except OSError:
            print("Error opening database")
            sys.exit(1)

    def main(self):
        """
        The function that contains the logic of the class.

        It iteratively searches the condon chart database for
        instances where the dna nucleotide seqeunce is present.
        If true, a counter is incremented. The final value of the
        counter represents the number of times an amino acid is
        present in the dna strand.

        Sequence with less than 3 nucelotides is logged.

        Returns:
            ''
        """
        amino_acids = re.findall("." * 3, self.dna)
        codon_codes = self.load_json()

        for codon in amino_acids:
            if len(codon) < 3:
                self.logger.info(
                    f"Ignoring bases: {codon} with less than 3 nucelotides"
                )
            for codon_code in codon_codes:
                if codon in codon_codes[codon_code]:
                    if codon_code in self.counter:
                        self.counter[codon_code] += 1
                    else:
                        self.counter[codon_code] = 1
                    self.total += 1
                    break

        arranged = dict(
            sorted(self.counter.items(), reverse=True,
                   key=lambda item: item[1])
        )
        for codon_code in arranged:
            print(
                f"{codon_code} - {self.counter[codon_code]} ({self.counter[codon_code]/self.total*100:.1f} %)"
            )
        return


if __name__ == "__main__":
    aac_object = amino_acid_count("CTAGGACCG")
    aac_object.main()

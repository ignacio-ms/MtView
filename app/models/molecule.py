import requests
import json

from app import utils


class Molecule:
    def __init__(self):

        self.mol = None
        self.pae = None

    def set_mol(self, accession_id):
        """
        Gets the pdb data of the 3d molecule predicted from AplphafoldV2 via API.
        """
        url = f'https://alphafold.ebi.ac.uk/files/AF-{accession_id}-F1-model_v3.pdb'
        res = requests.get(url)
        if res.status_code != 200:
            print('Molecule not found')
            return

        print(f'Molecule found with accession id: {accession_id}')
        self.mol = res.text

    def set_pae(self, accession_id):
        """
        Gets the Predicted Aligned Error data of the 3d molecule predicted from AplphafoldV2 via API.
        """

        url = f'https://alphafold.ebi.ac.uk/files/AF-{accession_id}-F1-predicted_aligned_error_v3.json'
        res = requests.get(url)
        if res.status_code != 200:
            return

        self.pae = json.loads(res.text)[0]

    def get_mol(self):
        return self.mol

    def get_pae(self):
        return self.pae['predicted_aligned_error']

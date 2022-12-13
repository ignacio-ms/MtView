import requests
import json

import plotly.express as px
import plotly.utils

from app import values


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
            print('Molecule: Molecule not found')
            return False

        print(f'Molecule: Molecule found with accession id: {accession_id}')
        self.mol = res.text
        return True

    def set_pae(self, accession_id):
        """
        Gets the Predicted Aligned Error data of the 3d molecule predicted from AplphafoldV2 via API.
        """

        url = f'https://alphafold.ebi.ac.uk/files/AF-{accession_id}-F1-predicted_aligned_error_v3.json'
        res = requests.get(url)
        if res.status_code != 200:
            return

        self.pae = json.loads(res.text)[0]

    def init_pae(self, size=400):
        """
        Function to initialize the molecule Predicted Aligned Error heatmat.
        """

        fig = px.imshow(
            self.pae['predicted_aligned_error'],
            color_continuous_scale=values.color_scale,
            labels={'x': 'Scored esidue', 'y': 'Aligned residue', 'color': 'EPE (Angstroms)'}
        )

        fig.update_xaxes(title='Scored residue').update_yaxes(title='Aligned residue')
        fig.update_coloraxes(colorbar_title='Angstroms')
        fig.update_layout(
            height=size, width=size,
            title='Predicted aligned error',
            hovermode="closest",
            dragmode='select'
        )

        fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return fig_json

from __future__ import print_function


import requests
import os

import pandas as pd
import numpy as np
import json

from app import utils


class Taxonomy:
    def __init__(self):

        self.gene_names = pd.DataFrame()

        self.taxonomy = pd.DataFrame()
        self.expression = pd.DataFrame()

    def set_gene_names(self):
        """
        Reads all avaivable gene locus tags (Gene Names)
        """

        self.gene_names = pd.read_csv(os.path.join(os.getcwd(), 'app/static/data/gene_names.tsv'), sep='\t')

    @utils.timed
    def set_gene_taxonomy(self, gene_name, verbose=False):
        """
        Gets the taxonomy of a single gen from UniProt.
        Data will be estored in self Pandas DataFrame variable taxonomy.
        """

        gene_name = gene_name.replace(" ", "")  # White spaces fix

        url = f'https://rest.uniprot.org/uniprotkb/stream?fields=accession%2Cdate_modified%2Cid%2Cgene_orf%2Cgene_oln%2Ccc_function%2Ccc_tissue_specificity%2Ccc_induction%2Cgo%2Ccc_subcellular_location%2Clength%2Csequence&format=tsv&query=%28{gene_name}%29'
        res = requests.get(url)
        line = res.text.splitlines()

        try:  # Check of data availability in Dataset
            cols = line[0].split('\t')
            line = np.array(line[1].split('\t'))

            print(f'Gene found with accession id: {line[0]}')
            self.taxonomy = pd.DataFrame(line.reshape((1, -1)), columns=cols)

            if verbose:
                print(self.taxonomy.head())

            return True
        except IndexError:
            print('Gene not found')
            return False

    @utils.timed
    def set_gene_expression(self, gene_name, verbose=False):
        """
        Gets expression of a single gen from ExpressionAtlas.
        Data will be estored in self Pandas DataFrame variable expression.
        """

        gene_name = gene_name.replace(" ", "")  # White spaces fix

        url = f'https://lipm-browsers.toulouse.inra.fr/expression-atlas-api/public/v3/zz_complete_dataset/{gene_name}/byReplicate'
        res = requests.get(url)
        lines = res.text.splitlines()[3:]

        cols = lines[0].split(sep='\t')[1:]
        if len(cols) <= 1:  # Check of data availability in Dataset
            print('Gene not found')
            return False
        print('Gene found.')

        log2_tmm = lines[1].split(sep='\t')[1:]
        tmm = lines[3].split(sep='\t')[1:]
        self.expression = pd.DataFrame(list(zip(*zip(log2_tmm, tmm))), columns=cols, index=['log2_tmm', 'tmm'])

        if verbose:
            print(self.expression.head())
        return True

    def filter_by_experiment(self, experiment, verbose=False):
        """
        Filters gene expression by a single experiment
        """

        if self.expression.empty:  # Chech for empty expression data
            print('No expression data available to filter.')
            return

        filtered = self.expression[[exp for exp in self.expression.columns if exp.startswith(f'{experiment}')]]
        if filtered.empty:  # Chech for existing experiment
            print('Not existing experiment for current gene.')
            return

        # Delete experiment name from columns
        pd.options.mode.chained_assignment = None
        for col in filtered.columns:
            _, c_type = col.split(':')
            filtered.rename(columns={col: c_type}, inplace=True)
        pd.options.mode.chained_assignment = 'warn'

        if verbose:
            print(f'Experiment {experiment} found:')
            print(filtered.head())
        return filtered

    @staticmethod
    def get_experiments_info(proyect_id, field):
        """
        Gets the categories of a given experiment.
        """

        url = 'https://lipm-browsers.toulouse.inra.fr/expression-atlas-api/public/v3/zz_complete_dataset'
        res = requests.get(url)
        species_release = json.loads(res.text)

        proyects = species_release['projects']
        proyect = [proyect for proyect in proyects if proyect['id'] == proyect_id][0]
        return proyect[field]

    def get_gene_names(self):
        return self.gene_names

    def get_taxonomy(self):
        return self.taxonomy

    def get_expression(self):
        return self.expression

from __future__ import print_function

import re

import requests
import os

import pandas as pd
import numpy as np
import json

from app import values


class Taxonomy:
    def __init__(self):

        self.gene_names = pd.DataFrame()

        self.taxonomy = pd.DataFrame()
        self.expression = pd.DataFrame()

        self.experiments = []
        self.dataset_info = []

    def set_gene_names(self):
        """
        Reads all avaivable gene locus tags (Gene Names)
        """

        self.gene_names = pd.read_csv(os.path.join(os.getcwd(), 'app/static/data/gene_names.tsv'), sep='\t')

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

            for i in range(line.size):
                for del_elem in values.del_list:
                    line[i] = re.sub(del_elem, '', line[i])

            print(f'Gene found with accession id: {line[0]}')
            self.taxonomy = pd.DataFrame(line.reshape((1, -1)), columns=cols)
            self.taxonomy.at[0, 'Gene Names (ordered locus)'] = self.taxonomy.at[0, 'Gene Names (ordered locus)'].replace('MTR_', 'Medtr')

            if verbose:
                print(self.taxonomy.head())

            return True
        except Exception:
            print('Gene not found')
            return False

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

        filtered = self.expression[[exp for exp in self.expression.columns if exp.startswith(experiment)]]
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

    def set_experiments(self):
        """
        Set all available experiments
        """

        if not self.expression.empty:
            exp = []
            for col in self.expression.columns:
                exp_id, _ = col.split(':')
                if not [i for i in exp if i.startswith(exp_id)]:
                    date = str(self.get_experiments_info(exp_id, 'date'))
                    categories = str(self.get_experiments_info(exp_id, 'categories'))
                    exp.append(exp_id + '-' + date + '-' + categories)
            self.experiments = exp
            return
        self.experiments = values.experiments

    def get_dataset_info(self):
        """
        Gets info of the available experiments in the dataset.
        """

        url = 'https://lipm-browsers.toulouse.inra.fr/expression-atlas-api/public/v3/zz_complete_dataset'
        res = requests.get(url)
        self.dataset_info = json.loads(res.text)

    def get_experiments_info(self, proyect_id, field):
        """
        Gets the categories of a given experiment.
        """

        projects = self.dataset_info['projects']
        project = [proyect for proyect in projects if proyect['id'] == proyect_id][0]
        return project[field]

    def get_gene_names(self):
        return self.gene_names

    def get_taxonomy(self):
        return self.taxonomy

    def get_expression(self):
        return self.expression

    def get_accession_id(self):
        if not self.taxonomy.empty:
            return self.taxonomy.at[0, 'Entry']

    def get_gene_name_v4(self):
        if not self.taxonomy.empty:
            return self.taxonomy.at[0, 'Gene Names (ordered locus)']

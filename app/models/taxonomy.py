from __future__ import print_function

import re

import requests
import os

import pandas as pd
import numpy as np
import json

from app import values, cache


class Taxonomy:
    def __init__(self):

        self.gene_names = pd.DataFrame()
        self.synonimous = {}

        self.taxonomy = pd.DataFrame()

    def set_gene_names(self):
        """
        Reads all avaivable gene locus tags (Gene Names)
        """

        self.gene_names = pd.read_csv(os.path.join(os.getcwd(), 'app/static/data/gene_names.tsv'), sep='\t')

    def set_synonymous(self, gene_kw):
        """
        Gets all available synonymous of a given gene; v4 & v5 nomination
        """

        self.synonimous = {}
        gene_kw = gene_kw.replace(" ", "")  # White spaces fix

        res = cache.get(gene_kw)
        if res is not None:
            self.synonimous['v5'] = res
        else:
            url = f'https://lipm-browsers.toulouse.inra.fr/expression-atlas-api/public/v3/zz_complete_dataset/{gene_kw}/synonymous'
            res = requests.get(url)
            if res.status_code == 200:
                data = json.loads(res.text)
                if data[0]['synonymous_dataset'] == '':
                    print('Gene not found')
                    return False

                self.synonimous['v5'] = data[0]['locus_tag']
                cache.set(gene_kw, self.synonimous['v5'])
                for line in data:
                    ds = line['synonymous_dataset']
                    if ds in values.synonymous_ds.keys():
                        self.synonimous[values.synonymous_ds[ds]] = line['synonymous_id']

        self.set_v4_synonymus(gene_kw)
        return True

    def set_v4_synonymus(self, gene_kw):
        res = cache.get(gene_kw + '_v4')
        if res is not None:
            self.synonimous['v4'] = res
        else:
            gene_name = self.synonimous['v5']

            url = f'https://lipm-browsers.toulouse.inra.fr/expression-atlas-api/public/v3/zz_complete_dataset/{gene_name}/synonymous'
            res = requests.get(url)
            if res.status_code == 200:
                data = json.loads(res.text)
                for line in data:
                    if line['synonymous_dataset'] == 'JCVI-Mt4.0v2-gene':
                        self.synonimous['v4'] = line['synonymous_id']
                        cache.set(gene_kw + '_v4', line['synonymous_id'])

    def set_gene_taxonomy(self, gene_kw, gene_name, verbose=False):
        """
        Gets the taxonomy of a single gen from UniProt.
        Data will be estored in self Pandas DataFrame variable taxonomy.
        """

        res = cache.get(gene_kw + '_taxonomy')
        if res is not None:
            self.taxonomy = res
        else:
            url = f'https://rest.uniprot.org/uniprotkb/stream?fields=accession%2Cdate_modified%2Cid%2Cgene_orf%2Cgene_oln%2Ccc_function%2Ccc_tissue_specificity%2Ccc_induction%2Cgo%2Ccc_subcellular_location%2Clength%2Csequence%2Cxref_string&format=tsv&query=%28{gene_name}%29'
            res = requests.get(url)
            line = res.text.splitlines()

            try:  # Check of data availability in Dataset
                cols = line[0].split('\t')
                line = np.array(line[1].split('\t'))

                for i in range(line.size):
                    for del_elem in values.del_list:
                        line[i] = re.sub(del_elem, '', line[i])

                print(f'Taxonomy: Gene found with accession id: {line[0]}')
                self.taxonomy = pd.DataFrame(line.reshape((1, -1)), columns=cols)
                self.taxonomy.at[0, 'Gene Names (ordered locus)'] = self.taxonomy.at[0, 'Gene Names (ordered locus)'].replace('MTR_', 'Medtr')
                self.taxonomy.at[0, 'Gene Names (ORF)'] = self.synonimous['v5']

                cache.set(gene_kw + '_taxonomy', self.taxonomy)

                if verbose:
                    print(self.taxonomy.head())
                return True

            except Exception as e:
                print(f'Taxonomy: {e}')
                return False

        return True

    def validate_gene_form_taxonomy(self, gene_kw, synonyms):
        """
        Function to validate the existance of a gene in the differents DDBB via API.
        """

        fs_taxonomy = self.set_gene_taxonomy(gene_kw, synonyms['v5'])
        if not fs_taxonomy:
            fs_taxonomy = self.set_gene_taxonomy(
                gene_kw,
                synonyms['v4'].replace('Medtr', 'MTR_') if 'v4' in synonyms else synonyms['v5']
            )
            if not fs_taxonomy:
                return False

        return True

    def get_accession_id(self):
        if not self.taxonomy.empty:
            return self.taxonomy.at[0, 'Entry']

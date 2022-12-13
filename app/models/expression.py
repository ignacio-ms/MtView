import requests
import re

import plotly.graph_objects as go
import plotly.utils

import numpy as np
import pandas as pd
import json

from app import values


class Expression:
    def __init__(self):

        self.expression = pd.DataFrame()

        self.experiments = []
        self.dataset_info = []

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
            print('Expression: Gene not found.')
            return False
        print('Expression: Gene found.')

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
                    author = values.experiments[exp_id]
                    exp.append(exp_id + ' - ' + date + ' - ' + author)
            exp.sort(key=lambda x: x.split('-')[2])
            self.experiments = exp
            return
        self.experiments = []

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

    def validate_gene_form_expression(self, synonyms):
        """
        Function to validate the existance of a gene in the differents DDBB via API.
        """

        fs_expression = self.set_gene_expression(synonyms['v5'])
        if not fs_expression:
            return False

        return True

    def init_boxplot(self, experiment, mode):
        """
        Function to initialize and update the gene expression values boxplot.
        """

        fig = go.Figure()

        titles = {}
        for c, exp in enumerate(experiment):
            expression = self.filter_by_experiment(exp)
            titles[exp] = values.experiments[exp]

            ticks = pd.unique([re.sub(r'(?is)-.+', '', col) for i, col in enumerate(expression.columns)])
            reps = {t: len([col for col in expression.columns if col.__contains__(t + '-')]) for t in ticks}
            data = expression.loc[mode]

            i = 0
            for tick, rep in reps.items():
                df = pd.DataFrame(np.array(data[i: i + rep]).reshape(rep, -1), columns=[tick], dtype=float)
                fig.add_trace(
                    go.Box(
                        y=df[tick],
                        name=tick,
                        marker_color=values.colors[c % 3]
                    )
                )
                i += rep

        fig.update_layout(
            title=str(titles).replace('{', '').replace('}', '').replace('\'', '')
        )
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

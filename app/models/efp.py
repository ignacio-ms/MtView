import os
import re

from app import values

import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.colors import n_colors


class efp:

    def __init__(self):
        self.tissues_log2_tmm = pd.DataFrame()
        self.tissues_tmm = pd.DataFrame()

        self.symbiosis_tmm = pd.DataFrame()
        self.symbiosis_log2_tmm = pd.DataFrame()

        self.data = {}
        self.fig = None

    @staticmethod
    def init_colors():
        """
        Initializes all tissue fills color to white
        """

        return {label+'_fill': '#ffffff' for label in values.img_labels}

    def read_tissues(self):
        """
        Reads tissue localization gene expression data
        """

        self.tissues_tmm = pd.read_csv(os.path.join(os.getcwd(), 'app/static/data/rnaseq_tissues_tmm.tsv'), sep='\t', index_col='gene_name')
        self.tissues_log2_tmm = pd.read_csv(os.path.join(os.getcwd(), 'app/static/data/rnaseq_tissues_log2_tmm.tsv'), sep='\t', index_col='gene_name')

    def read_symbiosis(self):
        """
        Reads tissue localization gene expression data based on nitrogen-fixing symbiosis and nitrate treatment.
        """

        self.symbiosis_tmm = pd.read_csv(os.path.join(os.getcwd(), 'app/static/data/rnaseq_symbiosis_tmm.tsv'), sep='\t', index_col='gene_name')
        self.symbiosis_log2_tmm = pd.read_csv(os.path.join(os.getcwd(), 'app/static/data/rnaseq_symbiosis_log2_tmm.tsv'), sep='\t', index_col='gene_name')

    def init_efp(self, gene_name, norm='tmm'):
        """
        Computes the eFP methods to colour each tissue with its corresponding expression value.
        """

        if gene_name != '':
            expression_t = self.tissues_tmm.loc[gene_name] if norm == 'tmm' else self.tissues_log2_tmm.loc[gene_name]
            ticks_t = np.unique([re.sub(r'(?is)-.+', '', col) for col in self.tissues_tmm.columns])
            self.data = {
                t: round(np.average([val for item, val in expression_t.items() if item.__contains__(t + '-')]), 2)
                for t in ticks_t
            }

            expression_s = self.symbiosis_tmm.loc[gene_name] if norm == 'tmm' else self.symbiosis_log2_tmm.loc[gene_name]
            ticks_s = np.unique([re.sub(r'(?is)-.+', '', col) for col in self.symbiosis_tmm.columns])
            self.data.update({
                t: round(np.average([val for item, val in expression_s.items() if item.__contains__(t + '-')]), 2)
                for t in ticks_s
            })
            self.data.update({'intra_nodule': 0})

            def rgb_to_hex(rbg):
                data = [int(float(e)) for e in rbg.split(',')]
                return '#%02x%02x%02x' % (data[0], data[1], data[2])

            non_zero = [i for i in self.data.values() if i > 0]
            if norm == 'tmm':
                cmap = ['rgb(255, 255, 255)'] + n_colors('rgb(255, 255, 0)', 'rgb(255, 0, 0)', len(non_zero), 'rgb')
            else:
                cmap = ['rgb(255, 255, 255)'] + n_colors('rgb(0, 0, 255)', 'rgb(255, 0, 0)', len(self.data) - 1, 'rgb')
            cmap = [rgb.replace('rgb', '').replace('(', '').replace(')', '') for rgb in cmap]
            cmap = [rgb_to_hex(rgb) for rgb in cmap]

            self.fig = self.init_legend(cmap, non_zero, norm) if norm == 'tmm' else self.init_legend(cmap, self.data.values(), norm)

            cmap.pop(0)
            if norm == 'tmm':
                svg_colors = {e[0] + '_fill': cmap.pop(0) for i, e in enumerate(sorted(self.data.items(), key=lambda kv: (kv[1], kv[0]))) if e[1] > 0}
                svg_colors.update({k + '_fill': '#ffffff' for k, v in self.data.items() if v <= 0})
            else:
                svg_colors = {e[0] + '_fill': cmap.pop(0) for i, e in enumerate(sorted(self.data.items(), key=lambda kv: (kv[1], kv[0]))) if e[1] != 0}
                svg_colors.update({k + '_fill': '#ffffff' for k, v in self.data.items() if v == 0})
            return svg_colors

        self.fig = None
        return self.init_colors()

    def init_legend(self, cmap, non_zero, norm):
        """
        Creates the eFP legend colormap.
        """

        fig = go.Figure()

        aux = sorted(non_zero + [0]) if norm == 'tmm' else sorted(non_zero)
        for i, c in enumerate(cmap):
            fig.add_bar(
                x=list(sorted(self.data.values())), y=[1], marker_color=c,
                name=aux.pop(0), showlegend=False, hovertemplate=' '
            )

        fig.update_xaxes(visible=False).update_yaxes(visible=False)
        fig.update_layout(
            barmode='stack', width=300,
            plot_bgcolor='#F3F3F2', paper_bgcolor='#F3F3F2',
            dragmode=False,
            title=f'Expression value ({norm})'
        )
        return fig

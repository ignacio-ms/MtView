import os
import re

from app import values
# from app.models import taxonomy

import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.colors import n_colors


class efp:

    def __init__(self, taxonomy):
        self.tissues_log2_tmm = pd.DataFrame()
        self.tissues_tmm = pd.DataFrame()

        self.symbiosis_tmm = pd.DataFrame()
        self.symbiosis_log2_tmm = pd.DataFrame()

        self.taxonomy = taxonomy
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

        self.tissues_tmm = pd.read_csv(
            os.path.join(os.getcwd(), 'app/static/data/rnaseq_tissues_tmm.tsv'),
            sep='\t', index_col='gene_names'
        )
        self.tissues_log2_tmm = pd.read_csv(
            os.path.join(os.getcwd(), 'app/static/data/rnaseq_tissues_log2_tmm.tsv'),
            sep='\t', index_col='gene_names'
        )

    def init_efp(self, gene_name, norm='tmm'):
        """
        Computes the eFP methods to colour each tissue with its corresponding expression value.
        """

        if gene_name != '':
            expression = self.tissues_tmm.loc[gene_name] if norm == 'tmm' else self.tissues_log2_tmm.loc[gene_name]
            ticks_t = pd.unique([re.sub(r'(?is)-.+', '', col) for col in self.tissues_tmm.columns])
            self.data = {t: round(np.average([val for item, val in expression.items() if item.__contains__(t + '-')]), 2) for t in ticks_t}

            self.get_intra_nodule(norm)

            bins = sorted(np.unique([i for i in self.data.values() if i != 0]))
            is_zero = [True for i in self.data.values() if i == 0]

            if norm == 'tmm':
                cmap = ['rgb(255, 255, 255)'] + n_colors('rgb(255, 255, 0)', 'rgb(255, 0, 0)', len(bins), 'rgb')
            else:
                bins = sorted(np.unique([i for i in self.data.values()]))
                cmap = ['rgb(255, 255, 255)'] + n_colors('rgb(0, 0, 255)', 'rgb(255, 0, 0)', len(bins), 'rgb')
            cmap = [self.rgb2hex(rgb) for rgb in cmap]
            cmap_dict = {i: c for i, c in enumerate(cmap)}

            colors = [cmap_dict.get(i) for i in np.digitize(sorted(self.data.values()), bins)]
            svg_colors = {e[0] + '_fill': colors[i] for i, e in enumerate(sorted(self.data.items(), key=lambda kv: (kv[1], kv[0])))}

            self.fig = self.init_legend(colors, bins, norm, is_zero if norm == 'tmm' else [])
            return svg_colors

        self.fig = None
        return self.init_colors()

    def get_intra_nodule(self, norm='tmm'):
        """
        Gets expression values of Roux et. al. laser dissection expreiment
        """

        expression = self.taxonomy.filter_by_experiment('SRP028599')

        ticks = pd.unique([re.sub(r'(?is)-.+', '', col) for i, col in enumerate(expression.columns)])
        reps = {t: len([col for col in expression.columns if col.__contains__(t + '-')]) for t in ticks}
        expression = expression.loc[norm]

        vals = [
            'Mt_Sm_RbmL_Nodule_ZI',
            'Mt_Sm_RbmL_Nodule_ZIId',
            'Mt_Sm_RbmL_Nodule_ZIIp',
            'Mt_Sm_RbmL_Nodule_IZ',
            'Mt_Sm_RbmL_Nodule_ZIII'
        ]

        i = 0
        for tick, rep in reps.items():
            if tick in vals:
                t = tick.split('_')[4]
                self.data['intra_nodule_'+t] = round(np.average(np.array(expression[i: i+rep], dtype=float)), 3)
            i += rep

    @staticmethod
    def rgb2hex(rgb):
        """
        Parse rgb color into its hexadecimal value
        """

        rgb = rgb.replace('rgb', '').replace('(', '').replace(')', '')
        rgb = [int(float(e)) for e in rgb.split(',')]
        return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

    def init_legend(self, colors, bins, norm, is_zero):
        """
        Creates the eFP legend colormap.
        """

        fig = go.Figure()

        aux = sorted(bins)
        if is_zero and norm == 'tmm':
            aux = [0] + aux

        colors = np.flip(np.unique(colors)) if norm == 'tmm' else np.unique(colors)
        for i, c in enumerate(colors):
            name = aux.pop(0)
            fig.add_bar(
                x=list(sorted(self.data.values())), y=[1], marker_color=c,
                name=name, text=name, textposition='inside',
                showlegend=False, hovertemplate=' '
            )

        fig.update_xaxes(visible=False).update_yaxes(visible=False)
        fig.update_layout(
            barmode='stack', width=300, height=550,
            plot_bgcolor='#F3F3F2', paper_bgcolor='#F3F3F2',
            dragmode=False,
            title=f'Expression value ({norm})'
        )
        return fig

import json
import plotly.utils

from app.views import taxonomy, molecule
from app import values

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np

import re


def validate_gene_form(synonyms):
    """
    Function to validate the existance of a gene in the differents DDBB via API.
    """

    fs_expression = taxonomy.set_gene_expression(synonyms['v5'])
    if not fs_expression:
        return 'Gene not found', False, False

    fs_taxonomy = taxonomy.set_gene_taxonomy(synonyms['v5'])
    if not fs_taxonomy:
        fs_taxonomy = taxonomy.set_gene_taxonomy(synonyms['v4'].replace('Medtr', 'MTR_') if 'v4' in synonyms else synonyms['v5'])
        if not fs_taxonomy:
            return 'Gene found', True, False

    return 'Gene found', True, True


def init_boxplot(experiment, mode):
    """
    Function to initialize and update the gene expression values boxplot.
    """

    fig = go.Figure()

    titles = {}
    for c, exp in enumerate(experiment):
        expression = taxonomy.filter_by_experiment(exp)
        titles[exp] = values.experiments[exp]

        ticks = pd.unique([re.sub(r'(?is)-.+', '', col) for i, col in enumerate(expression.columns)])
        reps = {t: len([col for col in expression.columns if col.__contains__(t + '-')]) for t in ticks}
        data = expression.loc[mode]

        i = 0
        for tick, rep in reps.items():
            df = pd.DataFrame(np.array(data[i: i+rep]).reshape(rep, -1), columns=[tick], dtype=float)
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


def init_pae(size=400):
    """
    Function to initialize the molecule Predicted Aligned Error heatmat.
    """

    fig = px.imshow(
        molecule.get_pae(),
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

import json
import plotly.utils

from app.views import taxonomy, molecule
from app import values

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np

import re


def validate_gene_form(request):
    """
    Function to validate the existance of a gene in the differents DDBB via API.
    """

    fs_expression = taxonomy.set_gene_expression(request.form['gene_name'])
    if not fs_expression:
        return 'Gene not found', False, False

    fs_taxonomy = taxonomy.set_gene_taxonomy(request.form['gene_name'])
    if not fs_taxonomy:
        return 'Gene found', True, False

    return 'Gene found', True, True


def init_boxplot(experiment, mode, height=800, width=1200):
    """
    Function to initialize and update the gene expression values boxplot.
    """

    fig = go.Figure()

    titles = {}
    line_avg = []
    line_x = []
    for c, exp in enumerate(experiment):
        expression = taxonomy.filter_by_experiment(exp)
        titles[exp] = values.experiments[exp]

        ticks = pd.unique([re.sub(r'(?is)-.+', '', col) for i, col in enumerate(expression.columns)])
        reps = {t: len([col for col in expression.columns if col.__contains__(t + '-')]) for t in ticks}
        data = expression.loc[mode]

        i = 0
        for tick, rep in reps.items():
            line_avg.append(np.average(np.array(data[i: i+rep], dtype=float)))
            df = pd.DataFrame(np.array(data[i: i+rep]).reshape(rep, -1), columns=[tick], dtype=float)
            fig.add_trace(
                go.Box(
                    y=df[tick],
                    name=tick,
                    marker_color=values.colors[c % 3]
                )
            )
            i += rep
            line_x.append(tick)

    fig.add_trace(go.Scatter(
        x=line_x,
        y=line_avg,
        name='Average',
        mode='lines', line_color='#ffa400'
    ))
    fig.update_layout(
        height=height, width=width,
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

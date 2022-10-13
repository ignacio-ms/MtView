import json

import plotly.utils

from app.models import taxonomy
from app import values

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import re


def validate_gene_form(request):
    fs_expression = taxonomy.get_gene_expression(request.form['gene_name'])
    fs_taxonomy = taxonomy.get_gene_taxonomy(request.form['gene_name'])
    if not fs_taxonomy or not fs_expression:
        return 'Gene not found', False

    return 'Gene found', True


def init_boxplot(experiment, mode):
    fig = go.Figure()

    titles = {}
    for c, exp in enumerate(experiment):
        expression = taxonomy.filter_by_experiment(exp)
        categories = taxonomy.get_experiments_info(exp, 'categories')
        date = taxonomy.get_experiments_info(exp, 'date')

        d = np.zeros(shape=(3, expression.loc[f'{mode}'].shape[0] // 3))
        d_aux = np.zeros(shape=(3,))

        titles[exp] = str(date) + '-' + exp + '-' + categories[0]
        ticks = [re.sub(r'(?is)-.+', '', col) for i, col in enumerate(expression.columns) if i % 3 == 0]

        for i, data in enumerate(expression.loc[f'{mode}']):
            d_aux[i % 3] = data
            if i % 3 == 2:
                d[:, i // 3] = d_aux
                d_aux = np.zeros(shape=(3,))

        d = pd.DataFrame(d, columns=ticks)
        for i, cols in enumerate(d):
            fig.add_trace(go.Box(y=d[cols], name=ticks[i], marker_color=values.colors[c % 3]))

    fig.update_layout(height=800, width=1200, title=mode + str(titles))

    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

# def init_efp(gf, experiment, mode, _):
#     """
#     Funtion to plot the eFP (electronic fluorescent pictograph)
#     """
#
#     if taxonomy.expression.empty or gf != 'Gene found':
#         return None
#
#     fig = go.Figure()
#
#     efp.generate_efp(experiment, mode)
#
#     fig.add_trace(go.Image(colormodel='rgba', z=efp.get_contours(), hoverinfo='none'))
#     fig.update_xaxes(showticklabels=False)
#     fig.update_yaxes(showticklabels=False)
#     fig.update_layout(
#         height=800,
#         dragmode=False,
#         xaxis_range=[200, 1920],
#         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
#         xaxis=dict(showgrid=False),
#         yaxis=dict(showgrid=False)
#     )
#     return dcc.Graph(figure=fig)

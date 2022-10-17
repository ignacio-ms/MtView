import json
import plotly.utils

from app.views import taxonomy
from app import values

import plotly.graph_objects as go
import pandas as pd
import numpy as np

import re


def validate_gene_form(request):
    fs_expression = taxonomy.set_gene_expression(request.form['gene_name'])
    fs_taxonomy = taxonomy.set_gene_taxonomy(request.form['gene_name'])
    if not fs_taxonomy or not fs_expression:
        return 'Gene not found', False

    return 'Gene found', True


def init_boxplot(experiment, mode, height=800, width=1200):
    fig = go.Figure()

    titles = {}
    for c, exp in enumerate(experiment):
        print(taxonomy.get_taxonomy())
        print(taxonomy.get_expression())
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

    fig.update_layout(height=height, width=width, title=mode + str(titles))

    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

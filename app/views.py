import json
import re

import plotly
from flask import render_template, request, Response

from app import app, values
from app.models import taxonomy, efp, molecule

from .forms import GeneForm
from app.controller import validate_gene_form, init_boxplot, init_pae


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    Funtion to render the index.html template with all it's jinja variables.
    Also in change of managing the gene request form.
    """

    svg_colors = efp.init_colors()
    svg_data = None
    interaction_id = None
    is_expression = False
    is_taxonomy = False
    efp_legend = None
    gene_found = ''
    gene_name = ''
    boxplot = None
    mol = None
    pae = None

    gene_form = GeneForm()
    if request.method == 'POST':
        gene_name = request.form['gene_name']
        if taxonomy.set_synonymous(gene_name):
            gene_found, is_expression, is_taxonomy = validate_gene_form(taxonomy.synonimous)

            if is_expression:
                taxonomy.set_experiments()
                boxplot = init_boxplot(['SRP109847'], 'tmm')

                svg_colors = efp.init_efp(taxonomy.synonimous['v4'], norm='tmm')
                svg_data = efp.data
                if efp.fig is not None:
                    efp_legend = json.dumps(efp.fig, cls=plotly.utils.PlotlyJSONEncoder)

            if is_taxonomy:
                interaction_id = taxonomy.taxonomy['STRING']
                if interaction_id[0] == '':
                    interaction_id = None

                if molecule.set_mol(taxonomy.get_accession_id()):
                    molecule.set_pae(taxonomy.get_accession_id())
                    mol = molecule.get_mol()
                    pae = init_pae()
                else:
                    mol, pae = None, None
        else:
            gene_found = 'Gene not found'

    return render_template(
        'control_card.html',
        title='MtView',
        analysis_tools=values.analysis_tools,
        experiments=taxonomy.experiments,
        norm_methods=values.norm_methods,
        right_col=is_expression,
        is_taxonomy=is_taxonomy,
        interaction_id=interaction_id,
        gene_found=gene_found,
        gene_name=gene_name,
        taxonomy=taxonomy,
        boxplot=boxplot,
        gene_form=gene_form,
        pae=pae,
        mol=mol,
        svg_colors=svg_colors,
        svg_data=svg_data,
        efp_legend=efp_legend
    )


@app.route('/search', methods=['GET'])
def live_search():
    """
    Funtion to manage the gene request form autocomplete with all genes available.
    """

    choices = list(taxonomy.get_gene_names()['locus_tag'])
    return Response(json.dumps(choices), mimetype='application/json')


@app.route('/boxplot', methods=['GET', 'POST'])
def update_boxplot():
    """
    Funtion to update the boxplot with ajax.
    """

    if request.method == 'POST':
        data = request.json
        experiment = [re.sub(r'(?is)-.+', '', exp) for exp in data['exp_selected']]
        mode = data['norm_selected']
        return init_boxplot(experiment, mode)


@app.route('/efp', methods=['GET', 'POST'])
def update_efp():
    """
    Funtion to update the efp with ajax.
    """
    if request.method == 'POST':
        data = request.json
        mode = data['norm_selected']

        svg_colors = efp.init_efp(taxonomy.synonimous['v4'], norm=mode)
        svg_data = efp.data

        efp_legend = None
        if efp.fig is not None:
            efp_legend = json.dumps(efp.fig, cls=plotly.utils.PlotlyJSONEncoder)
        return {'colors': json.dumps(svg_colors), 'plot': efp_legend, 'vals': json.dumps(svg_data)}

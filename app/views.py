import json

from flask import render_template, request, Response

from app import app, values
from app.models import taxonomy, efp, molecule

from .forms import GeneForm
from app.controller import validate_gene_form, init_boxplot, init_pae


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    is_expression = False
    is_taxonomy = False
    gene_found = ''
    gene_name = ''
    boxplot = None
    mol = None
    pae = None
    svg_colors = efp.init_colors()

    gene_form = GeneForm()
    if request.method == 'POST':
        gene_found, is_expression, is_taxonomy = validate_gene_form(request)
        boxplot = init_boxplot(['SRP362799'], 'log2_tmm')
        gene_name = request.form['gene_name']
        if is_taxonomy:
            molecule.set_mol(taxonomy.get_accession_id())
            molecule.set_pae(taxonomy.get_accession_id())
            mol = molecule.get_mol()
            pae = init_pae()

    return render_template(
        'control_card.html',
        title='MtView',
        analysis_tools=values.analysis_tools,
        experiments=values.experiments,
        norm_methods=values.norm_methods,
        right_col=is_expression,
        is_taxonomy=is_taxonomy,
        gene_found=gene_found,
        gene_name=gene_name,
        taxonomy=taxonomy,
        boxplot=boxplot,
        gene_form=gene_form,
        pae=pae,
        mol=mol,
        svg_colors=svg_colors
    )


@app.route('/search', methods=['GET'])
def live_search():
    choices = list(taxonomy.get_gene_names()['locus_tag'])
    return Response(json.dumps(choices), mimetype='application/json')


@app.route('/boxplot', methods=['GET', 'POST'])
def update_boxplot():
    if request.method == 'POST':
        data = request.json
        experiment = data['exp_selected']
        mode = data['norm_selected']
        return init_boxplot(experiment, mode)


@app.route('/pae', methods=['GET', 'POST'])
def update_molecule():
    if request.method == 'POST':
        # Update mol
        return request.json

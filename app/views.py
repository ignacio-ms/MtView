from flask import render_template, request

from app import app, values
from app.models import taxonomy

from .forms import GeneForm
from app.controller import validate_gene_form, init_boxplot


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    right_col = False
    gene_found = ''
    boxplot = None

    gene_form = GeneForm()
    if request.method == 'POST':
        if gene_form.validate():
            gene_found, right_col = validate_gene_form(request)
            boxplot = init_boxplot(['SRP362799'], 'log2_tmm')

    return render_template(
        'control_card.html',
        title='MtView',
        analysis_tools=values.analysis_tools,
        experiments=values.experiments,
        norm_methods=values.norm_methods,
        right_col=right_col,
        gene_found=gene_found,
        taxonomy=taxonomy,
        boxplot=boxplot,
        gene_form=gene_form
    )


@app.route('/boxplot', methods=['GET', 'POST'])
def update_boxplot():
    if request.method == 'POST':
        data = request.json
        experiment = data['exp_selected']
        mode = data['norm_selected']
        return init_boxplot(experiment, mode)

from flask import render_template, request
from app import app, values
from app.models import taxonomy
from .forms import GeneForm


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    cols = False
    gene_found = ''

    form = GeneForm()
    if request.method == 'POST':
        if form.validate():
            fs_taxonomy = taxonomy.get_gene_taxonomy(request.form['gene_name'])
            fs_expression = taxonomy.get_gene_expression(request.form['gene_name'])
            if not fs_taxonomy and not fs_expression:
                gene_found = 'Gene not found'
                cols = False
            else:
                gene_found = 'Gene found'
                cols = True

    return render_template(
        'control_card.html',
        title='MtView',
        analysis_tools=values.analysis_tools,
        experiments=values.experiments,
        norm_methods=values.norm_methods,
        right_col=cols,
        experiemnt_div=cols,
        gene_found=gene_found,
        taxonomy=taxonomy,
        form=form
    )

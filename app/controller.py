import json
import re

import plotly
from flask import render_template, request, Response

from app import app, values, cache
from app.models import taxonomy, efp, molecule, expression

from .forms import GeneForm

is_expression = False
is_taxonomy = False

gene_name_v5 = None
gene_found = ''
gene_name = ''

interaction_id = None
svg_colors = efp.init_colors()
svg_data = None
efp_legend = None
boxplot = None
mol = None
pae = None


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    Funtion to render the index.html template with all it's jinja variables.
    Also in change of managing the gene request form.
    """

    global is_expression
    global is_taxonomy

    global gene_name_v5
    global gene_found
    global gene_name

    global interaction_id
    global svg_colors
    global svg_data
    global efp_legend
    global boxplot
    global mol
    global pae

    gene_form = GeneForm()
    if request.method == 'POST':
        gene_name = request.form['gene_name']
        res = cache.get(gene_name)
        if res is None:
            get_data_api()
        else:
            get_data_cache()

    return render_template(
        'control_card.html',
        title='MtView',
        analysis_tools=values.analysis_tools,
        experiments=expression.experiments,
        norm_methods=values.norm_methods,
        right_col=is_expression,
        is_taxonomy=is_taxonomy,
        interaction_id=interaction_id,
        gene_found=gene_found,
        gene_name=gene_name,
        gene_name_v5=gene_name_v5,
        taxonomy=taxonomy,
        boxplot=boxplot,
        gene_form=gene_form,
        svg_colors=svg_colors,
        svg_data=svg_data,
        efp_legend=efp_legend,
        pae=pae,
        mol=mol,
    )


def get_data_cache():
    global is_expression
    global is_taxonomy

    global gene_name_v5
    global gene_found
    global gene_name

    global interaction_id
    global svg_colors
    global svg_data
    global efp_legend
    global boxplot
    global mol
    global pae

    print('Loading from cache')

    is_expression = expression.load_data_from_cache(gene_name)
    is_taxonomy = taxonomy.load_data_from_cache(gene_name)
    gene_found = 'Gene found'

    if is_expression:
        expression.set_experiments()
        boxplot = expression.init_boxplot(['SRP109847'], 'tmm')
        gene_name_v5 = taxonomy.synonimous['v5']

        if 'v4' in taxonomy.synonimous:
            svg_colors = efp.init_efp(taxonomy.synonimous['v4'], norm='tmm')
        else:
            svg_colors = efp.init_efp('', norm='tmm')
        svg_data = efp.data
        if efp.fig is not None:
            efp_legend = json.dumps(efp.fig, cls=plotly.utils.PlotlyJSONEncoder)

    if is_taxonomy:
        interaction_id = cache.get(gene_name + '_STRING')

        if molecule.load_data_from_cache(gene_name):
            mol = molecule.mol
            pae = molecule.init_pae()
        else:
            mol, pae = None, None

    return


def get_data_api():
    global is_expression
    global is_taxonomy

    global gene_name_v5
    global gene_found
    global gene_name

    global interaction_id
    global svg_colors
    global svg_data
    global efp_legend
    global boxplot
    global mol
    global pae

    if taxonomy.set_synonymous(gene_name):
        is_expression = expression.validate_gene_form_expression(gene_name, taxonomy.synonimous)
        is_taxonomy = taxonomy.validate_gene_form_taxonomy(gene_name, taxonomy.synonimous)
        gene_found = 'Gene found'

        if is_expression:
            expression.set_experiments()
            boxplot = expression.init_boxplot(['SRP109847'], 'tmm')
            gene_name_v5 = taxonomy.synonimous['v5']

            if 'v4' in taxonomy.synonimous:
                svg_colors = efp.init_efp(taxonomy.synonimous['v4'], norm='tmm')
            else:
                svg_colors = efp.init_efp('', norm='tmm')
            svg_data = efp.data
            if efp.fig is not None:
                efp_legend = json.dumps(efp.fig, cls=plotly.utils.PlotlyJSONEncoder)

        if is_taxonomy:
            interaction_id = taxonomy.taxonomy['STRING']
            if interaction_id[0] == '':
                interaction_id = None
            else:
                cache.set(gene_name + '_STRING', interaction_id)

            if molecule.set_mol(gene_name, taxonomy.get_accession_id()):
                molecule.set_pae(gene_name, taxonomy.get_accession_id())
                mol = molecule.mol
                pae = molecule.init_pae()
            else:
                mol, pae = None, None
    else:
        gene_found = 'Gene not found'

        is_expression = False
        is_taxonomy = False

        gene_name_v5 = None

        interaction_id = None
        svg_colors = efp.init_colors()
        svg_data = None
        efp_legend = None
        boxplot = None
        mol = None
        pae = None


@app.route('/search', methods=['GET'])
def live_search():
    """
    Funtion to manage the gene request form autocomplete with all genes available.
    """

    choices = list(taxonomy.gene_names['locus_tag'])
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
        return expression.init_boxplot(experiment, mode)


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

from flask import render_template
from app import app, values


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'analysis_card.html',
        title='MtView',
        analysis_tools=values.analysis_tools,
        experiments=values.experiments,
        norm_methods=values.norm_methods,
        right_col=True,
        experiemnt_div=True
    )

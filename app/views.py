from flask import render_template
from app import app, VALUES


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'analysis_card.html',
        title='MtView',
        analysis_tools=VALUES.analysis_tools,
        experiments=VALUES.experiments,
        norm_methods=VALUES.norm_methods
    )

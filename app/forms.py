from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class GeneForm(Form):
    """
    Flask html form to submit Gene Name to search
    """
    gene_name = StringField('gene_name', id='gene-in', validators=[DataRequired()], default='MtrunA17_Chr3g0110971')
    # MtrunA17_Chr1g0201991
    # MtrunA17_Chr7g0257471

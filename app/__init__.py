from flask import Flask
from app import taxonomy, efp


app = Flask(__name__)
taxonomy = taxonomy.Taxonomy()
efp = efp.efp()

from app import views, utils, VALUES

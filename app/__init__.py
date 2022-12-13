from flask import Flask
from app.models import efp, taxonomy

app = Flask(__name__)
app.config.from_object('config')

from app import controller, values

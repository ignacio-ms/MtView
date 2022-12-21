import os
import bmemcached

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

cache = bmemcached.Client(
  os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
  os.environ.get('MEMCACHEDCLOUD_USERNAME'),
  os.environ.get('MEMCACHEDCLOUD_PASSWORD')
)


from app.models import efp, taxonomy
from app import controller, values

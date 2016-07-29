__version__ = '0.1.hack'

from flask import Flask
app = Flask(__name__)

import template.views

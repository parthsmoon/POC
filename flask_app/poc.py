"""
POC - Design of plugable flask application
Author: Parth Wadhwa
"""

import yaml
from flask import Flask
from plugins import hello_app, qr_app
from flask_talisman import Talisman, GOOGLE_CSP_POLICY

# Making it relative, just for poc
# It will be managed by EviveScript
conf = yaml.load(open('etc/flask_app.yaml'))


app = Flask(__name__)
app.secret_key = conf['secret_key']

# Importing plugins
app.register_blueprint(hello_app)
app.register_blueprint(qr_app)

GOOGLE_CSP_POLICY['default-src'] = '\'self\' *.gstatic.com *.googleapis.com'
Talisman(app, content_security_policy=GOOGLE_CSP_POLICY)

# Executing flask application in debug mode
app.run(debug=True)

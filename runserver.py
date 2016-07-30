#!/usr/bin/env python3

import os
from template import app

if os.environ.get("DOCKER_PROD", False):
    app.run(host="0.0.0.0", port=8080)
elif os.environ.get("DOCKER_DEV", False):
    app.run(host="0.0.0.0", port=8080, debug=True)
else:
    app.run(debug=True)

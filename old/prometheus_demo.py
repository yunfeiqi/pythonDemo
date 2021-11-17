#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2021/06/21 11:29:14
@Author  :   sam.qi
@Version :   1.0
@Desc    :   Prometheus Client 
'''

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import start_http_server, Summary,Gauge
import random
import time

# Create my app
app = Flask(__name__)

# Create a metric to track time spent and requests made.
REQUEST_TIME = Gauge('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == "__main__":
    app.run()

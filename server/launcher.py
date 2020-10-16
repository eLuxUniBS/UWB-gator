"""
Lancio servizi
"""
from .settings.urls import app
def launcher():
    app.run()

import pytest
from app import app
import os
from flask import Flask

def test_if_correct_database():
    if os.environ.get("RUNNING_ON_HEROKU") is None:
        assert app.config['MYSQL_USER'] == "Andrei"
    else:
        assert app.config['MYSQL_USER'] == 'bca07be0627548'

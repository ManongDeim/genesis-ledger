import pytest

from app import app
from db import client, db


@pytest.fixture
def client_app():
    app.config['TESTING'] = True
    with app.test_client() as client_app:
        yield client_app
        
client.drop_database(db.name)  # Drop the database after tests to ensure a clean state
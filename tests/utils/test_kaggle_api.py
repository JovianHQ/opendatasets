import json
import os
from pathlib import Path

from opendatasets.utils.kaggle_api import read_kaggle_creds


def test_read_kaggle_creds():
    found = read_kaggle_creds()
    assert not found


def test_read_kaggle_creds_file_found():
    """Creates a local kaggle credential file and verifies that the credentials are loaded"""
    credentials_file = Path(__file__).cwd() / 'kaggle.json'
    credentials_file.unlink(missing_ok=True)

    os.environ['KAGGLE_USERNAME'] = ''
    os.environ['KAGGLE_KEY'] = ''

    kaggle_data = {'username': 'wolverine', 'key': 'adamantium11'}
    with open(credentials_file, 'w') as f:
        json.dump(kaggle_data, f)

    assert credentials_file.exists()

    found = read_kaggle_creds()
    assert found
    assert os.environ['KAGGLE_USERNAME'] == kaggle_data['username']
    assert os.environ['KAGGLE_KEY'] == kaggle_data['key']

    credentials_file.unlink()


def test_read_kaggle_creds_custom_credentials(fixtures_folder):
    credentials_file = fixtures_folder / 'kaggle.json'

    os.environ['KAGGLE_USERNAME'] = ''
    os.environ['KAGGLE_KEY'] = ''

    assert credentials_file.exists()

    found = read_kaggle_creds(credentials_file=credentials_file)
    assert found
    assert os.environ['KAGGLE_USERNAME'] == 'wintersoldier'
    assert os.environ['KAGGLE_KEY'] == 'adamantium22'

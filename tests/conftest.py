from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def fixtures_folder():
    folder = Path(__file__).parent / 'fixtures'
    return folder

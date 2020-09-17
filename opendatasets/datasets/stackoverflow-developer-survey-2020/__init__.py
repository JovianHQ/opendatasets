from urllib.request import urlretrieve
from opendatasets.utils import download_url, GITHUB_RAW_BASE_URL

FILES = [
    'survey_results_public.csv',
    'survey_results_schema.csv',
    'README.txt'
]

def download(dataset_id, data_dir, dry_run, **kwargs):
    base_url = GITHUB_RAW_BASE_URL + dataset_id + "/"
    for fname in FILES:
        full_url = base_url + fname
        download_url(full_url, data_dir, fname, dry_run=dry_run)
            
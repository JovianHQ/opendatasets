from opendatasets.utils.network import download_url

GITHUB_RAW_BASE_URL = 'https://raw.githubusercontent.com/JovianML/opendatasets/master/data/'


def download_raw_files(dataset_id, data_dir, dry_run, files):
    base_url = GITHUB_RAW_BASE_URL + dataset_id + "/"
    for fname in files:
        full_url = base_url + fname
        download_url(full_url, data_dir, fname, dry_run=dry_run)

from opendatasets.utils import download_url

URLs = [
    'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv',
    'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data-last-updated-timestamp.txt',
    'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-codebook.csv'
]


def download(dataset_id, data_dir, dry_run, **kwargs):
    for url in URLs:
        download_url(url, data_dir, dry_run=dry_run)

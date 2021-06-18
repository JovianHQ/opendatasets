import importlib
from opendatasets.utils.network import download_url, is_url
from opendatasets.utils.googledrive import is_google_drive_url, download_google_drive
import os
from opendatasets._version import __version__
from opendatasets.utils.kaggle_api import download_kaggle_dataset, is_kaggle_url
from opendatasets.utils.archive import extract_archive


def download(dataset_id_or_url, data_dir='.', force=False, dry_run=False, **kwargs):
    # Check for a Kaggle dataset URL
    if is_kaggle_url(dataset_id_or_url):
        return download_kaggle_dataset(dataset_id_or_url, data_dir=data_dir, force=force, dry_run=dry_run)

    # Check for Google Drive URL
    if is_google_drive_url(dataset_id_or_url):
        return download_google_drive(dataset_id_or_url, data_dir)

    # Download a raw URL
    if is_url(dataset_id_or_url):
        return download_url(dataset_id_or_url, data_dir)

    dataset_id = dataset_id_or_url
    data_dir = os.path.join(data_dir, dataset_id_or_url)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    dataset = importlib.import_module('opendatasets.datasets.' + dataset_id)
    if dry_run:
        print('This is a dry run. URLs will be displayed but the files will not be downloaded.')
    return dataset.download(dataset_id=dataset_id, data_dir=data_dir, dry_run=dry_run, **kwargs)


def version():
    return __version__

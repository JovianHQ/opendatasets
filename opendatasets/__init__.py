import importlib
import os
from opendatasets._version import __version__
from opendatasets.utils.kaggle_api import download_kaggle_dataset, is_kaggle_url


def download(dataset_id_or_url, data_dir='.', force=False, dry_run=False, **kwargs):
    # Check for a Kaggle dataset URL
    if is_kaggle_url(dataset_id_or_url):
        return download_kaggle_dataset(dataset_id_or_url, data_dir=data_dir, force=force, dry_run=dry_run)

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

import importlib
import os
from opendatasets._version import __version__

def download(dataset_id, data_dir='.', dry_run=False, **kwargs):
    data_dir = os.path.join(data_dir, dataset_id)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    dataset = importlib.import_module('opendatasets.datasets.' + dataset_id)
    if dry_run:
        print('This is a dry run. URLs will be displayed but the files will not be downloaded.')
    return dataset.download(dataset_id=dataset_id, data_dir=data_dir, dry_run=dry_run, **kwargs)

def version():
    return __version__
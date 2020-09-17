import importlib
import os

def download(dataset_id, data_dir='.', dry_run=False, **kwargs):
    data_dir = os.path.join(data_dir, dataset_id)
    os.makedirs(data_dir, exist_ok=True)
    dataset = importlib.import_module('opendatasets.datasets.' + dataset_id)
    return dataset.download(dataset_id=dataset_id, data_dir=data_dir, dry_run=dry_run, **kwargs)
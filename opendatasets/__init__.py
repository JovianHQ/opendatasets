import importlib

def download(dataset_id, *args, **kwargs):
    dataset = importlib.import_module('opendatsets.' + dataset_id)
    return dataset.download(*args, **kwargs)
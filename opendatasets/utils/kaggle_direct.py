import os
from opendatasets.utils.network import urlopen, download_url, is_url
from opendatasets.utils.archive import extract_archive


def is_kaggle_url(url):
    prefixes = ['kaggle.com',
                'www.kaggle.com',
                'http://kaggle.com',
                'http://www.kaggle.com',
                'https://www.kaggle.com',
                'https://kaggle.com']
    return any((url.startswith(prefix) for prefix in prefixes))


def get_kaggle_dataset_id(dataset_id_or_url):
    parts = []
    dataset_id_or_url = dataset_id_or_url.replace("/datasets/", "/")
    if is_kaggle_url(dataset_id_or_url):
        parts = dataset_id_or_url.split('?')[0].split(
            'kaggle.com/')[1].split('/')[:2]
    elif not is_url(dataset_id_or_url):
        parts = dataset_id_or_url.split('/')[:2]
    assert len(parts) == 2, 'Invalid Kaggle dataset URL or ID: ' + \
        dataset_id_or_url
    return '/'.join(parts)


def get_kaggle_download_hash(dataset_id):
    download_page_url = 'https://www.kaggle.com/' + dataset_id + '/download'
    with urlopen(download_page_url) as response:
        redirect_url = response.geturl()
    download_hash = redirect_url.split('downloadHash%3D')[1].split('&')[0]
    return download_hash


def download_kaggle_dataset(dataset_url, data_dir='.', force=True, dry_run=False):
    dataset_id = get_kaggle_dataset_id(dataset_url)
    print('Kaggle dataset ID: ', dataset_id)
    raw_dataset_url = ('https://www.kaggle.com/' +
                       dataset_id +
                       '/download?resource=download&downloadHash=' +
                       get_kaggle_download_hash(dataset_id))
    folder_name = dataset_id.split('/')[-1]
    archive_name = folder_name + '.zip'
    download_url(raw_dataset_url, root=data_dir,
                 filename=archive_name, force=force, dry_run=dry_run)

    extract_archive(os.path.join(data_dir, archive_name),
                    os.path.join(data_dir, folder_name))

import os
import hashlib
from tqdm import tqdm

GITHUB_RAW_BASE_URL = 'https://raw.githubusercontent.com/JovianML/opendatasets/master/data/'


def download_raw_files(dataset_id, data_dir, dry_run, files):
    base_url = GITHUB_RAW_BASE_URL + dataset_id + "/"
    for fname in files:
        full_url = base_url + fname
        download_url(full_url, data_dir, fname, dry_run=dry_run)


def download_url(url, root, filename=None, md5=None, dry_run=False):
    """Download a file from a url and place it in root.
    Args:
        url (str): URL to download file from
        root (str): Directory to place downloaded file in
        filename (str, optional): Name to save the file under. If None, use the basename of the URL
        md5 (str, optional): MD5 checksum of the download. If None, do not check
    """
    import urllib

    try:
        urlretrieve = urllib.request.urlretrieve
    except Exception:
        # For Python 2.7
        urlretrieve = urllib.urlretrieve

    root = os.path.expanduser(root)
    if not filename:
        filename = os.path.basename(url)
    fpath = os.path.join(root, filename)

    if not(os.path.exists(root)):
        os.makedirs(root)

    # check if file is already present locally
    if check_integrity(fpath, md5):
        print('Using downloaded and verified file: ' + fpath)
    else:   # download the file
        try:
            print('Downloading ' + url + ' to ' + fpath)
            if not dry_run:
                urlretrieve(
                    url, fpath,
                    reporthook=gen_bar_updater()
                )
        # type: ignore[attr-defined]
        except (urllib.error.URLError, IOError) as e:
            if url[:5] == 'https':
                url = url.replace('https:', 'http:')
                print('Failed download. Trying https -> http instead.'
                      ' Downloading ' + url + ' to ' + fpath)
                urlretrieve(
                    url, fpath,
                    reporthook=gen_bar_updater()
                )
            else:
                raise e
        # check integrity of downloaded file
        if not dry_run and not check_integrity(fpath, md5):
            raise RuntimeError("File not found or corrupted.")


def gen_bar_updater():
    pbar = tqdm(total=None)

    def bar_update(count, block_size, total_size):
        if pbar.total is None and total_size:
            pbar.total = total_size
        progress_bytes = count * block_size
        pbar.update(progress_bytes - pbar.n)

    return bar_update


def calculate_md5(fpath, chunk_size=1024 * 1024):
    md5 = hashlib.md5()
    with open(fpath, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def check_md5(fpath, md5, **kwargs):
    return md5 == calculate_md5(fpath, **kwargs)


def check_integrity(fpath, md5=None):
    if not os.path.isfile(fpath):
        return False
    if md5 is None:
        return True
    return check_md5(fpath, md5)

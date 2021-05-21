import os
import cgi
import re
from tqdm import tqdm
from opendatasets.utils.md5 import check_integrity
import urllib

try:
    import urllib.request as request
    urlopen = request.urlopen
except Exception:
    # For Python 2.7
    import urllib
    urlopen = urllib.urlopen

try:
    import urllib.request as request
    urlretrieve = request.urlretrieve
except Exception:
    import urllib
    # For Python 2.7
    urlretrieve = urllib.urlretrieve


def download_url(url, root, filename=None, md5=None, force=False, dry_run=False):
    """Download a file from a url and place it in root.
    Args:
        url (str): URL to download file from
        root (str): Directory to place downloaded file in
        filename (str, optional): 
        Name to save the file under. If None, use the basename of the URL
        md5 (str, optional): MD5 checksum of the download. If None, do not check
    """
    root = os.path.expanduser(root)
    if not filename:
        remotefile = urlopen(url)
        _, params = cgi.parse_header(remotefile.info().get('Content-Disposition', ''))
        filename = params.get('filename')
    if not filename:
        filename = os.path.basename(url)
    fpath = os.path.join(root, filename)

    if not(os.path.exists(root)):
        os.makedirs(root)

    # check if file is already present locally
    if not force and check_integrity(fpath, md5):
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


URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_url(url):
    return re.match(URL_REGEX, url) is not None


def get_filename_cd(response):
    cd = response.headers.get('content-disposition')
    if not cd:
        return None
    _, params = cgi.parse_header(cd)
    return params.get('filename')

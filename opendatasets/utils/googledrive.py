from opendatasets.utils.network import get_filename_cd
import os
import re
import zipfile
import cgi  
from opendatasets.utils.md5 import check_integrity
from urllib.parse import urlparse
from tqdm import tqdm


def download_google_drive(url, data_dir):
    print('Downloading from Google Drive (may take a while):', url)
    file_id = _get_google_drive_file_id(url)
    fpath = download_file_from_google_drive(file_id, data_dir)
    if fpath and str(fpath).endswith('.zip'):
        try:
            with zipfile.ZipFile(fpath) as z:
                z.extractall(fpath[:-4])
            print('Downloaded and unzipped to ', fpath[:-4])
        except zipfile.BadZipFile as e:
            raise ValueError('Bad zip file! Please retry', e)
        try:
            os.remove(fpath)
        except OSError as e:
            print('Could not delete zip file, got %s' % e)
    else:
        print('Downloaded to ', fpath)


def is_google_drive_url(url):
    return url.startswith('https://drive.google.com') or url.startswith('http://drive.google.com') or url.startswith('drive.google.com')


def _get_google_drive_file_id(url):
    parts = urlparse(url)

    if re.match(r"(drive|docs)[.]google[.]com", parts.netloc) is None:
        return None

    match = re.match(r"/file/d/(?P<id>[^/]*)", parts.path)
    if match is None:
        return None

    return match.group("id")

def _quota_exceeded(response):
    return "Google Drive - Quota exceeded" in response.text


def download_file_from_google_drive(file_id, root, filename=None, md5=None):
    """Download a Google Drive file from  and place it in root.
    Args:
        file_id (str): id of file to be downloaded
        root (str): Directory to place downloaded file in
        filename (str, optional): Name to save the file under. If None, use the id of the file.
        md5 (str, optional): MD5 checksum of the download. If None, do not check
    """
    # Based on https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url
    try:
        import requests
    except ImportError as e:
        print(
            'To download from Google Drive, first install the requests library by running:')
        print('pip install requests --upgrade')
        raise e
    url = "https://docs.google.com/uc?export=download"

    root = os.path.expanduser(root)
    fpath = os.path.join(root, filename or file_id)

    os.makedirs(root, exist_ok=True)

    if os.path.isfile(fpath) and check_integrity(fpath, md5):
        print('Using downloaded and verified file: ' + fpath)
    else:
        session = requests.Session()
        response = session.get(url, params={'id': file_id}, stream=True)
        token = _get_confirm_token(response)
        if token:
            params = {'id': file_id, 'confirm': token}
            response = session.get(url, params=params, stream=True)

        if not filename:
            filename = get_filename_cd(response)
        if not filename:
            filename = file_id
        fpath = os.path.join(root, filename)

        if _quota_exceeded(response):
            msg = (
                "The daily quota of the file " + filename + " is exceeded and it " +
                "can't be downloaded. This is a limitation of Google Drive " +
                "and can only be overcome by trying again later."
            )
            raise RuntimeError(msg)

        _save_response_content(response, fpath)
        return fpath


def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def _save_response_content(response, destination, chunk_size=32768):
    with open(destination, "wb") as f:
        pbar = tqdm(total=None)
        progress = 0
        for chunk in response.iter_content(chunk_size):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                progress += len(chunk)
                pbar.update(progress - pbar.n)
        pbar.close()

# AGENTS.md - OpenDatasets Project Guide

> **For AI Agents & Human Developers**: This document provides comprehensive information about the OpenDatasets project structure, architecture, and implementation details.

## Project Overview

**OpenDatasets** is a Python library that simplifies downloading datasets from multiple online sources through a unified Python API. It provides easy access to curated datasets and supports downloads from Kaggle, Google Drive, raw HTTP/HTTPS URLs, and pre-configured curated datasets.

- **Version**: 0.1.22
- **License**: MIT License (Copyright 2020 Jovian.ml)
- **Repository**: https://github.com/JovianML/opendatasets
- **PyPI Package**: `opendatasets`
- **Python Version**: Python 3.5+
- **Maintained by**: [Jovian.ai](https://www.jovian.ai) team

## Quick Reference

### Installation
```bash
pip install opendatasets --upgrade
```

### Basic Usage
```python
import opendatasets as od

# Download from Kaggle
od.download('https://www.kaggle.com/tunguz/us-elections-dataset')

# Download from Google Drive
od.download('https://drive.google.com/file/d/FILE_ID/view')

# Download from raw URL
od.download('https://example.com/dataset.csv')

# Download curated dataset
od.download('stackoverflow-developer-survey-2020')
```

## Project Structure

```
opendatasets/
├── opendatasets/              # Main package directory
│   ├── __init__.py            # Primary entry point - exports download() function
│   ├── _version.py            # Version string (0.1.22)
│   ├── utils/                 # Core utility modules
│   │   ├── __init__.py        # Helper functions for raw file downloads
│   │   ├── network.py         # HTTP/HTTPS URL downloading with retry logic
│   │   ├── kaggle_api.py      # Official Kaggle API integration
│   │   ├── kaggle_direct.py   # Direct Kaggle scraping (fallback method)
│   │   ├── googledrive.py     # Google Drive file downloading
│   │   ├── archive.py         # Multi-format archive extraction
│   │   └── md5.py             # MD5 checksum verification
│   └── datasets/              # Curated dataset definitions (plugin system)
│       ├── __init__.py
│       ├── stackoverflow-developer-survey-2020/
│       ├── countries-languages-spoken/
│       ├── owid-covid-19-latest/
│       └── state-of-javascript-{2016,2017,2018,2019}/
├── data/                      # Sample dataset storage (not in package)
├── scripts/                   # Build and publish automation scripts
│   ├── clean                  # Removes build artifacts
│   └── publish                # Builds and publishes to PyPI
├── setup.py                   # Package configuration and metadata
├── requirements.txt           # Development dependencies
├── README.md                  # User-facing documentation
├── LICENSE                    # MIT License
└── .gitignore                 # Standard Python exclusions
```

## Architecture & Design Patterns

### 1. Main Entry Point (`opendatasets/__init__.py`)

**Primary API**: `download(dataset_id_or_url, data_dir='.', force=False, dry_run=False, **kwargs)`

**Download Detection & Routing Logic**:
1. Check if URL is a Kaggle dataset → route to `download_kaggle_dataset()`
2. Check if URL is a Google Drive link → route to `download_google_drive()`
3. Check if URL is a raw HTTP/HTTPS URL → route to `download_url()`
4. Otherwise, treat as curated dataset ID → dynamically import from `datasets/` directory

**Return Value**: Path to downloaded/extracted files

### 2. Plugin Architecture for Curated Datasets

Each curated dataset is a subdirectory under `opendatasets/datasets/` with its own `__init__.py` containing a `download()` function:

```python
def download(dataset_id, data_dir, dry_run=False, **kwargs):
    # Implementation specific to this dataset
    # Usually downloads from GitHub raw content
    pass
```

**Adding New Curated Datasets**:
1. Create new directory: `opendatasets/datasets/new-dataset-name/`
2. Add `__init__.py` with `download()` function
3. Dataset automatically available via `od.download('new-dataset-name')`

**Current Curated Datasets**:
- `stackoverflow-developer-survey-2020` - Stack Overflow Developer Survey 2020
- `owid-covid-19-latest` - COVID-19 statistics by Our World in Data
- `state-of-javascript-2016` to `2019` - State of JavaScript annual surveys
- `countries-languages-spoken` - Languages spoken in different countries

### 3. Module Responsibilities

#### `utils/network.py` - HTTP/HTTPS Downloads
**Key Function**: `download_url(url, data_dir='.', filename=None, force=False, md5=None, dry_run=False)`

**Features**:
- Progress bars via `tqdm`
- Automatic HTTPS → HTTP fallback on SSL errors
- Content-Disposition header parsing for filenames
- MD5 integrity verification
- Streaming downloads for large files
- Resume capability check

**Usage Pattern**:
```python
from opendatasets.utils.network import download_url
download_url('https://example.com/data.csv', data_dir='./data')
```

#### `utils/kaggle_api.py` - Kaggle Integration
**Key Functions**:
- `download_kaggle_dataset(dataset_url, data_dir, force=False, dry_run=False)`
- `read_kaggle_creds(dataset_url)` - Reads credentials from `kaggle.json`

**Authentication Flow**:
1. Check for `kaggle.json` in current directory
2. If not found, check `~/.kaggle/kaggle.json`
3. If still not found, prompt user interactively using `click`
4. Credentials format: `{"username": "YOUR_USERNAME", "key": "YOUR_API_KEY"}`

**Kaggle Credential Setup**:
Users obtain credentials from https://kaggle.com/me/account → API → Create New API Token

**File Location**: `opendatasets/utils/kaggle_api.py:53-89`

#### `utils/kaggle_direct.py` - Direct Kaggle Scraping
**Purpose**: Fallback method when official API has limitations

**Key Functions**:
- `get_kaggle_dataset_id(dataset_url)` - Extracts dataset ID from URL
- `get_kaggle_download_hash(dataset_id)` - Scrapes download hash from Kaggle page

**When Used**: When Kaggle API restrictions require alternative access method

#### `utils/googledrive.py` - Google Drive Downloads
**Key Function**: `download_file_from_google_drive(file_id, data_dir, filename=None, force=False)`

**Google Drive URL Parsing**:
- Extracts file ID from URLs like: `https://drive.google.com/file/d/FILE_ID/view`
- Handles various Google Drive URL formats

**Features**:
- Handles large file confirmations
- Detects and handles quota exceeded errors
- Automatic ZIP extraction
- Session management for auth tokens
- Streaming downloads with progress bars

**File Location**: `opendatasets/utils/googledrive.py:10-71`

#### `utils/archive.py` - Archive Extraction
**Key Function**: `extract_archive(from_path, to_path=None, remove_finished=False)`

**Supported Formats**:
- `.zip` - ZIP archives
- `.tar` - TAR archives
- `.tar.gz`, `.tgz` - Gzipped TAR archives
- `.tar.xz`, `.txz` - XZ compressed TAR archives
- `.gz` - Gzipped files

**Dry-Run Support**: Can preview extraction without actually extracting

**File Location**: `opendatasets/utils/archive.py:7-52`

#### `utils/md5.py` - Integrity Verification
**Key Functions**:
- `calculate_md5(fpath, chunk_size=1024 * 1024)` - Computes MD5 hash in chunks
- `check_integrity(fpath, md5=None)` - Verifies file exists and matches hash
- `check_md5(fpath, md5, **kwargs)` - Direct MD5 comparison

**Usage Pattern**:
```python
from opendatasets.utils.md5 import check_integrity
if check_integrity('file.zip', md5='abc123...'):
    print('File is valid')
```

**File Location**: `opendatasets/utils/md5.py:4-29`

#### `utils/__init__.py` - Raw File Downloads
**Key Function**: `download_raw_files(dataset_id, data_dir, dry_run, files, base_url=None)`

**Default Base URL**: `https://raw.githubusercontent.com/JovianML/opendatasets/master/data/`

**Purpose**: Downloads multiple files from GitHub raw content for curated datasets

## Key Workflows

### Workflow 1: Kaggle Dataset Download
```
User: od.download('https://www.kaggle.com/username/dataset-name')
  ↓
1. Detect Kaggle URL (via is_kaggle_url)
2. Extract dataset ID: 'username/dataset-name'
3. Read/prompt for Kaggle credentials (kaggle.json)
4. Call Kaggle API to download ZIP file
5. Extract ZIP automatically
6. Return path to extracted directory
```

**Implementation**: `opendatasets/utils/kaggle_api.py:42-89`

### Workflow 2: Google Drive Download
```
User: od.download('https://drive.google.com/file/d/FILE_ID/view')
  ↓
1. Detect Google Drive URL (via is_google_drive_url)
2. Extract file ID from URL
3. Create session and handle auth tokens
4. Download file with streaming and progress bar
5. Check for quota exceeded errors
6. Auto-extract if ZIP file
7. Return path to downloaded/extracted files
```

**Implementation**: `opendatasets/utils/googledrive.py:10-71`

### Workflow 3: Raw URL Download
```
User: od.download('https://example.com/dataset.csv')
  ↓
1. Detect as generic URL (via is_url)
2. Attempt HTTPS download
3. On SSL error, fallback to HTTP
4. Parse filename from Content-Disposition or URL
5. Verify MD5 if provided
6. Return path to downloaded file
```

**Implementation**: `opendatasets/utils/network.py:44-128`

### Workflow 4: Curated Dataset Download
```
User: od.download('stackoverflow-developer-survey-2020')
  ↓
1. Not a URL, treat as curated dataset ID
2. Create directory: ./stackoverflow-developer-survey-2020/
3. Dynamically import: opendatasets.datasets.stackoverflow-developer-survey-2020
4. Call dataset's download() function
5. Dataset downloads files from GitHub raw content
6. Return path to dataset directory
```

**Implementation**: 
- Router: `opendatasets/__init__.py:12-24`
- Dataset plugins: `opendatasets/datasets/*/`

## Dependencies

### Runtime Dependencies (Required)
```
tqdm        # Progress bars for downloads
kaggle      # Official Kaggle API (v1.5.12)
click       # Interactive credential prompts
```

### Implicit Dependencies (Used but not in install_requires)
```
requests    # HTTP library (v2.24.0)
urllib3     # URL handling (v1.25.10)
```

### Development Dependencies
```
ipython     # Interactive development
autopep8    # Code formatting
pylint      # Code linting
twine       # PyPI package publishing
```

**Installation for Development**:
```bash
conda create -n opendatasets python=3.5
conda activate opendatasets
pip install -r requirements.txt
```

## Configuration Files

### `kaggle.json` - Kaggle Credentials
**Location**: Current directory or `~/.kaggle/kaggle.json`

**Format**:
```json
{
  "username": "YOUR_KAGGLE_USERNAME",
  "key": "YOUR_KAGGLE_API_KEY"
}
```

**Obtaining Credentials**:
1. Visit https://kaggle.com/me/account
2. Scroll to API section
3. Click "Create New API Token"
4. Download `kaggle.json`

**Security Note**: Keep this file private, do not commit to version control

## API Parameters

### `download()` Function Parameters

```python
def download(dataset_id_or_url, data_dir='.', force=False, dry_run=False, **kwargs)
```

**Parameters**:
- `dataset_id_or_url` (str): Kaggle URL, Google Drive URL, raw URL, or curated dataset ID
- `data_dir` (str, optional): Directory to save files. Default: current directory
- `force` (bool, optional): Force re-download even if files exist. Default: False
- `dry_run` (bool, optional): Display URLs without downloading. Default: False
- `**kwargs`: Additional parameters passed to dataset-specific download functions

**Returns**: Path to downloaded files (str)

### Common Usage Patterns

#### Download with Custom Directory
```python
import opendatasets as od
od.download('dataset-url', data_dir='./my_data')
```

#### Force Re-download
```python
od.download('dataset-url', force=True)
```

#### Preview Without Downloading
```python
od.download('dataset-url', dry_run=True)
```

## Error Handling & Edge Cases

### Google Drive Quota Exceeded
**Error**: "Google Drive quota exceeded. Please try again later."

**Solution**: Wait and retry, or access file through browser

**Implementation**: `opendatasets/utils/googledrive.py:55-59`

### Kaggle Credentials Missing
**Behavior**: Interactive prompt using `click` library

**User Prompted For**:
1. Kaggle username
2. Kaggle API key

**Implementation**: `opendatasets/utils/kaggle_api.py:53-63`

### HTTPS SSL Errors
**Behavior**: Automatic fallback to HTTP

**Implementation**: `opendatasets/utils/network.py:110-115`

### MD5 Verification Failure
**Behavior**: Raises error if file integrity check fails

**Implementation**: `opendatasets/utils/md5.py:15-29`

### Competition Dataset Download
**Requirement**: User must accept competition rules on Kaggle before downloading

**Note**: Mentioned in README.md - no automated handling

## Build & Publish Scripts

### `scripts/publish` - PyPI Publishing
**Purpose**: Build and upload package to PyPI

**Steps**:
1. Runs `./scripts/clean` to remove old builds
2. Builds source distribution: `python setup.py sdist`
3. Builds wheel: `python setup.py bdist_wheel`
4. Uploads to PyPI: `twine upload dist/*`

**Usage**: `./scripts/publish` (requires PyPI credentials)

### `scripts/clean` - Artifact Cleanup
**Purpose**: Remove build artifacts

**Removes**:
- `build/` directory
- `dist/` directory  
- `*.egg-info` directories

**Tool Used**: `trash` command (moves to trash instead of permanent delete)

## Code Style & Conventions

### File Naming
- Module names: lowercase with underscores (`kaggle_api.py`, `network.py`)
- Dataset IDs: lowercase with hyphens (`stackoverflow-developer-survey-2020`)

### Function Naming
- All lowercase with underscores: `download_kaggle_dataset()`, `check_integrity()`

### Error Messages
- Clear, user-friendly messages
- Include actionable guidance (e.g., "Please try again later")

### Progress Reporting
- All downloads show progress bars via `tqdm`
- Status messages printed during operations
- Dry-run mode prints URLs and actions without execution

## Testing & Development

### Local Development Setup
```bash
# Clone repository
git clone https://github.com/JovianML/opendatasets.git
cd opendatasets

# Setup environment
conda create -n opendatasets python=3.5
conda activate opendatasets
pip install -r requirements.txt

# Test local changes
python -c "import opendatasets; opendatasets.download('test-dataset')"
```

### Testing Dataset Downloads
```python
# Test with dry-run
import opendatasets as od
od.download('stackoverflow-developer-survey-2020', dry_run=True)

# Test with actual download
od.download('countries-languages-spoken', data_dir='./test_data')
```

## Extension Points

### Adding New Download Sources

To support a new download source (e.g., Dropbox, AWS S3):

1. Create new module: `opendatasets/utils/newsource.py`
2. Implement URL detection function: `is_newsource_url(url)`
3. Implement download function: `download_newsource(url, data_dir, **kwargs)`
4. Add routing logic in `opendatasets/__init__.py:download()`:
   ```python
   if is_newsource_url(dataset_id_or_url):
       return download_newsource(dataset_id_or_url, data_dir)
   ```

### Adding New Curated Datasets

1. Create directory: `opendatasets/datasets/my-new-dataset/`
2. Create `__init__.py`:
   ```python
   from opendatasets.utils import download_raw_files
   
   def download(dataset_id, data_dir, dry_run=False, **kwargs):
       files = ['file1.csv', 'file2.csv']
       return download_raw_files(dataset_id, data_dir, dry_run, files)
   ```
3. (Optional) Add data files to `data/my-new-dataset/` for GitHub raw hosting
4. Update README.md with new dataset information

### Adding New Archive Formats

Edit `opendatasets/utils/archive.py:extract_archive()`:

1. Add file extension check
2. Add extraction logic using appropriate Python library
3. Update docstring with supported formats

## Common LLM Tasks

### Task: Debug Download Failure

**Investigation Steps**:
1. Check which download method is being used (Kaggle/Google Drive/URL/curated)
2. Review relevant utility module in `opendatasets/utils/`
3. Check for authentication issues (Kaggle credentials)
4. Verify URL format and accessibility
5. Check for quota/rate limiting errors

### Task: Add New Dataset Source

**Implementation Steps**:
1. Analyze target source's API/download mechanism
2. Create new utility module following existing patterns
3. Implement URL detection and download functions
4. Add routing in main `download()` function
5. Test with sample downloads
6. Update documentation

### Task: Fix Archive Extraction Bug

**Relevant Files**:
- `opendatasets/utils/archive.py` (extraction logic)
- `opendatasets/utils/network.py` (calls extraction after download)
- `opendatasets/utils/kaggle_api.py` (calls extraction for Kaggle)

### Task: Improve Error Messages

**Key Locations**:
- Exception handling in each utility module
- Interactive prompts in `kaggle_api.py`
- Download status messages in `network.py`
- Quota exceeded detection in `googledrive.py`

## Git Workflow

**Main Branch**: `master`

**Recent Commits** (as of analysis):
- `73aab91` - Update README.md
- `c42d450` - Update README.md
- `190eca1` - Update README.md
- `7cd335e` - Bump version
- `656cff0` - Merge pull request #7: fix-kaggle-issue

**Repository Status**: Clean (no uncommitted changes)

## Important Notes for AI Agents

1. **Read Before Edit**: Always read files before suggesting modifications to understand existing patterns and conventions

2. **Preserve Plugin Architecture**: When adding datasets, follow the plugin pattern - don't modify core download logic

3. **Authentication Handling**: Kaggle credentials are sensitive - never hardcode or log them

4. **Error Handling**: Match existing error handling patterns - provide clear, actionable messages

5. **Testing Requirements**: Test with `dry_run=True` before actual downloads

6. **Version Updates**: When making changes, consider if version bump is needed in `_version.py`

7. **Dependencies**: Be cautious adding new dependencies - keep the package lightweight

8. **Backward Compatibility**: Maintain existing API signatures to avoid breaking user code

9. **Documentation**: Update README.md when adding new features or datasets

10. **Security**: Be aware of potential security issues (command injection, path traversal, etc.)

## Useful Commands

```bash
# Install package locally for testing
pip install -e .

# Run cleanup
./scripts/clean

# Publish to PyPI (requires credentials)
./scripts/publish

# Check package version
python -c "import opendatasets; print(opendatasets.version())"

# Test import
python -c "import opendatasets; print('OK')"
```

## Contact & Contributing

- **Maintainer**: Jovian.ai team (hello@jovian.ml)
- **Issues**: https://github.com/JovianML/opendatasets/issues
- **Pull Requests**: Welcome! Follow existing code patterns
- **License**: MIT License - free for commercial and non-commercial use

---

**Last Updated**: 2026-01-10 (based on repository state)
**Document Version**: 1.0

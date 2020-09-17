from opendatasets.utils import download_raw_files


def download(dataset_id, data_dir, dry_run, **kwargs):
    download_raw_files(dataset_id, data_dir, dry_run, [
        'survey_results_public.csv',
        'survey_results_schema.csv',
        'README.txt'
    ])

from dataclasses import dataclass

import pandas
from google.cloud import storage
from  antenna.matching import rule_processor
from antenna.integration import get_enricher
from antenna.data import default_data_repository
from antenna.dev import file_paths
from antenna.store import GoogleStorageParameters, google_df_storage_processor
from antenna.config.file_paths import google as google_storage
from antenna.repeat_entries import repeat_entries_processor


enricher = get_enricher()

services = enricher(
    file_paths['rules'],
    file_paths['data'],
    'description',
    'service_name'
).process()

signals = enricher(
    file_paths['signals'],
    file_paths['data'],
    'description',
    'signal'
).process()


data_repo = default_data_repository()(file_paths['data'])

entries_processor = repeat_entries_processor()(
    data_repo, 'last_updated', 'item_id'
)

storage_processor_data = google_df_storage_processor()(
    data_repo.df, GoogleStorageParameters(storage.Client, google_storage['bucket'], 'test_1.csv')
).process()




# print(data_repo.get_df())
print(services)
print(signals)


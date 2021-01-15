from pandas import DataFrame
from google.cloud import storage
from dataclasses import dataclass


@dataclass
class GoogleStorageParameters:
    client: storage.Client
    bucket_name: str
    bucket_file_name: str

def google_df_storage_processor():
    def get(df: DataFrame, params: GoogleStorageParameters):
        return PandasCsvStorageProcessor(
            GoogleStorage(params), df
        )
    return get


class IBucketStorage:
    def upload_file(self, local_file_path: str):
        raise NotImplementedError

    def upload_string(self, string: str):
        raise NotImplementedError


class GoogleStorage(IBucketStorage):

    def __init__(self, params: GoogleStorageParameters):
        client = client = storage.Client()
        self.bucket = client.get_bucket(params.bucket_name)
        self.file_name = params.bucket_file_name

    def upload_file(self, local_file_path: str):
        blob = self.bucket.blob(self.file_name)
        blob.upload_from_filename(local_file_path)

    def upload_string(self, string: str):
        blob = self.bucket.blob(self.file_name)
        blob.upload_from_string(string)


class PandasCsvStorageProcessor:

    def __init__(self, storage: IBucketStorage, df: DataFrame):
        self.storage = storage
        self.df = df

    def process(self):
        df = self.df
        print(df)
        csv = df.to_csv()
        self.storage.upload_string(csv)
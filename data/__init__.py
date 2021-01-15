from antenna.data.columns import ColumnNames, EnrichedColumns
from antenna.data.repositories import PandasRepository, PandasContext
import pandas


column_names = ColumnNames()
enriched_columns = EnrichedColumns()


class DataRepository:

    file_paths = []
    repo = None

    @staticmethod
    def create(file_path):
        if not file_path in DataRepository.file_paths:
            DataRepository.file_paths.append(file_path)
            DataRepository.repo = PandasRepository(PandasContext(pandas, file_path), ColumnNames())

        return DataRepository.repo


def default_data_repository():
    def get(file_path: str):

        return DataRepository.create(file_path)

    return get
from antenna.data.columns import IDataRepository, ColumnNames
from dataclasses import dataclass
from pandas.core.frame import pandas_dtype, DataFrame
import numpy



@dataclass
class PandasContext:
    pandas: pandas_dtype
    file_path: str

    def read_data(self) -> DataFrame:
        return self.pandas.read_csv(self.file_path)

class PandasRepository(IDataRepository):

    def __init__(self, context: PandasContext, cols: ColumnNames):
        self.context = context
        self.cols = cols
        self.loaded_data = False
        self.df = None

    def add_col(self, col_name: str, values: list):
        self.get_df()[col_name] = values


    def get_values_for(self, col_name: str) -> []:
        return self.get_df()[col_name].tolist()


    def get_df(self):
        if not self.loaded_data:
            self.df = self.context.read_data()
            self.loaded_data = True

        return self.df
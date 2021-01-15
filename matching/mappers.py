from antenna.matching.rules import RuleCollection, MatchingRule
from pandas.core.frame import pandas_dtype, DataFrame
from dataclasses import dataclass
import numpy


class IRuleMapper:
    def map(self) -> RuleCollection:
        raise NotImplementedError

    def get_value_for_id(self, id: str, where_col_name: str, where_value):
        raise NotImplementedError

    def get_values_for_id(self, id: str, where_col_name: str) -> dict:
        raise NotImplementedError

@dataclass
class ColumnNames:
    identifier: str
    text_match: str = 'text_match'
    text_exclude: str = 'text_exclude'
    matching_type: str = 'matching'


@dataclass
class PandasContext:
    pandas: pandas_dtype
    file_path: str

    def read_data(self) -> DataFrame:
        return self.pandas.read_csv(self.file_path)

# class PandasDataCleaner:
    # def clean(self, string: str) -> str:
        # if str is

class PandasCsvRuleMapper(IRuleMapper):
    def __init__(self, context: PandasContext, cols: ColumnNames):
        self.context = context
        self.cols = cols
        self.df = context.pandas.DataFrame()

    def map(self) -> RuleCollection:
        cols = self.cols
        df = self.context.read_data()

        df = df.sort_values(by = cols.identifier, axis = 0)
        df.set_index(keys = [cols.identifier], drop = False)
        df = df.replace({numpy.nan: ''})

        identifiers = df[cols.identifier].unique().tolist()

        self.df = df
        rules = RuleCollection()
        for id in identifiers:
            self.map_rules(df[:][df[cols.identifier] == id], id, rules)
        return rules

    def map_rules(self, df: DataFrame, id: str, rules: RuleCollection):

        df = df[['service_id', self.cols.text_match, self.cols.text_exclude, self.cols.matching_type]]

        df = df[df[self.cols.text_match].notna()]
        df = df.groupby([
            'service_id', self.cols.matching_type, self.cols.text_match
        ])[self.cols.text_exclude].apply(list).reset_index()

        for index, row in df.iterrows():
            rules.add_rule(
               id, row[self.cols.matching_type], row[self.cols.text_match], row[self.cols.text_exclude]
            )

    def get_value_for_id(self, id: str, where_col_name: str, where_value):
        df = self.df
        return df.loc[df[where_col_name] == where_value].iloc[0][id]

    def get_values_for_id(self, id: str, where_col_name: str) -> dict:
        return self.context.pandas.Series(self.df[id].values,index=self.df[where_col_name]).to_dict()


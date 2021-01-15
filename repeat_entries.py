from pandas import DataFrame


def repeat_entries_processor():
    def get(df: DataFrame, update_col_name: str, dup_col_name: str):
        return PandasRepeatEntriesProcessor(df, update_col_name, dup_col_name)
    return get

class PandasRepeatEntriesProcessor:

    def __init__(self, df: DataFrame, update_col_name: str, dup_col_name: str):
        self.df = DataFrame
        self.update_col_name = update_col_name
        self.dup_col_name = dup_col_name

    def process(self):
        # Remove transactions that have an older entry
        self.df.sort_values(self.update_col_name).drop_duplicates(self.dup_col_name,keep='last')



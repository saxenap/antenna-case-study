from antenna.etl.matching.mapper import IRulesMapper, ColumnNames
from antenna.etl.matching.processor import MatchingRuleSet
from dataclasses import dataclass
from collections import namedtuple
from google.cloud import bigquery
import pandas_gbq
from antenna.etl.matching.mappers.pandas import PandasMapper
import pandas, numpy

@dataclass
class BigQueryPandasContext:
    pandas: pandas_gbq

class BigQueryMapper(IRulesMapper):
    def __init__(self, pandas_mapper: PandasMapper, context: BigQueryPandasContext, cols: ColumnNames):
        self.mapper = pandas_mapper
        self.context = context
        self.cols = cols

    def mapWith(self, rules: MatchingRuleSet) -> MatchingRuleSet:
        df = self.context.pandas.read_gbq(
            """
                WITH races AS (
                    SELECT service_name, matching, ARRAY_AGG(STRUCT( text_match, text_exclude)) AS text_match
                    FROM (
                        SELECT service_name, matching, text_match, STRING_AGG(text_exclude, '|') AS text_exclude
                        FROM `iconic-medley-298321.antenna_data.matching-rules`
                        WHERE text_exclude IS NOT NULL
                        GROUP BY service_name, matching, text_match
                        UNION DISTINCT 
                        SELECT service_name, matching, text_match, STRING_AGG(text_exclude,'') AS text_exclude
                        FROM `iconic-medley-298321.antenna_data.matching-rules`
                        WHERE text_exclude IS NULL
                        GROUP BY service_name, matching, text_match
                    ) 
                    GROUP BY service_name, matching
                    ORDER BY service_name
                )
                SELECT service_name, matching, text_match.text_match AS text_match, text_match.text_exclude AS text_exclude
                FROM races AS r 
                CROSS JOIN UNNEST(r.text_match) AS text_match 
            """
        )
        # print(df)
        # print(len(df.index))
        # raise SystemExit
        for index, row in df.iterrows():
            text_exclude = []
            if isinstance(row['text_exclude'], str):
                text_exclude = row['text_exclude'].split('|')
            rules.add_rule(
                index,
                row['matching'],
                row['text_match'],
                text_exclude
            )

        return rules
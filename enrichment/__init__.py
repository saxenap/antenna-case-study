import logging, logging.config
import pandas
from antenna.config.logger import conf as logger_configuration
from antenna.enrichment.generators import NegativeLookahead, ListCleaner, RegexesByIdentifierCombiner
from antenna.enrichment.patterns import Enricher, PatternTypes, StartMatchingType, AnywhereMatchingType, RegexMatchingType
from antenna.enrichment.mappers import IRuleMapper, PandasCsvRuleMapper, PandasContext, ColumnNames


logging.config.dictConfig(logger_configuration)

class DefaultEnricher:
    def __init__(self, mapper: IRuleMapper, generator: NegativeLookahead):
        self.mapper = mapper
        self.generator = generator

    # def map(self):

    def get_regexes(self) -> []:
        for rule in self.mapper.map().get_rules():
            self.generator.add_rule(rule)

        return self.generator.get_data()

    def get_value_for(self, col_name: str, when_col_name: str, when_col_value):
        return self.mapper.get_value_for_id(col_name, when_col_name, when_col_value)

    def get_dict(self, col_name, other_col: str) -> dict:
        return self.mapper.get_values_for_id(col_name, other_col)

def default_enricher():
    def from_csv(csv_path: str, service_id: str = 'service_name'):
        mapper = PandasCsvRuleMapper(
            PandasContext(pandas, csv_path),
            ColumnNames('service_name')
        )

        enrichers = PatternTypes([
            Enricher('S', StartMatchingType()),
            Enricher('A', AnywhereMatchingType()),
            Enricher('R', RegexMatchingType())
        ])
        generator = NegativeLookahead(ListCleaner(), enrichers, RegexesByIdentifierCombiner())
        return DefaultEnricher(mapper, generator)
    return from_csv

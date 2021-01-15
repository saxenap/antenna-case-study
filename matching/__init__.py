import logging, logging.config
import pandas
from antenna.matching.patterns import Enricher, PatternTypes, StartMatchingType, AnywhereMatchingType, RegexMatchingType
from antenna.matching.rule_processor import RuleProcessor
from antenna.matching.generators import NegativeLookahead, ListCleaner, RegexesByIdentifierCombiner
from antenna.matching.filters import RulesFilter
from antenna.matching.filters import TextMatchAndTextExcludesFilter, TextMatchFilter, PandasBadRulesRepo
from antenna.matching.mappers import PandasContext, PandasCsvRuleMapper, ColumnNames


def rule_processor():
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

        col_names = [v for v in  ColumnNames('service_name').__dict__.values()]
        bad_rules = pandas.DataFrame(columns = col_names)
        generator1 = NegativeLookahead(ListCleaner(), enrichers, RegexesByIdentifierCombiner())
        generator2 = RulesFilter(PandasBadRulesRepo(bad_rules), generator1)
        generator2.add_filter(TextMatchAndTextExcludesFilter())
        generator2.add_filter(TextMatchFilter())

        return RuleProcessor(mapper, generator2, bad_rules)
    return from_csv

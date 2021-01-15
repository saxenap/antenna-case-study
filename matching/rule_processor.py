from antenna.matching.generators import IGenerator
from antenna.matching.mappers import IRuleMapper, PandasCsvRuleMapper, PandasContext, ColumnNames
from antenna.matching.filters import PandasBadRulesRepo

class RuleProcessor:
    def __init__(self, mapper: IRuleMapper, generator: IGenerator, bad_rules: PandasBadRulesRepo):
        self.mapper = mapper
        self.generator = generator
        self.bad_rules = bad_rules

    def get_bad_rules(self) -> dict:
        return self.bad_rules.get_data()

    def get_regexes(self) -> []:
        for rule in self.mapper.map().get_rules():
            self.generator.add_rule(rule)
        return self.generator.get_data()

    def get_value_for(self, col_name: str, when_col_name: str, when_col_value):
        return self.mapper.get_value_for_id(col_name, when_col_name, when_col_value)

    def get_dict(self, col_name, other_col: str) -> dict:
        return self.mapper.get_values_for_id(col_name, other_col)

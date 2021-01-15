from antenna.matching.patterns import MatchingRule
from antenna.matching.generators import IGenerator, RegexByIdentifier
from pandas import DataFrame
from datetime import datetime


class PandasBadRulesRepo:
    def __init__(self, df: DataFrame):
        self.df = df

    def add_rule(self, rule: MatchingRule):
        self.df.loc[datetime.utcnow().strftime('%Y%m%d%H%M%S%f')] = [
            rule.identifier, rule.text_match, rule.get_excludes(), rule.pattern_type
        ]

    def get_data(self):
        return self.df.to_dict()

class RulesFilter(IGenerator):

    def __init__(self, repo: PandasBadRulesRepo, generator: IGenerator):
        self.generator = generator
        self.filters = []
        self.repo = repo

    def add_filter(self, filter):
        self.filters.append(filter)

    def ignore(self, rule: MatchingRule) -> bool:
        for filter in self.filters:
            if filter(rule):
                self.repo.add_rule(rule)
                return True

        return False

    def add_rule(self, rule: MatchingRule):
        if self.ignore(rule):
            return

        self.generator.add_rule(rule)

    def get_data(self) -> [RegexByIdentifier]:
        return self.generator.get_data()


class TextMatchAndTextExcludesFilter:

    def __call__(self, rule: MatchingRule):
        if rule.text_match == None or rule.text_match == '':
            if all(exclude in ['', None] for exclude in rule.get_excludes()):
                return True

        return False

class TextMatchFilter:

    def __call__(self, rule: MatchingRule):
        if rule.text_match == None or rule.text_match == '':
            return True

        return False
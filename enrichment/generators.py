from antenna.enrichment.rules import MatchingRule, RuleCollection
from antenna.enrichment.patterns import IPatternTypeEnricher
from dataclasses import dataclass


# (?!.*(Fake|Franchise|a^))^(.*CBS.*)$




@dataclass
class RegexByIdentifier:
    identifier: str
    data: str


class RegexesByIdentifierCombiner:
    def __init__(self):
        self.data = {}

    def add_data(self, identifier: str, data: str):
        if not identifier in self.data:
            self.data[identifier] = []

        self.data[identifier].append(data)

    def combine(self, char = '|') -> [RegexByIdentifier]:
        id_data = []
        for id, data in self.data.items():
            data = char.join(data)
            id_data.append(RegexByIdentifier(id, data))

        return id_data


class ListCleaner:

    def filter(self, look_in: [], bad_values: []) -> []:
        return [x for x in look_in if x not in bad_values]

    def replace(self, look_in: [], bad_values: [], good_value: str) -> []:
        return [good_value if v in bad_values else v for v in look_in]

class NegativeLookahead:

    pattern = '(?!.*({piped_excludes}))^({single_text_match})$'

    def __init__(
            self, cleaner: ListCleaner, enricher: IPatternTypeEnricher, combiner: RegexesByIdentifierCombiner
    ):
        self.cleaner = cleaner
        self.enricher = enricher
        self.combiner = combiner

    def add_rule(self, rule):

        excludes = self.cleaner.filter(rule.get_excludes(), [None, '', 'NaN', 'NAN', 'nan'])
        excludes = self.cleaner.replace(rule.get_excludes(), ['', None], 'a^')

        text_match = self.enricher.enrich(rule)
        if not text_match:
            text_match = '.*'

        self.combiner.add_data(
            rule.get_identifier(),
            self.pattern.format(piped_excludes = '|'.join(excludes), single_text_match = text_match)
        )

    def get_data(self) -> [RegexByIdentifier]:
        return self.combiner.combine('|')



@dataclass
class IdentifierData:
    identifier: str
    data: str


class JoinedIdentifierDataBuilder:
    def __init__(self):
        self.data = {}

    def add_data(self, identifier: str, data: str):
        if not identifier in self.data:
            self.data[identifier] = []

        self.data[identifier].append(data)

    def build(self, char = '|') -> [IdentifierData]:
        id_data = []
        for id, data in self.data.items():
            data = char.join(data)
            id_data.append(IdentifierData(id, data))

        return id_data

class NegativeLookbehind:
    def __init__(self, pattern_type: IPatternTypeEnricher, builder: JoinedIdentifierDataBuilder):
        self.pattern_type = pattern_type
        self.builder = builder

    def add_rule(self, rule: MatchingRule):
        self.pattern_type.enrich(rule)
        text_match = '^(' + rule.get_text_match() + ')$'

        trans_excludes = []
        excludes = rule.get_excludes()
        for exclude in excludes:
            print(exclude)
            if exclude == None or exclude == '':
                print(exclude)
                exclude = 'a^'
                print(exclude)
            exclude = '.*' + exclude
            trans_excludes.append(exclude)

        trans_excludes = '|'.join(trans_excludes)

        trans_excludes = '(?<!(' + trans_excludes + '))'

        self.builder.add_data(
            rule.get_identifier(), trans_excludes + text_match
        )

    def generate(self):
        return self.builder.build('|')


class NegativeLookahead1:
    def __init__(self, pattern_type: IPatternTypeEnricher, builder: JoinedIdentifierDataBuilder):
        self.pattern_type = pattern_type
        self.builder = builder

    def add_rule(self, rule: MatchingRule):
        self.pattern_type.enrich(rule)
        text_match = '^(' + rule.get_text_match() + ')$'

        trans_excludes = []
        excludes = rule.get_excludes()
        for exclude in excludes:
            print(exclude)
            if exclude == None or exclude == '':
                print(exclude)
                exclude = 'a^'
                print(exclude)
            exclude = '.*' + exclude
            trans_excludes.append(exclude)

        trans_excludes = '|'.join(trans_excludes)

        trans_excludes = '(?!(' + trans_excludes + '))'

        self.builder.add_data(
            rule.get_identifier(), trans_excludes + text_match
        )

    def generate(self):
        return self.builder.build('|')

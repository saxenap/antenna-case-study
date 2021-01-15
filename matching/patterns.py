from antenna.matching.rules import MatchingRule
from dataclasses import dataclass



class IPatternTypeEnricher:

    def enrich(self, string: str) -> str:
        raise NotImplementedError


@dataclass
class Enricher:
    type: str
    enricher: IPatternTypeEnricher

class PatternTypes(IPatternTypeEnricher):
    def __init__(self, enrichers: [Enricher] = None):
        if enrichers is None:
            enrichers = []
        self.enrichers = enrichers

    def add_enricher(self, enricher: Enricher):
        self.enrichers.append(enricher)

    def enrich(self, rule: MatchingRule) -> str:

        pattern_type = rule.get_pattern_type()
        string = rule.get_text_match()

        for enricher in self.enrichers:
            if enricher.type == pattern_type:
                string = enricher.enricher.enrich(string)

        return string


class BasePatternType(IPatternTypeEnricher):

    def enrich(self, string: str) -> str:
        raise NotImplementedError


class StartMatchingType(BasePatternType):

    def enrich(self, string: str) -> str:
        return string


class RegexMatchingType(BasePatternType):

    def enrich(self, string: str) -> str:
        return string


class AnywhereMatchingType(BasePatternType):

    def enrich(self, string: str) -> str:
        return '.*' + string + '.*'
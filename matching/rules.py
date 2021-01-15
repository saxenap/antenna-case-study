from dataclasses import dataclass
from json import dumps


class MatchingRule:
    def __init__(
            self, identifier: str, pattern_type: str, text_match: str, text_excludes: []
    ):
        self.identifier = identifier
        self.pattern_type = pattern_type
        self.text_match = text_match
        self.text_excludes = text_excludes

    def get_identifier(self) -> str:
        return self.identifier

    def get_excludes(self) -> []:
        return self.text_excludes

    def get_text_match(self) -> str:
        return self.text_match

    def get_pattern_type(self) -> str:
        return self.pattern_type

    def prefix_text_match(self, prefix: str):
        self.text_match = prefix + self.get_text_match()

    def suffix_text_match(self, suffix: str):
        self.text_match = self.get_text_match() + suffix

    def decorate_text_match(self, prefix: str, suffix: str):
        self.text_match = prefix + self.get_text_match() + suffix

class RuleCollection:
    def __init__(self):
        self.rules = []

    def add_rule(self, identifier: str, pattern_type: str, text_match: str, text_excludes: []):
        self.rules.append(MatchingRule(identifier, pattern_type, text_match, text_excludes))

    def get_rules(self) -> [MatchingRule]:
        return self.rules
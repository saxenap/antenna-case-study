from dataclasses import dataclass

@dataclass
class Pattern:
    data: str

    def prefix(self, string: str):
        self.data = string + self.data

    def suffix(self, string: str):
        self.data = self.data + string

    def decorate(self, prefix: str, suffix: str):
        self.data = prefix + self.data + suffix


class PatternCollection:
    def __init__(self, texts = None):
        if texts is None:
            texts = []
        self.texts = texts

    def add_pattern(self, text: Pattern):
        self.texts.append(text)

    def prefix(self, string: str):
        for text in self.texts:
            text.prefix(string)

    def suffix(self, string: str):
        for text in self.texts:
            text.suffix(string)

    def decorate(self, prefix: str, suffix: str):
        for text in self.texts:
            text.decorate(prefix, suffix)


class TextMatch:
    def __init__(self, type: str, text_match: Pattern, text_excludes: PatternCollection):
        self.type = type
        self.text_match = text_match
        self.text_excludes = text_excludes

    def decorate_text_excludes(self, prefix: str, suffix: str):
        self.text_excludes.decorate(prefix, suffix)

    def prefix(self, string: str):
        self.text_excludes.prefix(string)

    def suffix(self, string: str):
        self.text_excludes.suffix(string)


class MatchingRule:
    def __init__(self, identifier: str):
        self.identifier = identifier
        self.text_match = Pattern('')
        self.text_excludes = PatternCollection()
        self.matching_pattern = ''

    def set_text_match(self, text_match: str, type: str, text_excludes: [str]):
        self.text_match.suffix(text_match)
        for text in text_excludes:
            self.text_excludes.add_pattern(Pattern(text))
        self.matching_pattern = type

    def exclude_text_match(self, pattern):
        return self.text_excludes

    def get_text_match(self) -> Pattern:
        return self.text_match

    def get_pattern_type(self) -> str:
        return self.matching_pattern


class IPatternType:
    def can_build(self, type: str) -> bool:
        raise NotImplementedError

    def build(self, rule: MatchingRule):
        raise NotImplementedError


class PatternTypes(IPatternType):
    def __init__(self, types: [IPatternType] = None):
        if types is None:
            types = []
        self.types = types

    def add_type(self, type: IPatternType):
        self.types.append(type)

    def can_build(self, type: str) -> bool:
        for type in self.types:
            if not type.can_handle(type):
                return False

        return True

    def build(self, rule: MatchingRule):
        for type in self.types:
            if type.can_handle(rule.get_pattern_type()):
                type.build(rule)


class BasePatternType(IPatternType):
    def __init__(self, type: str):
        self.type = type

    def can_build(self, type: str) -> bool:
        return self.type == type

    def build(self, rule: MatchingRule):
        raise NotImplementedError


class StartMatchingType(BasePatternType):
    def __init__(self, type: str = 'S'):
        BasePatternType.__init__(self, type)

    def build(self, rule: MatchingRule):
        rule.get_text_match().suffix('.*')


class RegexMatchingType(BasePatternType):
    def __init__(self, type: str = 'R'):
        BasePatternType.__init__(self, type)

    def build(self, rule: MatchingRule):
        return


class AnywhereMatchingType(BasePatternType):
    def __init__(self, type: str = 'A'):
        BasePatternType.__init__(self, type)

    def build(self, rule: MatchingRule):
        return rule.get_text_match().decorate('.*', '.*')
from enrichment.rules import MatchingRule, IPatternType

class NegativeLookahead:
    def __init__(self, pattern_type: IPatternType):
        self.pattern_type = pattern_type
        return

    def add_rule(self, rule: MatchingRule):
        self.pattern_type.build(rule)
        rule.exclude_matches.prefix('.*')

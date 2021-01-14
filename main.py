from enrichment.rules import MatchingRule, PatternTypes
from enrichment.generators import NegativeLookahead


def main():
    print('We are working.')

    rule = MatchingRule('Netflix')
    rule.set_text_match('netflix', 'A', [])
    print(rule.__dict__)

    generator = NegativeLookahead(PatternTypes())
    print(generator)

if __name__ == "__main__":
    main()
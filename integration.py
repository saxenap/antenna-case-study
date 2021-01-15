from antenna.enricher import IDataRepository as IEnrichmentDataRepository, RegexKeyMap, Regexes, EnrichmentProcessor
from antenna.data.repositories import IDataRepository
from antenna.data import default_data_repository
from antenna.matching import rule_processor
import dataclasses



class EnrichmentDataRepository(IEnrichmentDataRepository):

    repo = None

    def __init__(self, repo: IDataRepository, read_column: str, save_column1: str = ''):
        self.repo = repo
        self.read_column = read_column
        self.save_column1 = save_column1

    def get_data(self) -> [str]:
        return self.repo.get_values_for(self.read_column)

    def add_column(self, data):
        self.repo.add_col(self.save_column1, data)


def get_enricher():
    def get(rules_file_path: str, data_file_path: str, read_col: str, save_col: str) -> EnrichmentProcessor:

        _rule_processor = rule_processor()(rules_file_path)
        regexes = _rule_processor.get_regexes()

        regex_key_maps = []
        for regex in regexes:
            regex_key_maps.append(RegexKeyMap(regex.identifier, regex.data))

        return EnrichmentProcessor(
            EnrichmentDataRepository(default_data_repository()(data_file_path), read_col, save_col),
            Regexes(regex_key_maps)
        )
    return get


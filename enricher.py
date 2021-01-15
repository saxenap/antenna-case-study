from dataclasses import dataclass, asdict
import re


@dataclass
class RegexKeyMap:
    key: str
    regex: str


@dataclass
class Regexes:
    maps: [RegexKeyMap]

    def append(self, regex: RegexKeyMap):
        self.maps.append(regex)


class IDataRepository:
    def get_data(self) -> [str]:
        raise NotImplementedError

    def add_column(self, data: []):
        raise NotImplementedError


class EnrichmentProcessor:
    def __init__(self, data: IDataRepository, regexes: Regexes):
        self.data = data
        self.regexes = regexes

    def process(self):
        data = self.data.get_data()

        new_data = []
        regexes = self.regexes.maps
        for value in data:
            new_data.append(self.search_for(value, regexes))

        self.data.add_column(new_data)

    def search_for(self, value: str, regexes: [RegexKeyMap]) -> str:
        for regex_key_map in regexes:
            if re.search(regex_key_map.regex, value):
                return regex_key_map.key

        return value


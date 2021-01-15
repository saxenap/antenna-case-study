from dataclasses import dataclass

import pandas
from  antenna.matching import rule_processor
from antenna.integration import get_enricher
from antenna.data import default_data_repository


enricher = get_enricher()

services = enricher(
    '/Users/saxenap/Downloads/DE Case Study 3/ANTENNA_Data_Engineer_Matching_Rules.csv',
    '/Users/saxenap/Downloads/DE Case Study 3/ANTENNA_Data_Engineer_Test_Data.csv',
    'description',
    'service_name'
).process()

signals = enricher(
    '/Users/saxenap/Downloads/DE Case Study 3/case_study_signals.csv',
    '/Users/saxenap/Downloads/DE Case Study 3/ANTENNA_Data_Engineer_Test_Data.csv',
    'description',
    'signal'
).process()

repo = default_data_repository()('/Users/saxenap/Downloads/DE Case Study 3/ANTENNA_Data_Engineer_Test_Data.csv')
# print(repo.get_df())
print(services)
print(signals)


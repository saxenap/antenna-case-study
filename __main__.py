from  antenna.enrichment import default_enricher


if __name__ == "__main__":

    enricher = default_enricher()
    csvEnricher = enricher('/Users/saxenap/Downloads/DE Case Study 3/ANTENNA_Data_Engineer_Matching_Rules.csv')

    regexes = csvEnricher.get_regexes()
    service_ids = []
    for regex in regexes:
        service_ids.append(csvEnricher.get_value_for('service_id', 'service_name', regex.identifier))

    print(service_ids)
    print(csvEnricher.get_dict('service_id', 'service_name'))

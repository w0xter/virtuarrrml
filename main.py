from YarrrmlUtils import Yarrrml
from SparqlUtils import Sparql
from SqlUtils import Sql
import json
gtfs = "./test/gtfs/"
def main():
    query = Sparql( gtfs + 'query2/query.rq')
    mapping  = Yarrrml(gtfs + 'mapping.yaml')
    mapping.simplifyMappingAccordingToQuery(query.uris)
    sql = Sql(query.parsedQuery, mapping.simplifiyedYarrrml)
    print(json.dumps(query.splitedQuery, indent=2))
    #print(json.dumps(sql.sql, indent=2))
    #print(sql.queryStr)
if __name__ == '__main__':
    main()
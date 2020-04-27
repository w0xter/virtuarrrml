from YarrrmlUtils import Yarrrml
from SparqlUtils import Sparql
from SqlUtils import Sql
import json
def main():
    query = Sparql('./test/query.rq')
    mapping  = Yarrrml('./test/mapping.yaml')
    mapping.simplifyMappingAccordingToQuery(query.uris)
    sql = Sql(query.parsedQuery, mapping.simplifiyedYarrrml)
    print(json.dumps(sql.sql, indent=2))
    print(sql.queryStr)
if __name__ == '__main__':
    main()
from YarrrmlUtils import Yarrrml
from SparqlUtils import Sparql
from SqlUtils import Sql
import json
gtfs = "./test/gtfs/"
directory  = "query1/"
def main():
    query = Sparql( gtfs + directory + 'query.rq')
    mapping  = Yarrrml(gtfs + 'mapping.yaml')
    mapping.simplifyMappingAccordingToQuery(query.uris, query.splitedQuery)
    sql = Sql(mapping.splitedUris, mapping.simplifiyedYarrrml)
    writeResult(gtfs+directory+'splittedSparqlUrisIntoRequirements.json', mapping.splitedUris)
    writeResult(gtfs+directory+'sqlQuery.json', sql.sql)
    sql.writeQuery(gtfs+directory+'query.sql')

def writeResult(path, data):
    #Saving Results
    f = open(path, 'w')
    f.write(json.dumps(data, indent=2))
    f.close()
if __name__ == '__main__':
    main()
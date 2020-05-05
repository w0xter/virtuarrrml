from YarrrmlUtils import Yarrrml
from SparqlUtils import Sparql
from SqlUtils import Sql
import json
import sys
dataset = "./test/gtfs/"
queryDir  = "query2/"
def main():
    query = Sparql( dataset + queryDir + 'query.rq')
    mapping  = Yarrrml(dataset + 'mapping.yaml')
    writeResult(dataset + queryDir + "queryUris.json", query.uris)
    mapping.simplifyMappingAccordingToQuery(query.uris, query.splitedQuery)
    mapping.writeSimplifiedMapping(dataset + queryDir + "mapping.simplified.yaml")
    writeResult(dataset+queryDir+'splittedSparqlUrisIntoRequirements.json', mapping.splitedUris)
    sql = Sql(mapping.splitedUris, mapping.simplifiyedYarrrml)
    writeResult(dataset+queryDir+'sqlQuery.json', sql.sql)
    sql.writeQuery(dataset+queryDir+'query.sql')

def writeResult(path, data):
    #Saving Results
    f = open(path, 'w')
    f.write(json.dumps(data, indent=2))
    f.close()
if __name__ == '__main__':
    main()
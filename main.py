from YarrrmlUtils import Yarrrml
from SparqlUtils import Sparql 
import json
def main():
    query = Sparql('./test/query.rq')
    mapping  = Yarrrml('./test/mapping.yaml')
    mapping.simplifyMappingAccordingToQuery(query.uris)
    print(json.dumps(query.uris, indent=2))
    print(json.dumps(mapping.simplifiyedYarrrml, indent=2))
if __name__ == '__main__':
    main()
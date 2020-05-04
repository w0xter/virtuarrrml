import rdflib
import json

class RdflibUtils:
    def __init__(self, query="test/motivationexample/query3/queryUris.json", path="test/motivationexample/mapping.ttl"):
        self.g = None
        self.rdf = None
        self.query = json.loads(open(query).read())
        self.construct= {}
        self.__intializeGraph(path)
        self.__buildConstructor()
        self.__run_query()
    def __intializeGraph(self, path):
        self.g = rdflib.Graph()
        self.g.parse(path, format="ttl")
    def __buildConstructor(self):
        prefixes = "PREFIX semweb: <http://semweb.mmlab.be/ns/rml#>\nPREFIX r2rml: <http://www.w3.org/ns/r2rml#>\n"
        construct = "construct {\n"
        where = "} where {\n"
        for i,tm in enumerate(self.query.keys()):
            where += "?TM_%s a r2rml:TriplesMap.\n?TM_%s r2rml:subjectMap ?sbm_%s.\n?TM_%s semweb:logicalSource ?lgsrc_%s.\n"%(str(i),str(i),str(i), str(i), str(i))
            construct += "?TM_%s a r2rml:TriplesMap.\n?TM_%s r2rml:subjectMap ?sbm_%s.\n?TM_%s semweb:logicalSource ?lgsrc_%s.\n"%(str(i),str(i),str(i), str(i), str(i))
            for j,uri in enumerate(self.query[tm]["uris"]):
              construct += "?TM_%s r2rml:predicateObjectMap ?pom_%s.\n"%(str(i), str(i) + str(j))
              where += "?TM_%s r2rml:predicateObjectMap ?pom_%s.\n?pom_%s r2rml:predicateMap ?p_%s.\n?p_%s r2rml:constant <%s>.\n"%(str(i),
            str(i) + str(j),
            str(i) + str(j), 
            str(i) + str(j),
            str(i) + str(j), uri)

        where += "}"
        self.construct = prefixes + construct + where
    def __run_query(self):
        print(self.construct)
        self.qres = self.g.query(self.construct)
        #print(list(self.g))

a = RdflibUtils()

for rows in a.qres:
    print(rows)

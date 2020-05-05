import rdflib
import json

RDFschema = rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#")
SEMWEB = rdflib.URIRef("http://semweb.mmlab.be/ns/rml#")
R2RML = rdflib.URIRef("http://www.w3.org/ns/r2rml#")
RDF = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
defaultInitNs = {"rdfschema":RDFschema, "semweb":SEMWEB, "r2rml":R2RML}
class RdflibUtils:
    def __init__(self, query="test/gtfs/query2/queryUris.json", path="test/gtfs/mapping.ttl"):
        self.g = None
        self.rdf = None
        self.query = json.loads(open(query).read())
        self.minGraph = None
        self.__intializeGraph(path)
        self.__filterPredicates()
        self.__buildMinGraph()
        self.__MinGraph_to_ttl()
        
    def __intializeGraph(self, path):
        self.g = rdflib.Graph()
        self.minGraph = rdflib.Graph()
        self.g.parse(path, format="ttl")

    def __buildMinGraph(self):
        self.__expandPoms()
        self.__expandJoinCondition()
        self.__expandTMs()
        self.__expandSubjectMaps()
        self.__expandLogicalSource()
        #for tpo in self.minGraph:
        #    print(tpo)

    def __expandTMs(self):
        for s,p,o in self.minGraph.triples((None, RDF+ "type", R2RML + "TriplesMap")):
            query ="""
                construct {
                <%s> r2rml:subjectMap ?sbjMap.
                ?sbjMap a r2rml:SubjectMap.
                <%s> semweb:logicalSource ?lgsrc.
                ?lgsrc a semweb:LogicalSource.
                }
                where {
                <%s> r2rml:subjectMap ?sbjMap;
                semweb:logicalSource ?lgsrc.
                }
            """%(s,s,s)
            self.__addQueryResultToGraph(query)
    def __expandSubjectMaps(self):
        for s,p,o in self.minGraph.triples((None, RDF+ "type", R2RML + "SubjectMap")):
            query="""
                construct{
                <%s> ?p ?o.
                }where{
                <%s> ?p ?o.
                }
            """%(s,s)
            self.__addQueryResultToGraph(query)
    def __expandLogicalSource(self):
        for s,p,o in self.minGraph.triples((None, RDF+ "type", SEMWEB + "LogicalSource")):
            query="""
                construct{
                <%s> ?p ?o.
                }where{
                <%s> ?p ?o.
                }
            """%(s,s)
            self.__addQueryResultToGraph(query)
    def __expandJoinCondition(self):
        for s,p,o in self.minGraph.triples((None, R2RML + "joinCondition", None)):
            query="""
                construct{
                <%s> ?p ?o.
                }where{
                <%s> ?p ?o.
                }
            """%(o,o)
            self.__addQueryResultToGraph(query)                         
    def __expandPoms(self):
        for s,p,o in self.minGraph.triples((None, RDF+ "type", R2RML + "PredicateObjectMap")):
            query = """
            construct {
                <%s> ?p ?o.
                ?o ?o_p ?o_o.
                ?pTM a r2rml:TriplesMap.
            }where{
            <%s> ?p ?o.
            ?o ?o_p ?o_o.
            OPTIONAL{
            ?o r2rml:ParentTriplesMap ?pTM.
            }   
            }         
            """%(s, s)
            self.__addQueryResultToGraph(query)
    def __filterPredicates(self):
        construct = "construct {\n"
        where = "} where {\n"
        for i,tm in enumerate(self.query.keys()):
            where += """?TM_%s a r2rml:TriplesMap."""%(str(i))
            construct += """?TM_%s a r2rml:TriplesMap."""%(str(i))
            for j,uri in enumerate(self.query[tm]["uris"]):
              construct += """
              ?TM_%s r2rml:predicateObjectMap ?pom_%s.
              ?pom_%s a r2rml:PredicateObjectMap.
              """%(str(i),str(i) + str(j),str(i) + str(j))
              where += """
              ?TM_%s r2rml:predicateObjectMap ?pom_%s.
              ?pom_%s r2rml:predicateMap ?p_%s.
              ?p_%s r2rml:constant <%s>.
              """%(
            str(i),
            str(i) + str(j),
            str(i) + str(j), 
            str(i) + str(j),
            str(i) + str(j),
            uri                                            
            )

        where += "}"
        self.__addQueryResultToGraph(construct + where)

    def __addQueryResultToGraph(self, query):
        result = self.g.query(query, initNs=defaultInitNs)
        for tpo in result:
            self.minGraph.add(tpo)

    def __graph_to_nt(self):
        self.g.serialize(format="nt", destination="test/gtfs/mapping.nt")
    def __MinGraph_to_ttl(self):
        self.minGraph.serialize(format="ttl", destination="test/gtfs/query2/mapping.min.ttl")


a = RdflibUtils()

#for rows in a.qres:
#    print(rows)

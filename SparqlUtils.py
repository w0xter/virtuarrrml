import BashUtils as bash 
import GeneralUtils as utils
class Sparql:
    def __init__(self, path):
        self.path = path
        self.rawQuery = ""
        self.parsedQuery = {}
        self.uris = {}

    def __readQuery(self):
        f = open(self.path, 'r', encoding='utf-8')
        self.rawQuery = f
        
    def __parseQuery(self):
        parsedQuery = bash.parseSparqlQuery(self.path)
        self.parsedQuery = parsedQuery

    def __getUrisFromQuery(self):
        result = {}
        for el in self.parsedQuery['where']:
            if 'patterns' in el.keys():
                for tp in el['patterns']:
                    if('patterns' in tp.keys()):
                        for tp1 in tp['patterns']:
                            result.update(self.extractTriplePatternUris(result, tp1))
                    else:
                        result.update(self.extractTriplePatternUris(result, tp))
            else:
                result.update(self.extractTriplePatternUris(result, el))
        self.uris = result

    def extractTriplePatternUris(self, result, el):
        if('triples' in el.keys()):
            for tm in el['triples']:
                subject = tm['subject']['value']
                uri = tm['predicate']['value']
                if(subject not in result.keys()):
                    result[subject] = {'uris':[], 'fullTM':False}
    #                TMOfJoin = getSubjectInsideTPO(s,query)
    #                if(TMOfJoin != '')):
    #                    findSubjectOfJoin(TMOfJoin, mapping)
    #            if(isUri(subject)):
    #               subjectUri = findSubjectInMapping(subject, mapping) TODO
    #                result[subject]['uris'].append(subject)
                if(utils.isUri(uri)):
                    if(uri == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'):
                        uri = tm['object']['value']
                        if not  'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in result[subject]['uris']:
                            result[subject]['uris'].append('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
                    if(not uri in result[subject]['uris']):
                        result[subject]['uris'].append(uri)
                else:
                    result[subject]['fullTM'] = True
        return result
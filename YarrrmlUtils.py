import yaml
class Yarrrml:
    def __init__(self, path):
        self.path = path
        self.yarrrml = {}
        self.__readYarrrml()
    def __readYarrrml(self):
        f = open(self.path, 'r', encoding='utf-8')
        self.yarrrml = yaml.load(f, Loader=yaml.FullLoader)
    def setYarrrml(self, newYarrrml):
        self.yarrrml = newYarrrml

    def getSources(self):
        result = {}
        for tm in self.yarrrml["mappings"]:
            result[tm] = self.yarrrml["mappings"]["sources"][0] # we are assuming that every TM only have one source
        return result
    def getTm(self, tm):
        if(tm in self.yarrrml["mappings"]):
            return self.yarrrml["mappings"][tm]
        else:
            raise Exception("Invalid TM name:{} is not included in the Mappnig".format(tm))
    

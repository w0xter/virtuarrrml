import GeneralUtils as utils

class Sql:
    def __init__(self, query, mapping):
        self.sparql = query
        self.mapping = mapping
        self.sql = {}
        self.queryStr = []
        self.__createSqlQuery()
        self.__writeQuery()

    def __createSqlQuery(self):
        for tm in self.mapping["mappings"].keys():
            self.__tm2Sql(tm)
        self.__createSqlStrings()

    def __tm2Sql(self, tm):
        result = {"source":"", "select":[], "conditions":[], "alias":[]}
        subject = self.mapping["mappings"][tm]["s"]
        result["source"] = self.mapping["mappings"][tm]["sources"][0]["table"]
        predicateObjects = self.mapping["mappings"][tm]["po"]
        cols = utils.cleanColPattern(subject)
        for col in cols:
            uri = tm +  "_" + col
            result["alias"].append(uri)
        result["select"].extend(cols)        
        for po in predicateObjects:
            if(type(po) is not dict):
                cols = utils.cleanColPattern(po)
                for col in cols:
                    uri = tm + "_" + utils.getLastElementFromUri(po[0]) + "_" + col
                    result["alias"].append(uri)
                result["select"].extend(cols)
        self.sql[tm] = result
        
    def __createSqlStrings(self):
        for tm in self.sql.keys():
            result = "SELECT "
            for i,col in enumerate(self.sql[tm]["select"]):
                result += "%s AS %s,"%(col, self.sql[tm]["alias"][i])
            result = result[:-1] + " FROM %s "%(self.sql[tm]["source"])
            if(len(self.sql[tm]["conditions"]) != 0):
                result += " WHERE TODO"
            self.queryStr.append(result)
    def __writeQuery(self): 
        f = open("test/result.sql", '+a')
        for querie in self.queryStr:
            f.write(querie + ";" + "\n")




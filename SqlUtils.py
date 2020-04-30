import GeneralUtils as utils

class Sql:
    def __init__(self, query, mapping):
        self.sparql = query
        self.mapping = mapping
        self.sql = {}
        self.queryStr = []
        self.__createSqlQuery()
        self.writeQuery()

    def __createSqlQuery(self):
        for tm in self.mapping["mappings"].keys():
            self.__tm2Sql(tm)
        self.__createSqlStrings()

    def __tm2Sql(self, tm):
        result = {"source":"", "select":[], "conditions":[], "alias":[]}
        subject = self.mapping["mappings"][tm]["s"]
        result["source"] = self.mapping["mappings"][tm]["sources"][0]["table"]
        predicateObjects = self.mapping["mappings"][tm]["po"]
        cols = utils.cleanColPattern(subject) #Getting Subject
        for col in cols:
            uri = tm +  "_" + col
            result["alias"].append(uri)
        result["select"].append({"type":"mandatory", "columns":cols})        
        for po in predicateObjects:
            if(type(po) is not dict):
                tpoType = "mandatory" if po[0] in self.sparql[tm]["mandatory"] else "optional"
                cols = utils.cleanColPattern(po)
                for col in cols:
                    uri = tm + "_" + utils.getLastElementFromUri(po[0]) + "_" + col
                    result["alias"].append(uri)
                if(len(cols) > 0):
                    result["select"].append({"type":tpoType, "columns":cols})
        self.sql[tm] = result
        
    def __createSqlStrings(self):
        for tm in self.sql.keys():
            selection = "SELECT "
            conditions = "WHERE "
            for i,obj in enumerate(self.sql[tm]["select"]):
                for col in obj["columns"]:
                    selection += "%s AS %s,"%(col, self.sql[tm]["alias"][i]) + "\n" #TODO \n only for developing!!!
                    conditions += "%s IS NOT NULL AND \n"%(self.sql[tm]["alias"][i]) if self.sql[tm]["select"][i]["type"] is "mandatory" else ""
            #Remember to remove only last char if goes to production!!
            selection = selection[:-2] + " FROM %s "%(self.sql[tm]["source"]) + "\n" #TODO \n only for developing!!!
            #Remember to remove only last 4 char if goes to production!!
            conditions = conditions[:-5]
            if(len(self.sql[tm]["conditions"]) != 0):
                selection += " WHERE TODO"
            self.queryStr.append(selection + " " + conditions)
    def writeQuery(self, path="tmp/result.sql"): 
        f = open(path, 'w')
        result =""
        for querie in self.queryStr:
            result += querie + ";" + "\n"
        f.write(result)
        f.close()




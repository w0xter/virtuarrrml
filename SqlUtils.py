import GeneralUtils as utils
import sys
class Sql:
    def __init__(self, requirements, mapping):
        self.queryRequirements = requirements
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
        conditions = []
        if "filter" in self.queryRequirements[tm].keys():
            conditions = self.__generateFilters(self.queryRequirements[tm]["filter"])            
        result = {"source":"", "select":[], "conditions":conditions, "alias":[]}
        subject = self.mapping["mappings"][tm]["s"]
        result["source"] = self.mapping["mappings"][tm]["sources"][0]["table"]
        predicateObjects = self.mapping["mappings"][tm]["po"]
        cols = utils.cleanColPattern(subject) #Getting Subject
        for col in cols:
            uri = tm +  "_" + col
            result["alias"].append(uri)
        result["select"].append({"type":"mandatory", "columns":cols, "variable":self.queryRequirements[tm]["subjectVar"]})        
        for po in predicateObjects:
            if(type(po) is not dict):
                tpoType = "mandatory" if po[0] in self.queryRequirements[tm]["mandatory"]["predicates"] else "optional"
                predicatePosition = self.queryRequirements[tm][tpoType]["predicates"].index(po[0])
                cols = utils.cleanColPattern(po)
                for col in cols:
                    uri = tm + "_"  + col
                    result["alias"].append(uri)
                if(len(cols) > 0):
                    result["select"].append({
                        "type":tpoType,
                        "columns":cols,
                        "variable":self.queryRequirements[tm][tpoType]["objects"][predicatePosition]})
        self.sql[tm] = result
        
    def __createSqlStrings(self):
        for tm in self.sql.keys():
            selection = "SELECT "
            conditions = "WHERE "
            for i,obj in enumerate(self.sql[tm]["select"]):
                for j,col in enumerate(obj["columns"]):
                    selection += "%s AS %s"%(col, self.sql[tm]["alias"][i])
                    selection += ",\n" if j < len(obj["columns"]) - 1 else "" #TODO \n only for developing!!!
                    conditions += "%s IS NOT NULL "%(self.sql[tm]["alias"][i]) if self.sql[tm]["select"][i]["type"] is "mandatory" else ""
                    conditions += "AND \n" if (j < len(obj["columns"]) - 1) and self.sql[tm]["select"][i]["type"] is "mandatory" else "" #TODO \n only for developing!!!
                if i < len(self.sql[tm]["select"]) - 1:
                    selection += ",\n"
                    conditions += "AND \n" if self.sql[tm]["select"][i]["type"] is "mandatory" else ""

            selection += " FROM %s "%(self.sql[tm]["source"]) + "\n" #TODO \n only for developing!!!
            if(len(self.sql[tm]["conditions"]) != 0):
                
                conditions += "AND " if(len(conditions) > 0) else ""
                conditions += self.__generateStringSqlConditions(tm,self.sql[tm]["conditions"])
            self.queryStr.append(selection + " " + conditions)

    def writeQuery(self, path="tmp/result.sql"): 
        f = open(path, 'w')
        result =""
        for i,querie in enumerate(self.queryStr):
            result += "(" + querie + ")" + "\n"
            result += " JOIN " if i < len(self.queryStr) - 1 else ";"
        f.write(result)
        f.close()

    def __sqlOperator(self, op):
        sameOps = ["<", ">", "=", ">=", "<="]
        if(op in sameOps):
            return op
        elif(op == "&&"):
            return "AND"
        elif (op == "||"):
            return "OR"
        else:
            print("Actually we don't support this operator: %s"%(op))
            sys.exit()

    def __generateFilters(self, filters, result=[]):
        for _filter in filters:
            if(_filter["type"] == "operation"):
                op = self.__sqlOperator(_filter["operator"])
                condition = {"operator":op, "args":[]}
                for arg in _filter["args"]:
                    if("termType" in arg.keys()):
                        condition["args"].append(arg)
                    elif("type" in arg.keys()):
                        condition["args"].extend(self.__generateFilters(arg, []))
                result.append(condition)
        return result

    def __sparqlDataType2Sql(self, arg):
        xsd = "http://www.w3.org/2001/XMLSchema#"
        dataType = arg["datatype"]["value"] 
        value = arg["value"]
        if(dataType == xsd + "string"):
            return '%s'%(value)
        return value

    def __generateStringSqlConditions(self,tm,conditions):        
            result= ""
            for i,condition in enumerate(conditions):
                result += self.__travelConditionArgs(tm,condition["operator"],condition["args"])
                result += "AND" if i < len(conditions) - 1 else ""
            return result 
            

    def __travelConditionArgs(self, tm, operator, args):
            result = "("
            for i, arg in enumerate(args):
                if("termType" in arg.keys()):
                    if(arg["termType"] == "Literal"):
                        result += self.__sparqlDataType2Sql(arg) + " "
                    elif(arg["termType"] == "Variable"):
                        result += self.__getSqlALias(tm,arg["value"]) + " "
                elif("type" in arg.keys()):
                    result += self.__travelConditionArgs(tm, arg["operator"], arg["args"])
                result +=  operator + " " if i < len(args) - 1 else ""
            result += ")"
            return result

    def __getSqlALias(self, tm,var):
        for i,col in enumerate(self.sql[tm]["select"]):
            if(var == col["variable"]):
                return self.sql[tm]["alias"][i]
            else:
                print("Review SqlUtils L 132")
                print("Tm: %s Var: %s"%(str(tm), str(var)))


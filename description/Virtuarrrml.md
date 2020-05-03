# Virtuarrrml

###### Virtual knowledge graph  creation from yarrrml mappings

#### How it works?

**Virtuarrrml** born from the idea of mapping simplification through the *Sparql* query constrains.

Given a *Sparql* query and a *yarrrml* mapping we are ables to generate a simplified version of the mapping that contains only the constrains of the query. From this simplified version we extract the associated columns of each Subject and Object and generate a *SQL* query according to the conditions of the query.

The query conditions(For now) could be:

- Subject or Object instantiation.
- Variable Filter.
- Optional TPO.

The idea is simple:

##### 1.  Query Parsing:

   1. The first step is build an abstract representation of the query, to compose the final *SQL* query. So we identify the different subjects of the query and we build a *json* file where the different *TPOs* and filters associated to each subject.
   2. [Problems identified](./QueryParsingProblems.md)

##### 2. Mapping Simplification:

   1. Once the query is parsed we need to simplify the mapping to fit only the constrains. This is done by reading the different predicates of the query and selecting only the predicates objects of the Triples Map that are mentioned on the query.
      Now we have:
      - A mapping filtered which contains the columns that store the information needed. 
      - A parsed query where is specified  the conditions that must follow the returned information.
   2. [Problems identified](./MappingSimplificationProblems.md)

##### 3. Query Translation:

   1. Combining the parsed query and the filtered mapping we build a *json* structure where the objects(*TMs*) contains a list of filters, a list of elements and a list of alias to each column 
      (To ensure that we don't have duplicate column names in case of two columns of two different tables share the same name).  

      Those elements include:  

      - The columns and the variable name of the origin query.
      - The Predicate.
      - The condition of the *TPO* (optional/mandatory).

##### 4. Query Building:

   1. Following schema created on *3.1* we build a string applying the syntax of the *SQL* language.
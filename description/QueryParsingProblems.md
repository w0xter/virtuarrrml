# Virtuarrrml

### Query Parsing Problems:

#### Index:

- **[Extracting filters from the original query](#Extracting filters from the original query)**

### Extracting filters from the original query  

1. **We need to link each column with his condition.**
   A filter can be composed by one or more conditions, so we must identify for each condition:
- His column/s (If the filter it's composed by 2 variables we have to find the column of both of them).
   - 
   - His literal (If the condition it's composed by a literal and a variable)

2. **We need to link each condition with the rest of the conditions of the filter.** Following the logical operators used to combine them.

#### How can we do this?

Given this query:

```SPARQL
PREFIX ex: <http://example.com/> 
SELECT * WHERE {
    ?color a ex:Color.
    ?color ex:name ?colorName.
    ?color ex:complementary ?complementary.
    ?fruit a ex:Fruit.
    ?fruit ex:origin ?fruitOrigin.
    FILTER(?colorName = "yellow" && ?fruitOrigin = "spain")
}
```

The best way to parse this filter:

`FILTER(?colorName = "yellow" && ?fruitOrigin = "spain")`  

is creating an array of objects that follows this structure:

```json
{"filters":[ {
   "type":"condition",
   "operator":"&&",
   "conditions":[{
       "type":"condition",
       "value":{
           "operator":"=",
           "conditions":[{
               "type":"variable",
               "value":"colorName",
               "subject":"color"
           },
           {
               "type":"literal",
               "value":"yellow"
           }]
       }
   },
  {
       "type":"condition",
       "value":{
           "operator":"=",
           "conditions":[{
               "type":"variable",
               "value":"fruitOrigin",
               "subject":"fruit"
           },
           {
               "type":"literal",
               "value":"spain"
           }]
       }
   }]
 }]}
```


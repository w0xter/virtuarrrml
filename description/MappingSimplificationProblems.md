# Virtuarrrml

## Mapping simplification problems

#### Index:

- **[Subject and Object instantiation](#Subject and Object instantiation)**



### Subject and Object instantiation

The main **problem** on the **mapping simplification** it's the **instantiation**. We have to be ables to simplify the mapping file to fit only the requirements given by a query of this type:

```SPARQL
select * where {
    <http://example.com/Color/yellow> ?p1 ?o1.
    ?s2 ?p2 <http://example.com/Fruit/banana>.
    ?s3 ?p3 "yellow"^^<http://www.w3.org/2001/XMLSchema#string>.
}

```



With the previous query it's quite complicated to generate a simplified version of  the mapping, us as humans can easily understand what it's requesting this query.

- The first *TPO* aim to all the subjects and predicates of *TM* color and select me all where the *name* column of [colors.csv](/description/data/colors.csv) it's ***"yellow"***.
- The second *TPO* it's asking for all the *TPOs* where the *Object* it's a Fruit and from those *TPOs* select only the ones where the ***name*** column of [fruits.csv](/description/data/fruits.csv) it's ***"banana"*** .
- The last *TPO* request all the *TPOs* where the object it's a string and the value of that string is ***"yellow"***.

#### How can we solve this?

From the point of view of **Virtuarrrml** the the two first problems have the same solution. 

Taking a look to the first *TPO* we've realize that is requesting for the predicates and objects of the ***color*** *TM*. In our [Mapping](/description/data/mapping.yaml)  the subject of the ***color*** *TM* looks like this:
`s: http://example.com/Color/$(name)`

**how can we relate a instantiated subject with his generic shape?** 

*REGEX* it's the answer. 

If we build a regular expression for each subject of the [Mapping](/description/mapping.yaml) and travel those *REGEXs* to find the one that fit the instantiated subject we finally obtains the *TM* to which the subject belongs.

The second *TPO* can solved with this method too. But it's a bit complex. If we apply the previous method can occurs two things:

1. We find the TM which fits with the given *URI*, so we travel the mapping and select those *TMs* that have a join with the founded *TM*.
2. We didn't find any *TM* that fits with the given *URI* this means that the *URI* is not the subject of any *TM* so the *URI* must be an object where the *datatype* is *iri* . Now we have to find all the predicate objects which the object *datatype* is *iri*. 

The third *TPO* can be solved selecting all the predicates objects where the datatype is an string and then filtering the results selecting only the ones where the value is ***yellow***.


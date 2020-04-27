#!/bin/bash
file=$1
sparqljs $file > test/sparql.json
wait
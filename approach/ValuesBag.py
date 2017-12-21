from SPARQLWrapper import SPARQLWrapper, JSON

from approach.config.paths import *
from approach.config.imports import *

class ValuesBag(object):

    def __init__(self, prediction, popularity):
        self.prediction    = prediction
        self.popularity    = popularity
        self.predictionUrl = self.getPredictionUrl()
        self.values        = self.getValues()

    def getPredictionUrl(self):
        temp = self.prediction.split(":")
        prediction = temp[1]
        return "http://dbpedia.org/ontology/"+ str(prediction)

    def getValues(self):
        query = "select ?s ?p ?o where { \
            ?s ?p ?o . \
            ?s rdf:type <" + self.predictionUrl + "> . \
            filter (isNumeric(?o)) \
            filter (?p != <http://dbpedia.org/ontology/wikiPageID>) \
            filter (?p != <http://dbpedia.org/ontology/wikiPageRevisionID>) \
            } LIMIT 500"

        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)

        sparql.setQuery(query)  # the previous query as a literal string
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return self.createValuesObject(results["results"]["bindings"])

    def createValuesObject(self, results):
        valuesObject = {}
        valuesObjectClean = {}
        for result in results:
            sValue = self.getProperty(result["s"]["value"])
            pValue = self.getProperty(result["p"]["value"])
            oValue = float(result["o"]["value"])
            if pValue not in valuesObject:
                valuesObject[pValue] = []
            valuesObject[pValue].append(oValue)

        for bag in valuesObject:
            if len(valuesObject[bag]) > 5:
                if bag not in valuesObjectClean:
                    valuesObjectClean[bag] = []
                valuesObjectClean[bag] = valuesObject[bag]
        return valuesObjectClean

    def getProperty(self, numericalProperty):
        return numericalProperty[28:]

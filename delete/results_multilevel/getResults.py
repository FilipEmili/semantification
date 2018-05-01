import pandas as pd
import numbers
import math
import re
import os
import copy
import commands
import operator
import json
import numpy as np
from os.path import isfile, join
from pathlib import Path


def analyseResult(resultPath):
    avgtop1 = 0
    avgtop3 = 0
    majtop1 = 0
    majtop3 = 0

    with open(resultPath, 'r') as myfile:

        #content = myfile.readlines()
        data=myfile.read().replace('\n', '')
        dataCorrect = data.split('"invalid": [',1)[1]
        dataCorrect = dataCorrect.split('  ], ',1)[0]
        dataCorrect = dataCorrect.split('"http://dbpedia.org/ontology/')[1]
        dataCorrect = dataCorrect[:-1]

        dataResult = data.split('  "labelling": {',1)[1]
        dataResult = dataResult.split('"type": {',1)[0]
        li = dataResult.rsplit(',',1)
        dataResult = li[0]
        dataResult = "{ " + dataResult + " }"
        finalResults = json.loads(dataResult)

        counter = 0
        for d in finalResults['property']['avg']:
            if d[0] == dataCorrect and counter == 0:
                avgtop1 = 1
            if d[0] == dataCorrect and counter < 3:
                avgtop3 = 1
            counter += 1

        counter = 0
        for d in finalResults['property']['maj']:
            if d[0] == dataCorrect and counter == 0:
                majtop1 = 1
            if d[0] == dataCorrect and counter < 3:
                majtop3 = 1
            counter += 1


        return ((avgtop1, avgtop3), (majtop1, majtop3))



scoreAvg1 = 0
scoreAvg3 = 0
scoreMaj1 = 0
scoreMaj3 = 0
countAll  = 0
#sizePath = 'largeSample/large/'
#sizePath = 'mediumSample/medium/'
sizePath = 'smallSample/small/'
for fn in os.listdir(sizePath):
    resultPath = os.path.join(sizePath, fn)
    ((avgtop1, avgtop3), (majtop1, majtop3)) = analyseResult(resultPath)
    scoreAvg1 += avgtop1
    scoreAvg3 += avgtop3
    scoreMaj1 += majtop1
    scoreMaj3 += majtop3
    countAll  += 1

print sizePath
print "avg 1: " + str(scoreAvg1) + " score: " + str(scoreAvg1/float(countAll)*100)
print "avg 3: " + str(scoreAvg3) + " score: " + str(scoreAvg3/float(countAll)*100)
print "maj 1: " + str(scoreMaj1) + " score: " + str(scoreMaj1/float(countAll)*100)
print "maj 3: " + str(scoreMaj3) + " score: " + str(scoreMaj3/float(countAll)*100)
print "all: " + str(countAll)
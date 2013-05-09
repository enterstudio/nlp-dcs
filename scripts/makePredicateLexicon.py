#! /usr/bin/python
# Get the relations from the database and use these predicates as lexical triggers

import re

def camelConvert(camelCaseString):
  """Convert camel case string into a list of predicates"""
  s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camelCaseString)
  s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
  return s2.split("_")

#create a dictionary of lexical triggers for each predicate
def getPredicateTriggers(dbFile):
  """return a dictionary of lexical triggers for each predicate"""
  predTriggers={} # {predicate : set([lexical triggers]), ...}
  predPattern='^(\w+)\('
  with open(dbFile,'r') as dbfd:
    for line in dbfd:
      predicate=re.findall(predPattern, line)
      if(len(predicate)>0):
        if predTriggers.get(predicate[0]) is None:
          predTriggers[predicate[0]]=set()
        triggers = camelConvert(predicate[0])
        for trigger in triggers:
          predTriggers[predicate[0]].add(trigger)
  return(predTriggers)

def createLexiconFile(predTriggers, outFile):
  """write out the predicate triggers as in lexicon.dlog file format"""
  with open(outFile, 'w') as opfd:
    firstLine="_include('../../general/lexicon.dlog').\n\n%Lexical triggers\n"
    opfd.write(firstLine)
    beginPhrase="_lex(['"
    endPhrase="/2']).\n"
    for predicate in predTriggers:
      triggerList=""
      for trigger in predTriggers[predicate]:
        triggerList=triggerList+trigger+"', '"
      line=beginPhrase+triggerList[0:-4]+"'], ['"+predicate+endPhrase
        #line=beginPhrase+trigger+"'], ['"+predicate+endPhrase
      opfd.write(line)
    #include extra lexicon files?
    extraLines="\n\n%Other lexicon files\n"
    opfd.write(extraLines)
    for i in range(1,3):
      extraLines="_include('lexicon"+str(i)+".dlog') :- lexmode("+str(i)+").\n"
      opfd.write(extraLines)

def main():
  #databaseFile="../data/inputFiles/geo_db_2c"
  databaseFile="/u/ameliaj/nlp_proj/dcs-1.0/domains/dbquery/ibquery/1/geobase.dlog"
  #outputLexFile="../data/outputFiles/lexicon2Predicate.dlog"
  outputLexFile="/u/ameliaj/nlp_proj/dcs-1.0/domains/dbquery/ibquery/1/lexicon2Predicate.dlog"
  predTriggers=getPredicateTriggers(databaseFile)
  createLexiconFile(predTriggers, outputLexFile)

if __name__=="__main__":
  main()

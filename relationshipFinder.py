import sys
import getopt
import scrapePurple
import operator

commonwordfilter = ['the', 'of', 'and', 'a', 'to', 'in', 'is', 'that', 'it', 'was', 'for', 'on', 'are', 'as', 'with','they','or']

def diagnose(string):
   """
   Accepts a string
   Returns a list of Wordmaps
   A word map is a map with the keys ('before','word','after)
   """

   words = string.split(' ')
   if len(words) == 0:
      return None
   if len(words) == 1:
      return [{'before': None, 'word': words[0], 'after': None}]

   wordmaplist = []
   for index in range(len(words)): 
      if index == 0:
         wordmaplist.append({'before': None, 'word': words[index], 'after': words[index+1]})
      elif index == len(words) - 1:
         wordmaplist.append({'before': words[index-1], 'word': words[index], 'after': None})
      else :
         wordmaplist.append({'before': words[index-1], 'word': words[index], 'after': words[index+1]})

   return wordmaplist

def main(argv=None):
   """
   Accepts a purple chat log directory
   Returns a datastore of form
   datastore['word']={'count' : #count of this word in document
                      'after' : map of words and count
                      'before': map of words and count
                     } 
   Before and After maps are in form {'wordname1': count, 'wordname2': count, ...etc}
   """
   if argv is None:
      argv = sys.argv[1]
   
   return processPurpleDir(argv)

def addWordMaps(datastore, wordmaps):
   for wordmap in wordmaps:
      word = wordmap['word']
      if word in datastore:
         __updateWordMap(datastore, wordmap)
      else:
         beforeword = wordmap['before']
         afterword = wordmap['after']
         datastore[word]={'count': 1, 'before':{beforeword: 1}, 'after':{afterword: 1}}

def __updateWordMap(datastore, wordmap):
   word = wordmap['word']

   datastore[word]['count'] += 1

   beforeword = wordmap['before']
   afterword = wordmap['after']

   beforemap = datastore[word]['before']
   aftermap = datastore[word]['after']

   if afterword in aftermap:
      aftermap[afterword] += 1
   else :
      aftermap[afterword] = 1

   if beforeword in beforemap:
      beforemap[beforeword] += 1
   else :
      beforemap[beforeword] = 1

def processPurpleDir(filedir):
   """
   Builds a datastore from a purple file directory
   """
   linelist = scrapePurple.scrapeDir(filedir)
   return makeDatastore(linelist)

def processPurpleFile(fileloc):
   """
   Builds a datastore from a purple file directory
   """
   linelist = scrapePurple.scrapeFile(fileloc)
   return makeDatastore(linelist)

def processTextFile(fileloc):
   """
   Builds a datastore from a plain text file
   """
   import nltk.data

   tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
   filedata = open(fileloc).read()
   linelist = tokenizer.tokenize(filedata)
   return makeDatastore(linelist)

   
def makeDatastore(linelist):
   """
   Takes a list of words
   Outputs a datastore
   """
   datastore = {}

   for line in linelist:
      wordmaps = diagnose(line.lower())
      addWordMaps(datastore, wordmaps)

   return datastore 

def wordCount(datastore):
   wsum = 0
   for word in datastore.itervalues():
      wsum += word['count']
   return wsum

def getTopWordList(datastore, number=None, removeCommon=True):
   """
   Accepts a datastore and a number of words to return
   number of words defaults to all
   Returns a list of tuples size 2 in the format:
      (word, count) sorted by count descending
   """

   topWordList = sorted([word for word in datastore],key=lambda word:datastore[word]['count'], reverse=True)

   if removeCommon:
      topWordList = filter(lambda word: word not in commonwordfilter, topWordList)

   if number == None:
      number = len(topWordList)

   return topWordList[:number]

def getTopRelations(datastore, word, beforeorafter, number=None, removeCommon=True):
   """
   Accepts a datastore, word, 'before' or 'after',number
   number of words defaults to all

   Returns a list of Top relations as string sorted high to low
   """

   #Change none to correct string value
   if beforeorafter=='after':
      noneReplace = 'End of Sentence'
   else:
      noneReplace = 'Start of Sentence'

   #If None is a mapping in before or after map replace with proper identifier 
   if None in datastore[word][beforeorafter]:
      datastore[word][beforeorafter][noneReplace] = datastore[word][beforeorafter].pop(None)

   wordList = sorted([rword for rword in datastore[word][beforeorafter]], key=lambda rword: datastore[word][beforeorafter][rword], reverse=True)

   if number == None:
      number = len(wordCountList)
   
   if removeCommon:
      wordList = filter(lambda word: word not in commonwordfilter, wordList)

   return wordList[:number] 

if __name__ == "__main__":
    sys.exit(main())

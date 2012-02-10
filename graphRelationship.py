import sys
import getopt
import scrapePurple
import operator
#for key in datastore['just']['before']: sum += datastore['just']['before'][key]
#for later implementation

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
   linelist = scrapePurple.main(filedir)
   datastore = {}

   for line in linelist:
      wordmaps = diagnose(line.lower())
      addWordMaps(datastore, wordmaps)

   return datastore

def getTopWordList(datastore, number=None):
   """
   Accepts a datastore and a number of words to return
   number of words defaults to all
   Returns a list of tuples size 2 in the format:
      (word, count) sorted by count descending
   """

   wordCountPairList = sorted([(word, wordmap['count']) for (word,wordmap) in datastore.items()],key=operator.itemgetter(1), reverse=True)

   if number == None:
      number = len(wordCountList)

   return wordCountPairList[:number]

def getTopRelations(datastore, word, befereorafter, number=None):
   """
   Accepts a datastore, word, 'before' or 'after',number
   number of words defaults to all
   Returns a list of tuples size 2 in the format:
      (word, count) sorted by count descending
   """
   wordCountPairList = sorted([pair for pair in datastore[word][beforeorafter].items()], key=operator.itemgetter(1), reverse=True)

   return wordCountPairList[:number] 

if __name__ == "__main__":
    sys.exit(main())

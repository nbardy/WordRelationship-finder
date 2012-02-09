import sys
import getopt
import scrapePurple

def diagnose(string):
   words = string.split(' ')
   if len(words) == 0:
      return None
   if len(words) == 1:
      return [{'before': None, 'word': words[0], 'after': None}]

   wordmap = []
   for index in range(len(words)): 
      if index == 0:
         wordmap.append({'before': None, 'word': words[index], 'after': words[index+1]})
      elif index == len(words) - 1:
         wordmap.append({'before': words[index-1], 'word': words[index], 'after': None})
      else :
         wordmap.append({'before': words[index-1], 'word': words[index], 'after': words[index+1]})

   return wordmap

def main(argv=None):
   if argv is None:
      argv = sys.argv[1]
   
   return processFile(argv)

def addWordMaps(datastore, wordmaps):
   for wordmap in wordmaps:
      word = wordmap['word']
      if word in datastore:
         updateWordMap(datastore, wordmap)
      else:
         beforeword = wordmap['before']
         afterword = wordmap['after']
         datastore[word]={'count': 1, 'before':{beforeword: 1}, 'after':{afterword: 1}}

def updateWordMap(datastore, wordmap):
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

def processFile(filedir):
   linelist = scrapePurple.main(filedir)
   datastore = {}

   for line in linelist:
      wordmaps = diagnose(line)
      addWordMaps(datastore, wordmaps)

   return datastore

if __name__ == "__main__":
    sys.exit(main())

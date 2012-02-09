import sys
import getopt
import scrapePurple

def diagnose(string):
   words = string.split(' ')
   if len(words) == 0:
      return None
   if len(words) == 1:
      return [{'word': words[1]}]

   wordmap = []
   for index in range(len(words)): 
      if index == 0:
         wordmap.append({'word': words[index], 'after': words[index+1]})
      elif index == len(words) - 1:
         wordmap.append({'before': words[index-1], 'word': words[index]})
      else :
         wordmap.append({'before': words[index-1], 'word': words[index], 'after': words[index+1]})

   return wordmap

def main(argv=None):
   if argv is None:
      argv = sys.argv
   
   return diagnose(sys.argv[1])

def processFile(file):

   linelist = scrapePurple.main(file)
   datastore = {}

   for line in linelist:
      wordmap = diagnose(line)
      addWordMap(datastore, wordmap)
if __name__ == "__main__":
    sys.exit(main())

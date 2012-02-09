import sys
import getopt
import scrapePurple

def diagnose(line):
   words = line.split(' ')
   if len(words) == 0
      return None
   if len(words) == 1
      return {'before':None, 'word':words[0], 'after':None}
   for index in range(1,len(words)):
      if 

def main(argv=None):
   if argv is None:
      argv = sys.argv

   linelist = scrapePurple.main(sys.argv[1])
   datamap = {}

   for line in linelist:
      wordmap = diagnose(line)

if __name__ == "__main__":
    sys.exit(main())

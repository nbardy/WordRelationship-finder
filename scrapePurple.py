import os
import re
import sys
import string

def main(argv=None):   
   """
   Scrapes every file in the give directory
   Returns as a list of lines
   """
   if argv is None:
      argv = sys.argv

   directory = sys.argv[1]
   dirList = os.listdir(directory)
   datalist = []

   for filename in dirList:
         datalist += scrapedata(directory + filename) 
   
   return datalist


def scrapedata(filedir):
   """
   Scarpes data from given file
   Returns data as a list of each line
   """
   fstring = open(filedir).read()
   expr = ':</b></font>\s([\s\w]*)<br/>'
   return re.findall(expr, fstring)

if __name__ == "__main__":
   sys.exit(main())

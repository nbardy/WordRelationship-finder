import os
import re
import sys

def main(argv=None):   
   """
   Scrapes every file in the give directory
   Returns as a list of lines
   """
   if argv is None:
      argv = sys.argv[1]
   
   return scrapeDir(argv)

def scrapeDir(directory):
   """
   Scrapes data from all files given directory
   Returns data as a list of lines
   """

   dirList = os.listdir(directory)
   datalist = []

   for filename in dirList:
         datalist += scrapeFile(directory + '/' + filename) 
   
   return datalist

def scrapeFile(filedir):
   """
   Scrapes data from given file
   Returns data as a list of each line
   """
   fstring = open(filedir).read()
   expr = ':</b></font>\s([\s\w]*)<br/>'
   return re.findall(expr, fstring)

if __name__ == "__main__":
   sys.exit(main())

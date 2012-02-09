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
         datalist += scrapedata(open(directory + filename).read()) 
   
   return datalist

def scrapedata(file):
   """
   Scarpes data from given file
   Returns data as a list of each line
   """
   expr = ':</b></font>\s([\s\w]*)<br/>'
   return re.findall(expr, file)

if __name__ == "__main__":
   sys.exit(main())

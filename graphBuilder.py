import relationshipFinder
import sys

def __jsHeader(datastore, outputfile):
   outputfile.write("""
   <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
   <script src="highcharts.js" type="text/javascript"></script>
   """)
   outputfile.write("""
   <script>
   var chart;
   $(document).ready(function() {
      
      var colors = Highcharts.getOptions().colors,
         name = 'Common Words';
   """)

   __outputchartData(datastore, outputfile) 
   
   outputfile.write("""
      function setChart(name, categories, data, color) {
         chart.xAxis[0].setCategories(categories);
         chart.series[0].remove();
         chart.addSeries({
            name: name,
            data: data,
            color: color || 'white'
         });
      }
      
      chart = new Highcharts.Chart({
         chart: {
            renderTo: 'wordGraph', 
            type: 'column'
         },
         title: {
            text: 'Most Used Words'
         },
         subtitle: {
            text: 'Click the columns to view the words used before and after. Click again to return.'
         },
         xAxis: {
            categories: categories                     
         },
         yAxis: {
            title: {
               text: 'Total percent usage'
            }
         },
         plotOptions: {
            column: {
               cursor: 'pointer',
               point: {
                  events: {
                     click: function() {
                        var drilldown = this.drilldown;
                        if (drilldown) { // drill down
                           setChart(drilldown.name, drilldown.categories, drilldown.data, drilldown.color);
                        } else { // restore
                           setChart(name, categories, data);
                        }
                     }
                  }
               },
               dataLabels: {
                  enabled: true,
                  color: colors[0],
                  style: {
                     fontWeight: 'bold'
                  },
                  formatter: function() {
                     return this.y +'%';
                  }
               }               
            }
         },
         tooltip: {
            formatter: function() {
               var point = this.point,
                  s = this.x +':<b>'+ this.y +'% usage</b><br/>';
               if (point.drilldown) {
                  s += 'Click to view '+ point.category +' versions';
               } else {
                  s += 'Click to return to common words';
               }
               return s;
            }
         },
         series: [{
            name: name,
            data: data,
            color: 'white'
         }],
         exporting: {
            enabled: false
         }
      });
      
      
   });
   </script>
   """)

def __printHeader(name, datastore, outputfile):
   outputfile.write("""
   <html>
   <head>
   <title>""")
   outputfile.write(name)
   outputfile.write("</title>")
   __jsHeader(datastore, outputfile)
   outputfile.write("</head>")

def __printBody(name, outputfile):
   outputfile.write("<body>")
   outputfile.write("<h1>" + name + "</h1>")
   outputfile.write("<div id=\"wordGraph\"></div>")
   outputfile.write("<br /><p> Open Source Code hosted at <a href='https://github.com/DivisibleZero/WordRelationship-finder'>GitHub</a>")
   outputfile.write("<br /><p>Graphing library providing by <a href='http://www.highcharts.com'>highcharts</a></p>")
   outputfile.write("</body></html>")

def __outputchartData(datastore, outputfile, size=30): 
   topWordList = relationshipFinder.getTopWordList(datastore, size)
   outputfile.write("var categories = " + str(topWordList) + ';');

   total = float(relationshipFinder.wordCount(datastore))
   datalist = []
   for word in topWordList:
      datalist.append(__getDataMap(datastore, word, total))
   
   outputfile.write("var data = " + str(datalist) + ';');

def __getDataMap(datastore, word, total):
   datamap = {}
   datamap['y'] = datastore[word]['count']/total
   datamap['color'] = "#4572A7"
   datamap['drilldown'] = {}
   subchart =  datamap['drilldown']

   subchart['name'] = word
   subchart['categories'] = relationshipFinder.getTopRelations(datastore, word, 'before', 30)
   subchart['data'] = [datastore[word]['before'][relword]/float(datastore[word]['count']) for relword in subchart['categories']]
   subchart['color'] = "#4572A7"

   return datamap

def chartFromPurpleDir(outputfilename, pdirectory):
   outputfile = open(outputfilename, "w") 
   datastore = relationshipFinder.processPurpleDir(pdirectory)
   __printHeader("Nick's Chat Logs", datastore, outputfile)
   __printBody("Nick's Chat Logs", outputfile)

def main(argv=None):
   if argv==None:
      argv = sys.argv
   chartFromPurpleDir(argv[1], argv[2])

if __name__=="__main__":
   sys.exit(main())

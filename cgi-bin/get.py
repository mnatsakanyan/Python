import requests
import csv
import datetime
import cgi
import html

class GetDataAndCreateCsv():
    def __init__(self):
        self.getData()

    def getData(self):

        form = cgi.FieldStorage()
        infoType = form.getfirst("data_type", "")
        infoType = html.escape(infoType)
        message = ''
        if infoType.lower() not in ('daily', 'montly'):
            message = 'Error: no such M or D'
            errorM = 1
            self.returnHtml(message,infoType,errorM)
            return 0
        reportType = ''
        if infoType.lower() in 'daily':
            reportType = 'D'
        elif infoType.lower() in 'montly':
            reportType = 'M'
        response = requests.get(
            "http://api.eia.gov/series/?api_key=API_KEY&series_id=NG.RNGWHHD."+reportType)
        if response.status_code == 200:
           data = response.json()

           for dayPrices in data['series']:
               csvDatas = dayPrices['data']

           with open('Gas_prices_%s.csv' % (infoType), 'w', newline='') as fp:
               thewriter = csv.writer(fp,delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
               thewriter.writerow(['Date', 'Price'])

               for csvData in csvDatas:
                    if reportType == 'D':

                       datetimeobject = datetime.datetime.strptime(csvData[0], "%Y%m%d")
                       newformat = datetimeobject.strftime('%m-%d-%Y')
                       thewriter.writerow([newformat, csvData[1]])
                    elif reportType == 'M':
                        datetimeobject = datetime.datetime.strptime(csvData[0], "%Y%m")
                        newformat = datetimeobject.strftime('%m-%Y')
                        thewriter.writerow([newformat, csvData[1]])
               message = 'The Csv file is created'

        else:
           data = "No Data"
        self.returnHtml(message,infoType)

    def returnHtml(self,message,infoType,errorM = ''):
        print("Content-type: text/html\n")
        print("""<!DOCTYPE HTML>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Result</title>
                    <script src='//d3js.org/d3.v4.min.js'></script>
                    <link rel='stylesheet' type='text/css' href='../style.css'>
                </head>
                <body>""")

        print("<h1>Request Result</h1>")
        print('<h2>'+message+'</h2>')
        if errorM != 1:
            print('<input type="hidden" id="csvFileName" value="Gas_prices_%s.csv' % (infoType)+'">')
            print("<script src='../visual.js'></script>")
        print("""</body>
                </html>""")

test = GetDataAndCreateCsv()

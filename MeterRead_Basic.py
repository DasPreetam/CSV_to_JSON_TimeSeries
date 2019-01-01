import json, dateutil.parser as parser

data,daysdict={},{}
dayslist=[]

try:
  fileoperator = open('TestFile.csv','r')
  headers=[headers.replace('\n','') for headers in fileoperator.readline().split(',')]
  for line in fileoperator:
    elements=[elements.replace('\n','') for elements in line.split(',')]
    for columns in range(0,10):
      if(headers[columns]=='UpDateTime'):
        tempdate=parser.parse(elements[columns])
        updatetime=tempdate.strftime("%Y-%m-%d")
        data[headers[columns]]=updatetime
      else:
        data[headers[columns]]=elements[columns]
    currdate=tempdate
    data['IntervalLength']=int(data['IntervalLength'])   
    data['date']="ISODate('"+currdate.isoformat()+".000Z')"
    daysdict['date']=data['date']
    daysdict['CurrentRegisterRead']=int(elements[10])
    dayslist.append(daysdict)
    data['days']=dayslist
    dayslist=[]
    with open(data['NMI']+".json", 'w') as outfile:
      json.dump(data, outfile)
    outfile.close()
  fileoperator.close()  
  print("Run Complete")
  input("Hit Return to exit")

except BaseException as e:
  print(str(e))
  input("Hit Return to exit")

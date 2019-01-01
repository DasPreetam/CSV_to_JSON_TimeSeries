import json, dateutil.parser as parser, datetime

data,daysdict,tempdict,hoursdict={},{},{},{}
minuteslist,hourslist,dayslist=[],[],[]
totalRegRead,interRegRead,rownum=0,0,1

try:
  fileoperator = open('Input/TestFile.csv','r')
  headers=[headers.replace('\n','') for headers in fileoperator.readline().split(',')]
  for line in fileoperator:
    hourslist=[]
    dayslist=[]
    totalRegRead=0
    rownum+=1
    elements=[elements.replace('\n','') for elements in line.split(',')]
    for columns in range(0,10):
      if(headers[columns]=='UpDateTime'):
        tempdate=parser.parse(elements[columns])
        updatetime=tempdate.strftime("%Y-%m-%d")
        data[headers[columns]]=updatetime
      else:
        data[headers[columns]]=elements[columns]
    currdate=tempdate    
    data['date']="ISODate('"+currdate.isoformat()+".000Z')"
    if(data['IntervalLength']=='5' and len(elements)-10==288):
      data['IntervalLength']=5
      stepsize,minutesgap=12,5
    elif(data['IntervalLength']=='30' and len(elements)-10==48):
      data['IntervalLength']=30
      stepsize,minutesgap=2,30
    else:
      print("Data Issue in row number :",rownum)
      continue   

    for columns in range(10,len(elements),stepsize):
      interRegRead=0
      for innercol in range(columns,columns+stepsize):
        tempdict['date']="ISODate('"+currdate.isoformat()+".000Z')"
        tempdict['CurrentRegisterRead']=int(elements[innercol].replace('\n',''))
        interRegRead+=int(elements[innercol])
        minuteslist.append(tempdict.copy())
        currdate+=datetime.timedelta(hours=0,minutes=minutesgap)
      hoursdict['date']=minuteslist[0]['date']
      hoursdict['CurrentRegisterRead']=interRegRead
      hoursdict['minutes']=minuteslist
      minuteslist=[]
      totalRegRead+=interRegRead
      hourslist.append(hoursdict.copy())
       
    daysdict['date']=data['date']
    daysdict['CurrentRegisterRead']=totalRegRead
    daysdict['hours']=hourslist
    dayslist.append(daysdict)
    data['days']=dayslist

    with open('Output/'+data['MeterSerialNumber']+".json", 'w') as outfile:
      json.dump(data, outfile)
    outfile.close()
  fileoperator.close()  
  print("Run Complete")
  input("Hit Return to exit")

except BaseException as e:
  print(str(e))
  input("Hit Return to exit")

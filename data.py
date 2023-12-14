
#every 20 min : 10/25-12/2 (39 days)
import json
import numpy as np
import os
from collections import defaultdict
import pandas as pd

files=[]
path = os.getcwd()+'/release'
content = sorted(os.listdir(path))#[:11] #10/2-10/11
D=defaultdict()
with open('sno_test_set.txt','r') as f:
    stations = f.read().strip('\n')
    for station in stations.split('\n'):
        D[station]=defaultdict()  # data[station i ]={date1 : [...], date2:[...]}
        for dates in content:
            if not dates.startswith('.'):
                D[station][dates]=list()


for dates in content :
    if not dates.startswith('.'):
        for date in os.listdir(os.path.join(path,dates)):
            station=date.split('.')[0]
            if station in stations:  #in target stations
                with open(os.path.join(path,dates,date)) as f:  #the 24hr data in station[i]
                    D[station][dates]=list()
                    data = json.load(f)
                    for val in data.values():
                        if len(val.values())!=0:
                            D[station][dates].append(val['sbi'])
                        else: # data is missing     
                            D[station][dates].append(-1)
                    #filled missing value
                    for i in range(len(D[station][dates])):
                        j=i+1
                        while j<len(D[station][dates]) and D[station][dates][j]!=-1:
                            D[station][dates][i]=D[station][dates][j]
                            j+=1
                        if D[station][dates][i]==-1:
                            D[station][dates][i]=0
 

#for 20 min basis
for station in stations.split('\n'):
    d = []
    for date in D[station].keys():
        D[station][date]=np.array(D[station][date]).reshape(-1,20)
        d.extend(np.mean(D[station][date],axis=1).reshape(-1,))
    #print(np.array(d).shape)
    D[station]=d
    
data = pd.DataFrame(D)
data.to_csv('station_data.csv')




    


import pandas as pd
import pickle
from collections import defaultdict
from datetime import datetime, timedelta
import numpy as np

def load_model(station_name):
    with open(f'models/{station_name}.pkl', 'rb') as f:
        model = pickle.load(f)
    return model


def time(stations_list,day_list):
    #time part :['500101001_20231026_00:00',.....]
    time = []
    current_time = datetime.strptime('00:00', '%H:%M')
    end_time = datetime.strptime('23:40', '%H:%M')
    time_interval = timedelta(minutes=20)
    time_scale = []
    while current_time <= end_time:
        time_scale.append(current_time.strftime('%H:%M'))
        current_time += time_interval


    for day in day_list:
        for station in stations_list:
            for t in time_scale:
                time.append(station+'_'+day+'_'+t)
    return time


def outputs(stations_list,pred_len):
    prediction = defaultdict(list)

    for i in range(len(stations_list)): #stations_list=['500101001','500101002',...]
        model = load_model(stations_list[i])
        pred = model.get_forecast(steps=pred_len).predicted_mean #def predict(model,pre_len)
        prediction[stations_list[i]] = np.array(pred).reshape(-1,72)

    
    result = []
    for i in range(int(pred_len/72)):
        for station in stations_list:
            result.extend(prediction[station][i])   #len=72

    return result


def answer(time, outputs):
    d = {'id':time, 'sbi':outputs}
    df = pd.DataFrame(d)
    df.reset_index()
    df.to_csv('prediction.csv')
    


#--------------------------------------------------------------------------
with open('sno_test_set.txt','r') as f:
    stations_list = f.read().split('\n')

day_list = ['20231218','20231219','20231220','20231221','20231222','20231223','20231224']
time = time(stations_list, day_list)
outputs = outputs(stations_list=stations_list,pred_len=len(day_list)*72)
answer(time, outputs)





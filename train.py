
from collections import defaultdict
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
import itertools
import statsmodels.api as sm
import pickle



D = pd.read_csv('station_data.csv')
for i in range(1,len(D.columns)):  #for every station[i]
    station_name = D.columns[i]

    data = D[station_name][-864:]
    train = data

    param = (1,1,2) #find it!
    model = SARIMAX(train, order=(param[0], param[1], param[2]),seasonal_order=(param[0], param[1], param[2], 72))
    results = model.fit()
    

    with open(f'models/{station_name}.pkl', 'wb') as f:
        pickle.dump(results, f)
    print(f"station {station_name} finished!")
    




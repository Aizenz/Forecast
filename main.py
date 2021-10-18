"""

Created by @LZJ

on 18th, Oct

"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import datetime


def best_forecast(y: str, x: str, database: pd.DataFrame, derive: int):
    data_y, data_x = database[y], database[x]
    best_fit = [0.0, 0.0]
    best_R = [0.0, 0.0]
    for i in range(derive):
        if i == 0:
            data_x_temp = data_x
        else:
            data_x_temp = data_x[:-i]
        data_y_temp = data_y[i:].reset_index(drop=True)
        data_x_temp = sm.add_constant(data_x_temp)
        model = sm.OLS(data_y_temp, data_x_temp)
        results = model.fit()
        print(results.rsquared_adj)
        if best_fit[1] < abs(results.tvalues[1]):
            best_fit[0] = i
            best_fit[1] = results.tvalues[1]
        if best_R[1] < results.rsquared_adj:
            best_R[1] = results.rsquared_adj
            best_R[0] = i

    print(best_R)
    return best_fit


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    database = pd.read_excel('/Users/aizenz/Desktop/internHI/Copy of 价格.xlsx')
    database['日期'] = pd.to_datetime(database['日期'])
    database = database.set_index('日期').resample('W').last()
    save = database.copy()
    best_fit = [0.0, 0.0]
    best_R = [0.0, 0.0]
    for i in range(20):
        database['金属硅成本'] = database['金属硅成本'].shift(i)
        temp = database.loc[:, ['金属硅成本', '金属硅价格']].dropna().reset_index(drop=True)
        x = sm.add_constant(temp['金属硅成本'])
        y = temp['金属硅价格']
        model = sm.OLS(y, x)
        results = model.fit()
        if best_fit[1] < abs(results.tvalues[1]):
            best_fit[0] = i
            best_fit[1] = results.tvalues[1]
        if best_R[1] < results.rsquared_adj:
            best_R[1] = results.rsquared_adj
            best_R[0] = i
    print(best_R, best_fit)
    #print(best_forecast('金属硅价格', '金属硅成本', database, 300))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

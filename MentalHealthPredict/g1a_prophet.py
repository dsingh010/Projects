# -*- coding: utf-8 -*-
"""G1A_PROPHET.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RUzFvNU3II5hlAXebds4mdQbwEIAS7BG

**IMPORT PACKAGES**
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from prophet import Prophet
from pandas.api.types import CategoricalDtype
from sklearn.metrics import mean_squared_error, mean_absolute_error

plt.style.use('ggplot')
plt.style.use('fivethirtyeight')

"""**LOAD DATA**"""

## TO UPLOAD ##
from google.colab import files
uploaded = files.upload()

file = 'weighted_search_trends.csv'
df = pd.read_csv(file, index_col=[0], parse_dates=True, header = 1)
df = df.reset_index()
df = df.rename(columns = {'2020-12-27' : 'Week', '51.12757872668773' : 'Metric'})
df['Week'] = pd.to_datetime(df['Week'])
df.head()

"""**FEATURES**"""

## ADJUSTED FOR DATA #####################################################

from pandas.api.types import CategoricalDtype

cat_type = CategoricalDtype(categories=['Monday','Tuesday',
                                        'Wednesday',
                                        'Thursday','Friday',
                                        'Saturday','Sunday'],
                            ordered=True)

def create_features(df, label=None):
    """
    Creates time series features from datetime index.
    """
    df = df.copy()
    df['date'] = df['Week']
    df['dayofweek'] = df['date'].dt.dayofweek
    df['weekday'] = df['date'].dt.day_name()
    df['weekday'] = df['weekday'].astype(cat_type)
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df['dayofmonth'] = df['date'].dt.day
    df['weekofyear'] = df['date'].dt.isocalendar().week
    df['date_offset'] = (df.date.dt.month*100 + df.date.dt.day - 320)%1300

    df['season'] = pd.cut(df['date_offset'], [0, 300, 602, 900, 1300],
                          labels=['Spring', 'Summer', 'Fall', 'Winter']
                   )
    X = df[['dayofweek','quarter','month','year',
           'dayofyear','dayofmonth','weekofyear','weekday',
           'season']]
    if label:
        y = df[label]
        return X, y
    return X

X, y = create_features(df, label='Metric')
features_and_target = pd.concat([X, y], axis=1)

##########################################################################

"""**TRAIN TEST SPLIT**"""

split_date = '2023-12-27'
df_train = df.loc[df['Week'] <= split_date].copy()
df_test = df.loc[df['Week'] > split_date].copy()

result = df_test \
    .rename(columns={'Metric': 'TEST SET'}) \
    .join(df_train.rename(columns={'Metric': 'TRAINING SET'}),
          how='outer',
          lsuffix='_train',
          rsuffix='_test')

"""**PROPHET MODEL**"""

df_train_prophet = df_train.reset_index() \
    .rename(columns={'Week':'ds',
                     'Metric':'y'})

# Commented out IPython magic to ensure Python compatibility.
# %%time
# model = Prophet()
# model.fit(df_train_prophet)

df_test_prophet = df_test.reset_index() \
    .rename(columns={'Week':'ds',
                     'Metric':'y'})

df_test_fcst = model.predict(df_test_prophet)
df_test_fcst.index = pd.to_datetime(df_test_fcst.index, unit='s')

"""**PLOT FORECAST**"""

fig, ax = plt.subplots(figsize=(10, 5))
fig = model.plot(df_test_fcst, ax=ax)
ax.set_title('Seasonal Affective Disorder Forecast')
plt.show()

"""**COMPONENTS**

super cool because you can see forecast for different time spans (year, month, week)!
"""

fig = model.plot_components(df_test_fcst)
plt.show()

"""**COMPARE WITH ACTUAL DATA**"""

## ALL ##
f, ax = plt.subplots(figsize=(15, 5))
ax.scatter(df_test['Week'], df_test['Metric'], color='r')
fig = model.plot(df_test_fcst, ax=ax)

## MONTH ##
lower_bound = pd.to_datetime('2021-01-01')
upper_bound = pd.to_datetime('2024-10-20')

fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(df_test.index, df_test['Metric'], color='r')
fig = model.plot(df_test_fcst, ax=ax)

ax.set_xlim(lower_bound, upper_bound)  # Changed to set_xlim
ax.set_ylim(0, 100)
plot = plt.suptitle('Forecast vs Actuals')

## WEEK ##
f, ax = plt.subplots(figsize=(15, 5))
ax.scatter(df_test.index, df_test['Metric'], color='r')
fig = model.plot(df_test_fcst, ax=ax)

lower_bound = pd.to_datetime('2021-01-01')
upper_bound = pd.to_datetime('2024-10-20')

ax.set_xlim(lower_bound, upper_bound)
ax.set_ylim(0, 100)
ax.set_title('First Week of January Forecast vs Actuals')
plt.show()

"""**EVALUATE**"""

np.sqrt(mean_squared_error(y_true=df_test['Metric'],
                   y_pred=df_test_fcst['yhat']))

mean_absolute_error(y_true=df_test['Metric'],
                   y_pred=df_test_fcst['yhat'])

import itertools
import numpy as np
import pandas as pd
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics

df_cv = cross_validation(model, initial='763 days', period='105 days', horizon='217 days')

param_grid = {
    'changepoint_prior_scale': [0.001, 0.01, 0.1, 0.5],
    'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0],
}

# Generate all combinations of parameters
all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
rmses = []  # Store the RMSEs for each params here

# Use cross validation to evaluate all parameters
for params in all_params:
    m = Prophet(**params).fit(df_train_prophet)  # Fit model with given params
    df_cv = cross_validation(m, initial='763 days', period='105 days', horizon='217 days', parallel="processes")
    df_p = performance_metrics(df_cv, rolling_window=1)
    rmses.append(df_p['rmse'].values[0])

# Find the best parameters
tuning_results = pd.DataFrame(all_params)
tuning_results['rmse'] = rmses
print(tuning_results)

best_params = {
    'changepoint_prior_scale': 0.100,
    'seasonality_prior_scale': 10.00,
}

m = Prophet(**best_params).fit(df_train_prophet)

m_test_fcst = m.predict(df_test_prophet)
m_test_fcst.index = pd.to_datetime(df_test_fcst.index, unit='s')

f2, ax2 = plt.subplots(figsize=(15, 5))
ax2.scatter(df_test['Week'], df_test['Metric'], color='r')
fig = model.plot(m_test_fcst, ax=ax2)

np.sqrt(mean_squared_error(y_true=df_test['Metric'],
                   y_pred=m_test_fcst['yhat']))

mean_absolute_error(y_true=df_test['Metric'],
                   y_pred=m_test_fcst['yhat'])

"""**ACCOUNT FOR HOLIDAYS**
default code found online -- haven't checked functionality
"""

from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

cal = calendar()

holidays = cal.holidays(start=df['Week'].min(),
                        end=df['Week'].max()
                        return_name=True)

holiday_df = pd.DataFrame(data=holidays,
                          columns=['holiday'])

holiday_df = holiday_df.reset_index().rename(columns={'index':'ds'})
holiday_df.head()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# model_with_holidays = Prophet(holidays=holiday_df)
# model_with_holidays.fit(df_train_prophet)

df_test_fcst_with_hols = \
    model_with_holidays.predict(df=df_test_prophet)

fig = model_with_holidays.plot_components(
    df_test_fcst_with_hols)
plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(df_test.index, df_test['Mental Health Support: (United States)'], color='r')
fig = model.plot(df_test_fcst_with_hols, ax=ax)

lower_bound = pd.to_datetime('2021-01-01')
upper_bound = pd.to_datetime('2024-10-20')

ax.set_xlim(lower_bound, upper_bound)
ax.set_ylim(0, 100)
plot = plt.suptitle('Predictions')

np.sqrt(mean_squared_error(y_true=df_test['Mental Health Support: (United States)'],
                   y_pred=df_test_fcst_with_hols['yhat']))

mean_absolute_error(y_true=df_test['Mental Health Support: (United States)'],
                   y_pred=df_test_fcst_with_hols['yhat'])

future = model.make_future_dataframe(periods=365*24, freq='h', include_history=False)
forecast = model_with_holidays.predict(future)

forecast[['ds','yhat']].head()
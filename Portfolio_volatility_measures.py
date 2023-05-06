import datetime as dt
import pandas as pd
import numpy as np

from pandas_datareader import data as pdr
import plotly.offline as pyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pyo.init_notebook_mode(connected=True)
pd.options.plotting.backend = 'plotly'

end = dt.datetime.now()
start = dt.datetime(2015,1,1)
df = pdr.get_data_yahoo(['^AXJO', 'CBA.AX','NAB.AX','STO.AX','WPL.AX'], start, end)
Close = df.Close
Close.head()

log_returns = np.log(df.Close/df.Close.shift(1)).dropna()
log_returns

daily_std = log_returns.std()
annualized_std = daily_std * np.sqrt(252)
annualized_std

fig = make_subplots(rows=2, cols=2)
trace0 = go.Histogram(x=log_returns['CBA.AX'], name='CBA')
trace1 = go.Histogram(x=log_returns['NAB.AX'], name='NAB')
trace2 = go.Histogram(x=log_returns['STO.AX'], name='STO')
trace3 = go.Histogram(x=log_returns['WPL.AX'], name='WPL')
fig.append_trace(trace0, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace2, 2, 1)
fig.append_trace(trace3, 2, 2)
fig.update_layout(autosize = False, width=700, height=600, title='Frequency of log returns',
                  xaxis=dict(title='CBA Annualized Volatility: ' + str(np.round(annualized_std['CBA.AX']*100, 1))),
                  xaxis2=dict(title='NAB Annualized Volatility: ' + str(np.round(annualized_std['NAB.AX']*100, 1))),
                  xaxis3=dict(title='STO Annualized Volatility: ' + str(np.round(annualized_std['STO.AX']*100, 1))),
                  xaxis4=dict(title='WPL Annualized Volatility: ' + str(np.round(annualized_std['WPL.AX']*100, 1))))
fig.show()

TRADING_DAYS = 60
volatility = log_returns.rolling(window=TRADING_DAYS).std()*np.sqrt(TRADING_DAYS)
volatility.tail()
volatility.plot().update_layout(autosize = False, width=600, height=300).show()

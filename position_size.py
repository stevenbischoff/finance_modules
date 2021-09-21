import pandas as pd
import datetime as dt
import sys

def optimal_returns(returns1, returns2, start_date, end_date):

  returns_df = pd.DataFrame(columns=['returns'])

  for i in range(1, 10):
    for j in range(1, 10):

      returns_df.loc[str(i)+str(j), 'returns'] = sizing_returns(
        returns1, returns2, i/100, j/100, start_date, end_date)

  returns_df['returns'] = pd.to_numeric(returns_df['returns'])

  return returns_df


def sizing_returns(returns1, returns2, i_temp, j_temp, start_date, end_date):

  delta = dt.timedelta(days=1)
  bank_series = pd.Series()

  while start_date <= end_date:
    date_return(returns1, returns2, i_temp, j_temp, start_date, bank_series)    
    start_date += delta

  bank = bank_series.product()

  return bank


def date_return(returns1, returns2, i_temp, j_temp, date, bank_series):

  returns1_date = returns1.loc[returns1['Date'] == date, 'profit']
  returns2_date = returns2.loc[returns2['Date'] == date, 'profit']

  n_open1, n_open2 = len(returns1_date), len(returns2_date)

  if n_open1 == 0 and n_open2 == 0:
    return

  if len(returns1_date) > 0:
    returns1_date_total = i_temp*len(returns1_date)*(returns1_date.mean() - 1)
  else:
    returns1_date_total = 0
  if len(returns2_date) > 0:
    returns2_date_total = j_temp*len(returns2_date)*(returns2_date.mean() - 1)
  else:
    returns2_date_total = 0

  bank_series[date] = 1 + returns1_date_total + returns2_date_total
  

def max_drawdown(cumulative_bank_series):
  drawdown_series = cumulative_bank_series/cumulative_bank_series.cummax() - 1
  max_drawdown = drawdown_series.min()
  
  return max_drawdown

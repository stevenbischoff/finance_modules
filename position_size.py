import pandas as pd
import numpy as np
import itertools
import datetime as dt
import sys

def optimal_returns(returns_list, start_date, end_date):

  returns_df = pd.DataFrame(columns=['pct', 'returns'])

  size_list = np.linspace(0, 0.1, 11)

  for prod in itertools.product(size_list, repeat=len(returns_list)):
    prod_returns = sizing_returns(returns_list, start_date, end_date, prod)
    returns_df = returns_df.append(pd.Series(
      {'pct':prod, 'returns': prod_returns}), ignore_index=True)

  returns_df['returns'] = pd.to_numeric(returns_df['returns'])

  return returns_df


def sizing_returns(returns_list, start_date, end_date, prod):

  delta = dt.timedelta(days=1)
  bank_series = pd.Series()

  while start_date <= end_date:
    date_return(returns_list, start_date, bank_series, prod)    
    start_date += delta

  bank = bank_series.product()

  return bank

def date_return(returns_list, date, bank_series, prod):

  date_token, date_return = 0, 1
  for i in range(len(returns_list)):
    buy_pct = prod[i]
    return_series = returns_list[i]
    returns_date = return_series.loc[return_series['Date'] == date, 'profit']

    n_open = len(returns_date)
    if n_open == 0:
      continue
    date_token = 1

    returns_date_total = buy_pct*n_open*(returns_date.mean() - 1)
    date_return += returns_date_total
    
  if date_token == 0:
    return

  bank_series[date] = date_return
  

def max_drawdown(bank_series):
  cumulative_bank_series = bank_series.cumprod()
  drawdown_series = cumulative_bank_series/cumulative_bank_series.cummax() - 1
  max_drawdown = drawdown_series.min()
  
  return max_drawdown

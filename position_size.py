import pandas as pd
import numpy as np
import itertools
import datetime as dt
import sys

def optimal_returns(returns_list, max_drawdown, max_position_size, start_date, end_date):
  """
  Parameters
    returns_list : iterable
    max_drawdown : float
    max_position_size : float
    start_date : datetime.datetime
    end_date : datetime.datetime
  Calculates returns for an arbitrary number of strategies that each have an arbitrary number
  of actions in a particular time period, subject to a maximum drawdown constraint 
  """

  returns_df = pd.DataFrame(columns=['pct', 'returns', 'largest drawdown'])

  size_list = np.linspace(0.0, max_position_size, int(max_position_size*100 + 1))

  for prod in itertools.product(size_list, repeat=len(returns_list)):
    prod_returns = sizing_returns(returns_list, start_date, end_date, prod)
    
    largest_drawdown = calculate_largest_drawdown(prod_returns)
    if abs(largest_drawdown) > abs(max_drawdown):
      continue
    
    bank = prod_returns.product()
    returns_df = returns_df.append(
      pd.Series({'pct':prod, 'returns': bank, 'largest drawdown':largest_drawdown}),
      ignore_index=True)

  returns_df['returns'] = pd.to_numeric(returns_df['returns'])

  return returns_df


def sizing_returns(returns_list, start_date, end_date, prod):
  """
  Parameters
    returns_list : iterable
    start_date : datetime.datetime
    end_date : datetime.datetime
    prod : iterable
  """

  delta = dt.timedelta(days=1)
  bank_series = pd.Series()

  while start_date <= end_date:
    date_return(returns_list, start_date, bank_series, prod)    
    start_date += delta

  return bank_series


def date_return(returns_list, date, bank_series, prod):
  """
  Parameters
    returns_list : iterable
    date : datetime.datetime
    bank_series : Pandas series
    prod : iterable
  """
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
  

def calculate_largest_drawdown(bank_series):
  """
  Parameters
    bank_series : Pandas series
      Returns is 1 + (period pct return). E.g. a 2 pct return is represented as 1.02.
  """
  cumulative_bank_series = bank_series.cumprod()
  drawdown_series = cumulative_bank_series/cumulative_bank_series.cummax() - 1
  largest_drawdown = drawdown_series.min()
  
  return largest_drawdown

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
  bank = 1

  while start_date <= end_date:
    bank = date_return(returns1, returns2, i_temp, j_temp, start_date, bank)
    start_date += delta

  return bank


def date_return(returns1, returns2, i_temp, j_temp, date, bank):

  returns1_date = returns1.loc[returns1['Date'] == date, 'profit']
  returns2_date = returns2.loc[returns2['Date'] == date, 'profit']

  if len(returns1_date) > 0:
    returns1_date_total = i_temp*len(returns1_date)*(returns1_date.mean() - 1)
  else:
    returns1_date_total = 0
  if len(returns2_date) > 0:
    returns2_date_total = j_temp*len(returns2_date)*(returns2_date.mean() - 1)
  else:
    returns2_date_total = 0

  bank *= 1 + returns1_date_total + returns2_date_total

  return bank 

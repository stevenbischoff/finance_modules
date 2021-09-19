import pandas as pd
import datetime as dt

def optimal_returns(returns1, returns2, start_date, end_date):

  returns_df = pd.DataFrame(columns=['returns'])

  for i in range(1, 10):
    for j in range(1, 10):

      returns_df.loc[str(i)+str(j), 'returns'] = sizing_returns(
        returns1, returns2, i, j, start_date, end_date)

  returns_df['returns'] = pd.to_numeric(returns_df['returns'])

  return returns_df


def sizing_returns(returns1, returns2, i, j, start_date, end_date):

  i_temp = i/100
  j_temp = j/100

  returns1['temp'] = 1 + i_temp*(returns1['profit'] - 1)
  returns2['temp'] = 1 + j_temp*(returns2['profit'] - 1)

  delta = dt.timedelta(days=1)
  bank = 1

  while start_date <= end_date:
    bank = date_return(returns1, returns2, start_date, bank)
    start_date += delta

  return bank

def date_return(returns1, returns2, date, bank):

  returns1_date = returns1.loc[returns1['Date'] == date, 'temp']
  returns2_date = returns2.loc[returns2['Date'] == date, 'temp']

  if len(returns1_date) > 0:
    bank *= returns1_date.product()
  if len(returns2_date) > 0:
    bank *= returns2_date.product()

  return bank 

import pandas as pd



def fix_rent(data: pd.DataFrame ) -> pd.DataFrame:
    """ if rent is not paid at the end of the month the payment is made beginning of next month
    this results in 2x rent in one month
    So find month that has no rent, then take rent of next month and put it a month earlier
    """
    unique_months = data['monat'].unique()
    df = data
    print(unique_months)
    for month in unique_months:
        
        #df = data[month]
        print('-------------------FIX RENT ---------------------------')

        df_1 = df[(df['Zahlungsempfänger*in'] == 'Hans Schneider') & (df['monat'] == 'January')]
        df = df[(df['Zahlungsempfänger*in'] == 'Hans Schneider') & (df['monat'] == month)]
        #df = df[df['monat'] == 'January']
        print(month + type(month))
        print(type(month))
        print(type('january'))
        print(df)
        #if df != None:
        #    break
        #else:
        #    break

        


    return data
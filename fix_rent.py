import pandas as pd



def fix_rent(data: pd.DataFrame ) -> pd.DataFrame:
    """ if rent is not paid at the end of the month the payment is made beginning of next month
    this results in 2x rent in one month
    So find month that has no rent, then take rent of next month and put it a month earlier
    """

    month_dict = {"January": "December",
                   "February": "January", 
                   "March": "February", 
                   "April":"March", 
                   "May":"April", 
                   "June": "May", 
                   "July": "June", 
                   "August":"July", 
                   "September":"August", 
                   "October":"September", 
                   "November":"October", 
                   "December":"November",
    }

    unique_months = data['monat'].unique()
    df = data
    print(unique_months)
    monthly_rent = []
    for month in unique_months:
        
        #df = data[month]
        print('-------------------FIX RENT ---------------------------')
        
        #df_1 = df[(df['Zahlungsempfänger*in'] == 'Hans Schneider') & (df['monat'] == 'January')]
        df_monthly = df[(df['Zahlungsempfänger*in'] == 'Hans Schneider') & (df['monat'] == month)]
        monthly_rent.append(df_monthly)
        
        df_rent = pd.concat(monthly_rent, axis=0, ignore_index=True)
        #print(df_rent)

        #if df_rent.shape[0] > 1:



    print(df_rent)
    for idx, month in enumerate(df_rent["monat"]):
        #month_before = month
        if df_rent.iloc[idx-1, 13] == month:
            print(f"The Correct Month instead of {month} - would be: {month_dict[month]}")
            #print(month_dict[month])
            df_rent.iloc[idx, 13] = month_dict[month]
        #print(month)
    print('------------------ REEEEEEEEENT ---------------------------')
    print(df_rent)

    df_rent = df_rent.drop(columns=["Wertstellung","Status","Zahlungspflichtige*r","Verwendungszweck","Umsatztyp","IBAN","Gläubiger-ID","Mandatsreferenz","Kundenreferenz","jahr","categories","consumption_categories"], axis=1)
    print(df_rent)
    df = df.merge(right=df_rent, how= 'left', on = ['Zahlungsempfänger*in', "Betrag (€)", "Buchungsdatum"])
    print(df.columns)
    df_monthly = df[df['Zahlungsempfänger*in'] == 'Hans Schneider']
    print(df_monthly)

    print(df)



    data = df
    

    return data
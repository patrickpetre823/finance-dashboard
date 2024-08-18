import pandas as pd



def fix_rent(data: pd.DataFrame ) -> pd.DataFrame:
    """ if rent is not paid at the end of the month the payment is made beginning of next month
    this results in 2x rent in one month
    So find month that has no rent payment, then take rent of next month and put it a month earlier
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
 
    monthly_rent = []
    for month in unique_months:
        
        df_monthly = df[(df['Zahlungsempfänger*in'] == 'Hans Schneider') & (df['monat'] == month)]
        monthly_rent.append(df_monthly)
        
        df_rent = pd.concat(monthly_rent, axis=0, ignore_index=True)


    for idx, month in enumerate(df_rent["monat"]):

        if df_rent.iloc[idx-1, 13] == month:
            df_rent.iloc[idx, 13] = month_dict[month]



    df_rent = df_rent.drop(columns=["Wertstellung","Status","Zahlungspflichtige*r","Verwendungszweck","Umsatztyp","IBAN","Gläubiger-ID","Mandatsreferenz","Kundenreferenz","jahr","categories","consumption_categories"], axis=1)

    df = df.merge(right=df_rent, how= 'left', on = ['Zahlungsempfänger*in', "Betrag (€)", "Buchungsdatum"])

    df_monthly = df[df['Zahlungsempfänger*in'] == 'Hans Schneider']

    # Replacing the months in the monat column, then dropping the monat_y 
    df["monat_x"] = df["monat_y"].fillna(df["monat_x"])

    df = df.drop("monat_y", axis=1)
    df = df.rename(columns={'monat_x': 'monat'})


    

    return df
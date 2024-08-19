import pandas as pd
import numpy as np
import csv
import sys, os
from langchain_community.llms import Ollama
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from components.layout import create_layout
from os.path import dirname, join
import calendar
import glob
import os
from fix_rent import fix_rent
from categorize_transfer import categorize_transfer




def main() -> None:
    data = load_data()
    data = fix_rent(data)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Finance Dashboard"
    app.layout = create_layout(app, data)
    app.run()



def load_data() -> pd.DataFrame:
    
    
    col_names = ["Buchungsdatum","Wertstellung","Status","Zahlungspflichtige*r","Zahlungsempfänger*in","Verwendungszweck",
                 "Umsatztyp","IBAN","Betrag (€)","Gläubiger-ID","Mandatsreferenz","Kundenreferenz"]
    
    path = r'C:\Patrick\VSCode\Git_bank' 
    all_files = glob.glob(os.path.join(path , "*.csv"))

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, on_bad_lines='warn', names=col_names, delimiter=';')
        df = df.iloc[5:]
        li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)
    df = df.drop_duplicates()
    



    df['Buchungsdatum'] = pd.to_datetime(df['Buchungsdatum'], dayfirst=True)
    df['jahr'] = df['Buchungsdatum'].dt.year.astype(str)
    df['monat'] = df['Buchungsdatum'].dt.month
    df['monat'] = df['monat'].apply(lambda x: calendar.month_name[x])

    df_clean = categorize_transfer(df)

    df_clean = df_clean[df_clean["Umsatztyp"]=="Ausgang"]



    df_clean["Betrag (€)"] = df_clean['Betrag (€)'].str.replace('.','')
    df_clean["Betrag (€)"] = pd.to_numeric(df_clean['Betrag (€)'].astype(str).str.replace(',','.'))


    #df_clean.to_csv('clean.csv')

    print("------------------------------------")
    df_wohnen = df_clean[(df_clean['consumption_categories'] == 'Wohnen') & (df_clean['monat'] == 'July')]
    print(df_wohnen)
    print("------------------------------------")
    df_essen = df_clean[df_clean["consumption_categories"]=="Nahrungsmittel"]

    df_monthly = df_clean.groupby(['monat', 'consumption_categories'])["Betrag (€)"].sum()
    
    print(df_monthly.head(7))

    return df_clean


if __name__ == '__main__':
    main()


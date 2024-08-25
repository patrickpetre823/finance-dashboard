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

    li_csv = []


    # Loading all csv files that are in the folder
    for filename in all_files:
        df = pd.read_csv(filename, on_bad_lines='warn', names=col_names, delimiter=';')
        df = df.iloc[5:]
        li_csv.append(df)

    # Concat the files
    df = pd.concat(li_csv, axis=0, ignore_index=True)
    df = df.drop_duplicates()
    

    # Fromatting date to datetime
    df['Buchungsdatum'] = pd.to_datetime(df['Buchungsdatum'], dayfirst=True)
    df['jahr'] = df['Buchungsdatum'].dt.year.astype(str)
    df['monat'] = df['Buchungsdatum'].dt.month
    df['monat'] = df['monat'].apply(lambda x: calendar.month_name[x])

    df_clean = categorize_transfer(df)

    df_clean = df_clean[df_clean["Umsatztyp"]=="Ausgang"]

    # Fromatting numeric 
    df_clean["Betrag (€)"] = df_clean['Betrag (€)'].str.replace('.','')
    df_clean["Betrag (€)"] = pd.to_numeric(df_clean['Betrag (€)'].astype(str).str.replace(',','.'))


    #df_clean.to_csv('clean.csv')

    return df_clean


if __name__ == '__main__':
    main()


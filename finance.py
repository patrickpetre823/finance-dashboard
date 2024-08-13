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

#current_dir = dirname(__file__)
#file_path = join(current_dir, "./Umsatzliste_Girokonto")

file_path = 'C:\\Patrick\\VSCode\\Git_bank\\Umsatzliste_Girokonto2.csv'

def main() -> None:
    data = load_data(file_path)
    data = fix_rent(data)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Finance Dashboard"
    app.layout = create_layout(app, data)
    app.run()

def categorize_data(df: pd.DataFrame) -> pd.DataFrame:
    unique_values = df['Zahlungsempfänger*in'].unique()
    zahlungsempfänger_zuweisung = pd.DataFrame()
    zahlungsempfänger_zuweisung['Zahlungsempfänger*in'] = unique_values
    zahlungsempfänger_zuweisung['categories'] = np.nan
    zahlungsempfänger_zuweisung['consumption_categories'] = np.nan
    zahlungsempfänger_zuweisung['categories'].astype(str)
    zahlungsempfänger_zuweisung['consumption_categories'].astype(str)
    print(unique_values)
    for i in range(len(unique_values)):

        # Iterate through Empfänger
        empfänger = unique_values[i] 
        empfänger = empfänger.lower() 


        #print('Jetzige kategorie :' + str(df['categories'][i]))


        # Category suchbegriffe
        supermarkets = ['penny', 'edeka', 'rewe', 'lidl', 'aldi', 'dm-drogerie', 'tedi', 'dm.drogerie', 'tesco']

        verkehr = ['tankstelle', 'esso', 'shell', 'airport', 'düsseldorf', 'stuttgart', 'parkhausbetriebe']

        wohnen = ['schneider', 'e.on', 'rundfunk','enbw', 'søstrene Grene']

        telekommunikation = ['vodafone', 'simon']

        essen_gehen = ['takumi', 'mala.town', 'fishcotheque', 'nando']

        freizeit = ['fit', 'block']

        inneneinrichtung = ['obi', 'ikea', 'krebs', 'koelle','pflanzen', 'farben', 'bolia', 'imperia', 'bauhaus', 'flora']

        gesundheit = ['apotheke']

        n = 0
        #Supermärkte
        for laden in supermarkets:

            if laden in empfänger:
                n =+1

            else:
                None

            if n > 0:
                zahlungsempfänger_zuweisung.loc[i, 'categories'] = 'Konsum'
                zahlungsempfänger_zuweisung.loc[i, 'consumption_categories'] = 'Nahrungsmittel'
                break
            
        #Verkehr
        n = 0
        for verkehr in verkehr:

            if verkehr in empfänger:
                n =+1

            else:
                None

            if n > 0:
                zahlungsempfänger_zuweisung.loc[i,'categories'] = 'Konsum'
                zahlungsempfänger_zuweisung.loc[i,'consumption_categories'] = 'Verkehr'
                break
            
        #wohnen
        n = 0
        for wohnen in wohnen:

            if wohnen in empfänger:
                n =+1

            else:
                None

            if n > 0:
                zahlungsempfänger_zuweisung.loc[i,'categories'] = 'Konsum'
                zahlungsempfänger_zuweisung.loc[i,'consumption_categories'] = 'Wohnen'
                break
            
        #telekommunikation
        n = 0
        for telekommunikation in telekommunikation:

            if telekommunikation in empfänger:
                n =+1

            else:
                None

            if n > 0:
                zahlungsempfänger_zuweisung.loc[i,'categories'] = 'Konsum'
                zahlungsempfänger_zuweisung.loc[i,'consumption_categories'] = 'Telekommunikation'
                break

        #inneneinrichtung
        n = 0
        for inneneinrichtung in inneneinrichtung:

            if inneneinrichtung in empfänger:
                n =+1

            else:
                None

            if n > 0:
                zahlungsempfänger_zuweisung.loc[i,'categories'] = 'Konsum'
                zahlungsempfänger_zuweisung.loc[i,'consumption_categories'] = 'Inneneinrichtung'
                break

        #gesundheit
        n = 0
        for gesundheit in gesundheit:

            if gesundheit in empfänger:
                n =+1

            else:
                None

            if n > 0:
                zahlungsempfänger_zuweisung.loc[i,'categories'] = 'Konsum'
                zahlungsempfänger_zuweisung.loc[i,'consumption_categories'] = 'Gesundheit'
                break
        
        #essen_gehen
        n = 0
        for essen_gehen in essen_gehen:

            if essen_gehen in empfänger:
                n =+1

            else:
                None

            if n > 0:
                zahlungsempfänger_zuweisung.loc[i,'categories'] = 'Konsum'
                zahlungsempfänger_zuweisung.loc[i,'consumption_categories'] = 'Essen gehen'
                break
        
        #freizeit
        n = 0
        for freizeit in freizeit:

            if freizeit in empfänger:
                n =+1

            else:
                None

            if n > 0:
                zahlungsempfänger_zuweisung.loc[i,'categories'] = 'Konsum'
                zahlungsempfänger_zuweisung.loc[i,'consumption_categories'] = 'Freizeit'
                break

    no_match = zahlungsempfänger_zuweisung[zahlungsempfänger_zuweisung['consumption_categories'].isna()]
    print("------------------------------------")
    print(no_match)            
    print("------------------------------------")

    
    df = df.merge(right=zahlungsempfänger_zuweisung, how= 'left', on = 'Zahlungsempfänger*in')
    schneider = df[df['Zahlungsempfänger*in']=='Hans Schneider']
    print("------------------------------------")
    print(schneider)            
    print("------------------------------------")
    wohnen = df[df['consumption_categories']=='Wohnen']
    print("------------------------------------")
    print(wohnen[['Wertstellung','Zahlungsempfänger*in', 'Betrag (€)']])            
    print("------------------------------------")
    return df

def load_data(file_path) -> pd.DataFrame:
    
    
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

    df_clean = categorize_data(df)

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









#print(zahlungsempfänger_zuweisung)
#
#
## Intialise the categories_df_all dataframe
#categories_df_all = pd.DataFrame()
#
#
#
#categories_df_all.to_csv("categories_df_all.csv", index=False)
#
#
#
#print(len(df))
#unique_values = df['Zahlungsempfänger*in'].unique()
#print(unique_values)
#
#print(df['Zahlungsempfänger*in'].value_counts())
#
#
#print(zahlungsempfänger_zuweisung)
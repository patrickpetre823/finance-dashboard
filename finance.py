import pandas as pd
import numpy as np
import csv
import sys, os
from langchain_community.llms import Ollama
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from components.layout import create_layout
from os.path import dirname, join

#current_dir = dirname(__file__)
#file_path = join(current_dir, "./Umsatzliste_Girokonto")

file_path = 'C:\\Patrick\\VSCode\\Umsatzliste_Girokonto.csv'

def main() -> None:
    data = load_data(file_path)
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
    

    for i in range(len(unique_values)):

        # Iterate through Empfänger
        empfänger = unique_values[i] 

        print('Empfänger der geprüft wird :' + empfänger)
        empfänger = empfänger.lower() 


        #print('Jetzige kategorie :' + str(df['categories'][i]))


        # Category suchbegriffe
        supermarkets = ['penny', 'edeka', 'rewe', 'lidl', 'aldi', 'dm-drogerie', 'tedi', 'dm.drogerie']

        verkehr = ['tankstelle', 'esso', 'shell']

        wohnen = ['schneider', 'e.on', 'rundfunk','enbw']

        telekommunikation = ['vodafone', 'simon']

        freizeit = ['fit', 'block']

        inneneinrichtung = ['obi', 'ikea', 'krebs', 'koelle','pflanzen', 'farben']

        n = 0
        #Supermärkte
        for laden in supermarkets:

            if laden in empfänger:
                n =+1

            else:
                None

            if n > 0:
                print('NAHRUNGSMITTEL DETECTED ' + empfänger)
                zahlungsempfänger_zuweisung['categories'][i] = 'Konsum'
                zahlungsempfänger_zuweisung['consumption_categories'][i] = 'Nahrungsmittel'
                print('Neue kategorie :' + str(zahlungsempfänger_zuweisung['categories'][i]))
                print('Neue konsum kategorie :' + str(zahlungsempfänger_zuweisung['consumption_categories'][i]))
                break
            
        #Verkehr erb
        n = 0
        for verkehr in verkehr:

            if verkehr in empfänger:
                n =+1

            else:
                None

            if n > 0:
                print('Verkehr DETECTED ' + empfänger)
                zahlungsempfänger_zuweisung['categories'][i] = 'Konsum'
                zahlungsempfänger_zuweisung['consumption_categories'][i] = 'Verkehr'
                print('Neue kategorie :' + str(zahlungsempfänger_zuweisung['categories'][i]))
                print('Neue konsum kategorie :' + str(zahlungsempfänger_zuweisung['consumption_categories'][i]))
                break
            
        #wohnen
        n = 0
        for wohnen in wohnen:

            if wohnen in empfänger:
                n =+1

            else:
                None

            if n > 0:
                print('Wohnen DETECTED ' + empfänger)
                zahlungsempfänger_zuweisung['categories'][i] = 'Konsum'
                zahlungsempfänger_zuweisung['consumption_categories'][i] = 'Wohnen'
                print('Neue kategorie :' + str(zahlungsempfänger_zuweisung['categories'][i]))
                print('Neue konsum kategorie :' + str(zahlungsempfänger_zuweisung['consumption_categories'][i]))
                break
            
        #telekommunikation
        n = 0
        for telekommunikation in telekommunikation:

            if telekommunikation in empfänger:
                n =+1

            else:
                None

            if n > 0:
                print('telekommunikation DETECTED ' + empfänger)
                zahlungsempfänger_zuweisung['categories'][i] = 'Konsum'
                zahlungsempfänger_zuweisung['consumption_categories'][i] = 'Telekommunikation'
                print('Neue kategorie :' + str(zahlungsempfänger_zuweisung['categories'][i]))
                print('Neue konsum kategorie :' + str(zahlungsempfänger_zuweisung['consumption_categories'][i]))
                break

        #inneneinrichtung
        n = 0
        for inneneinrichtung in inneneinrichtung:

            if inneneinrichtung in empfänger:
                n =+1

            else:
                None

            if n > 0:
                print('inneneinrichtung DETECTED ' + empfänger)
                zahlungsempfänger_zuweisung['categories'][i] = 'Konsum'
                zahlungsempfänger_zuweisung['consumption_categories'][i] = 'Inneneinrichtung'
                print('Neue kategorie :' + str(zahlungsempfänger_zuweisung['categories'][i]))
                print('Neue konsum kategorie :' + str(zahlungsempfänger_zuweisung['consumption_categories'][i]))
                break


        if n == 0:
            print('Keine Zuordnung ' + empfänger)


        print('-----------------------------------------' )

        print(zahlungsempfänger_zuweisung.head(10))
    
    
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' )

    df = df.merge(right=zahlungsempfänger_zuweisung, how= 'left', on = 'Zahlungsempfänger*in')
    print(df.columns)
    return df

def load_data(file_path) -> pd.DataFrame:
    
    
    col_names = ["Buchungsdatum","Wertstellung","Status","Zahlungspflichtige*r","Zahlungsempfänger*in","Verwendungszweck",
                 "Umsatztyp","IBAN","Betrag (€)","Gläubiger-ID","Mandatsreferenz","Kundenreferenz"]
    
    #
    # df = pd.read_csv('C:\\Patrick\\VSCode\\Umsatzliste_Girokonto.csv', on_bad_lines='warn', names=col_names, delimiter=';')
    df = pd.read_csv(file_path, on_bad_lines='warn', names=col_names, delimiter=';')
    df = df.iloc[1:]
    
    print(df['Buchungsdatum'])
    df['Buchungsdatum'] = pd.to_datetime(df['Buchungsdatum'], dayfirst=True)
    df['jahr'] = df['Buchungsdatum'].dt.year.astype(str)
    df['monat'] = df['Buchungsdatum'].dt.month.astype(str)
    #categories = ['Ersparnis', 'Konsum', 'Sonstige Ausgaben']
    #consumption_categories = ["Ersparnisse", "Wohnen", "Verkehr", 'Nahrungsmittel', 'Freizeit', 'Restaurante', 'Telekommunikation', 'Gesundheit', 'Bekleidung', 'Sonstige', 'Inneneinrichtung/Wohnen']
#
    #df['categories'] = np.nan
    #df['consumption_categories'] = np.nan

    df_clean = categorize_data(df)

    return df_clean


if __name__ == '__main__':
    main()









print(zahlungsempfänger_zuweisung)


# Intialise the categories_df_all dataframe
categories_df_all = pd.DataFrame()



categories_df_all.to_csv("categories_df_all.csv", index=False)



print(len(df))
unique_values = df['Zahlungsempfänger*in'].unique()
print(unique_values)

print(df['Zahlungsempfänger*in'].value_counts())


print(zahlungsempfänger_zuweisung)
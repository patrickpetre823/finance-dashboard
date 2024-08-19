import pandas as pd
import numpy as np


def categorize_transfer(df: pd.DataFrame) -> pd.DataFrame:
    
    unique_values = df['Zahlungsempfänger*in'].unique()
    zahlungsempfänger_zuweisung = pd.DataFrame()
    zahlungsempfänger_zuweisung['Zahlungsempfänger*in'] = unique_values
    zahlungsempfänger_zuweisung['categories'] = np.nan
    zahlungsempfänger_zuweisung['consumption_categories'] = np.nan
    zahlungsempfänger_zuweisung['categories'].astype(str)
    zahlungsempfänger_zuweisung['consumption_categories'].astype(str)

    for i in range(len(unique_values)):

        # Iterate through Empfänger
        empfänger = unique_values[i] 
        empfänger = empfänger.lower() 


        #print('Jetzige kategorie :' + str(df['categories'][i]))


        # Category suchbegriffe
        supermarkets = ['penny', 'edeka', 'rewe', 'lidl', 'aldi', 'dm-drogerie', 'tedi', 'dm.drogerie', 'tesco']

        verkehr = ['tankstelle', 'esso', 'shell', 'airport', 'düsseldorf', 'stuttgart', 'parkhausbetriebe']

        wohnen = ['schneider', 'e.on', 'rundfunk','enbw' ]

        telekommunikation = ['vodafone', 'simon']

        essen_gehen = ['takumi', 'mala.town', 'fishcotheque', 'nando']

        freizeit = ['fit', 'block']

        inneneinrichtung = ['obi', 'ikea', 'krebs', 'koelle','pflanzen', 'farben', 'bolia', 'imperia', 'bauhaus', 'flora', 'søstrene Grene']

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
    print("-----------------ALLES WOHNEN-------------------")
    print(wohnen[['Wertstellung','Zahlungsempfänger*in', 'Betrag (€)']])            
    print("------------------------------------")
    return df
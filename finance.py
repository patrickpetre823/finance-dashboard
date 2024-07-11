import pandas as pd
import numpy as np
import csv
import sys, os
from langchain_community.llms import Ollama

# LLM Model
llm = Ollama(model="finance_llm_llama2")


from os.path import dirname, join
current_dir = dirname(__file__)
file_path = join(current_dir, "./Umsatzliste_Girokonto")

print(file_path)
#with open(file_path, 'r') as f:

col_names = ["Buchungsdatum","Wertstellung","Status","Zahlungspflichtige*r","Zahlungsempfänger*in","Verwendungszweck",
             "Umsatztyp","IBAN","Betrag (€)","Gläubiger-ID","Mandatsreferenz","Kundenreferenz"]

df = pd.read_csv('C:\\Patrick\\VSCode\\Umsatzliste_Girokonto.csv', on_bad_lines='warn', names=col_names, delimiter=';')

#print(df.columns)

# Monat

#print(df['Zahlungsempfänger*in'])


# Kategorien

categories = ['Ersparnis', 'Konsum', 'Sonstige Ausgaben']
consumption_categories = ["Ersparnisse", "Wohnen", "Verkehr", 'Nahrungsmittel', 'Freizeit', 'Restaurante', 'Telekommunikation', 'Gesundheit', 'Bekleidung', 'Sonstige', 'Inneneinrichtung/Wohnen']

df['categories'] = np.nan
df['consumption_categories'] = np.nan


zahlungsempfänger_zuweisung = pd.DataFrame()
unique_values = df['Zahlungsempfänger*in'].unique()

zahlungsempfänger_zuweisung['unique_empfänger'] = unique_values
print(type(unique_values))
zahlungsempfänger_zuweisung['categories'] = np.nan
zahlungsempfänger_zuweisung['consumption_categories'] = np.nan

#print(f'Unique ZAHLUNGSAEMPÖGER IN THIS {unique_values}')


# Get index list
#https://stackoverflow.com/questions/47518609/for-loop-range-and-interval-how-to-include-last-step
#def hop(start, stop, step):
#    for i in range(start, stop, step):
#        yield i
#    yield stop
#
#index_list = list(hop(0, len(unique_values), 30))
#index_list
#
#print(f'THIS IS INDEX KLLIS {index_list}')


# Categorize Function
def categorize_transaction(transaction_names, llm):
    response = llm.invoke('Füge bitte hinter jedem Zahlungsempfänger eine passende Kategorie hinzuh. Z.B.: penny - Lebensmittel, malatown - restaurant, tankstelle - Verkehr etc.. Als Kategorien, benutze ausschließlich die folgenden Begriffe: Ersparnisse, Wohnen, Verkehr, Lebensmittel, Freizeit, Restaurante, Telekommunikation, Gesundheit, Bekleidung, Sonstige, Inneneinrichtung/Wohnen. Es sind keine anderen Kategorien zulässig' + transaction_names)
    print("-----------------")
    print("RESPONSE!!!! :")
    print(response)
    print("-----------------")
    response = response.split('\n')  

    categories_df = pd.DataFrame({'Transaction vs category': response})
    categories_df[['Transaction', 'Category']] = categories_df['Transaction vs category'].str.split(' - ', expand=True)

    print("Size of DATAFRAMER :")
    print(categories_df.shape)
    return categories_df

#categories_df = categorize_transaction(unique_values, llm)



# Intialise the categories_df_all dataframe
categories_df_all = pd.DataFrame()

# Loop through the index_list
#for i in range(0, len(index_list)-1):
#    
#    transaction_names = unique_values[index_list[i]:index_list[i+1]]
#    transaction_names = ';'.join(transaction_names)
#    print(f'TRANSACTIONNAEEEMMMES {transaction_names}')
#    categories_df = categorize_transaction(transaction_names.lower(), llm)
#    categories_df_all = pd.concat([categories_df_all, categories_df], ignore_index=True)
#    categories_df_all = pd.concat([categories_df_all, categories_df], ignore_index=True)

#print(categories_df_all)
print(categories_df_all)

#print(f'CATEGORIES DF ALL SIZE  {categories_df.shape}')

categories_df_all.to_csv("categories_df_all.csv", index=False)

for i in range(len(unique_values)):
    
    # Iterate through Empfänger
    empfänger = unique_values[i] 

    print('Empfänger der geprüft wird :' + empfänger)
    print('Jetzige kategorie :' + str(df['categories'][i]))


    # Category suchbegriffe
    supermarkets = ['Penny', 'Edeka', 'REWE', 'Lidl', 'Aldi', 'DM-Drogerie']
    
    verkehr = ['TANKSTELLE', 'Tankstelle', 'Esso']

    wohnen = ['Schneider', 'E.ON', 'Rundfunk']

    telekommunikation = ['Vodafone', 'Simon']

    freizeit = ['fit', 'Block']

    inneneinrichtung = ['OBI', 'IKEA', 'KREBS', 'KOELLE']

    n = 0
    #Supermärkte
    for laden in supermarkets:
        
        if laden in empfänger:
            n =+1
            
        else:
            None
        
        if n > 0:
            print('NAHRUNGSMITTEL DETECTED ' + empfänger)
            df['categories'][i] = 'Konsum'
            df['consumption_categories'][i] = 'Nahrungsmittel'
            print('Neue kategorie :' + str(df['categories'][i]))
            print('Neue konsum kategorie :' + str(df['consumption_categories'][i]))
            break
    
    #Verkehr
    n = 0
    for verkehr in verkehr:
        
        if verkehr in empfänger:
            n =+1
            
        else:
            None
        
        if n > 0:
            print('Verkehr DETECTED ' + empfänger)
            df['categories'][i] = 'Konsum'
            df['consumption_categories'][i] = 'Verkehr'
            print('Neue kategorie :' + str(df['categories'][i]))
            print('Neue konsum kategorie :' + str(df['consumption_categories'][i]))
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
            df['categories'][i] = 'Konsum'
            df['consumption_categories'][i] = 'Wohnen'
            print('Neue kategorie :' + str(df['categories'][i]))
            print('Neue konsum kategorie :' + str(df['consumption_categories'][i]))
            break
    
    #telekommunikation
    for telekommunikation in telekommunikation:
        
        if telekommunikation in empfänger:
            n =+1
            
        else:
            None
        
        if n > 0:
            print('telekommunikation DETECTED ' + empfänger)
            df['categories'][i] = 'Konsum'
            df['consumption_categories'][i] = 'Telekommunikation'
            print('Neue kategorie :' + str(df['categories'][i]))
            print('Neue konsum kategorie :' + str(df['consumption_categories'][i]))
            break

    #inneneinrichtung
    for inneneinrichtung in inneneinrichtung:
        
        if inneneinrichtung in empfänger:
            n =+1
            
        else:
            None
        
        if n > 0:
            print('inneneinrichtung DETECTED ' + empfänger)
            df['categories'][i] = 'Konsum'
            df['consumption_categories'][i] = 'Inneneinrichtung'
            print('Neue kategorie :' + str(df['categories'][i]))
            print('Neue konsum kategorie :' + str(df['consumption_categories'][i]))
            break


    if n == 0:
        print('Keine Zuordnung ' + empfänger)

    
    print('-----------------------------------------' )


print(len(df))
unique_values = df['Zahlungsempfänger*in'].unique()
print(unique_values)

print(df['Zahlungsempfänger*in'].value_counts())
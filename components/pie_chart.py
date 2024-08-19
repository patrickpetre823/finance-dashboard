from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from . import ids
import plotly.graph_objects as go
from math import *
import plotly.io as pio


def render(app: Dash, data: pd.DataFrame) -> html.Div:

    # When calculating the Avg. we should not take the ongoing month into calc, so it does not skew the data
    all_months = data["monat"].unique()
    last_month = all_months[0]
  
    idx_month = data.columns.get_loc("monat")

    n = 0

    #Iterating through dataframe to find the number of entries in current month
    for idx, row in data.iterrows():

        if data.iloc[idx, idx_month] == last_month:
            n += 1
        else:
            break
    
    # Dropping those rows from the DF
    data = data.iloc[n:]
 

    # Grouping and avg by month and category
    df_mean = (data.groupby(['monat', 'consumption_categories'], as_index=False)['Betrag (€)'].sum().groupby('consumption_categories')['Betrag (€)'].mean())

    # Creating values and labels for Diagram
    df_mean = df_mean.to_dict()
    
    values = list(df_mean.values())
    values = list(map(float, values))
    values = [fabs(value) for value in values ]

    
    labels = list(df_mean.keys())

    for i, label in enumerate(labels):
        labels[i] = labels[i] + ' : ' + str(round(values[i],)) + ' €'
    

    sum_avg = round(sum(values), 0)
    sum_avg = '{:,}'.format(sum_avg)

    
    fig = go.Figure(data=[go.Pie(labels=labels, 
                                 values=values, 
                                 hole=.2,
                                 )])
    

    fig.update_layout(title=dict(text=f"Total Money spent per Month: {sum_avg} €", 
                                 xanchor='center',
                                 yanchor= 'top',
                                 y=0.9,
                                 x=0.5
                                )
    )


    fig.update_layout(font=dict(family='Arial', size=16),
                   legend=dict(x=1, y=0.5, ),
                   width=1000,
                   height=1000,
                   margin=dict(t=50, b=0, l=250, r=0),
                   legend_title_text='Categories:',
                   
                )

    
    pie_chart = html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART,)


    return html.Div(children=[pie_chart],)
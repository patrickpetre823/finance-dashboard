from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from . import ids
import plotly.graph_objects as go
from math import *
import plotly.io as pio


def render(app: Dash, data: pd.DataFrame) -> html.Div:


    df_mean = (data.groupby(['monat', 'consumption_categories'], as_index=False)['Betrag (€)'].sum().groupby('consumption_categories')['Betrag (€)'].mean())

    print(df_mean)
    print(type(df_mean))
    print(df_mean.shape)

    df_mean = df_mean.to_dict()

    print(df_mean)
    print(type(df_mean))
    #df_mean = df_mean.groupby('consumption_categories')['Betrag (€)'].mean()
    #print(df_mean)

    labels = list(df_mean.keys())
    
    values = list(df_mean.values())
    values = list(map(float, values))
    values = [fabs(value) for value in values ]

    sum_avg = round(sum(values), 0)
    sum_avg = '{:,}'.format(sum_avg)

    #fig = px.pie(values=values, names=labels)
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    

    fig.update_layout(title=dict(text=f"Total Money spent per Month: {sum_avg} €", 
                                 xanchor='center',
                                 yanchor= 'top',
                                 y=0.9,
                                )
    )

                      

    fig.update_layout(font=dict(family='Arial', size=16, color='#909090'),
                   legend=dict(x=1, y=0.5),
                   width=1000,
                   height=1000,
                   margin=dict(t=50, b=0, l=50, r=0),
                   template='ggplot2',
                   legend_title_text='Categories:'
                    )

    
    pie_chart = html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART,)


    return html.Div(children=[pie_chart],)
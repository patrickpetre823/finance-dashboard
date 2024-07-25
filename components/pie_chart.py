from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from . import ids
import plotly.graph_objects as go
from math import *

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
    

    fig.update_layout(title=f"Total Money per Month: {sum_avg} €",
                  font=dict(family='Arial', size=12, color='#909090'),
                   legend=dict(x=2, y=0.5)
                    )

    
    pie_chart = html.Div(dcc.Graph(figure=fig, style={'width': '90vh', 'height': '90vh'}), id=ids.PIE_CHART,)


    return html.Div(children=[html.H6('Average Money Spent Per Month'), pie_chart],)
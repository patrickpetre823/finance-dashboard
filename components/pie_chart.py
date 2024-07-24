from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from . import ids
import plotly.graph_objects as go

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

    print("---------------------------------------")
    print(values)
    print(labels)
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    
    layout = go.Layout(
                   title="Percentage of events",
                   font=dict(family='Arial', size=12, color='#909090'),
                   legend=dict(x=0.9, y=0.5)
                    )

    fig.show()
    
    pie_chart = html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART)


    return html.Div(children=[html.H6('Average Money Spent Per Month'), pie_chart],)
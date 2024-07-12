from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    
    fig = px.bar(data, x=data["monat"], y=data['Betrag (€)'], color='consumption_categories')

    return html.Div(dcc.Graph(figure=fig), id= ids.BAR_CHART)
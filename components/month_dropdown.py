from dash import Dash, html, dcc
from. import ids
import pandas as pd
from dash.dependencies import Input, Output

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    
    all_months = data['monat'].unique()
     
    return html.Div(
        children=[
            html.H6("Months"),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=[{"label": month, "value": month} for month in all_months],
                value=all_months,
                multi=True,
            ),
        ],
    ),
from dash import Dash, html, dcc
from. import ids
import pandas as pd
from dash.dependencies import Input, Output

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_years = data['jahr'].unique()
     
    return html.Div(
        children=[
            html.H6("Year"),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=[{"label": year, "value": year} for year in all_years],
                value=all_years,
                multi=True,
            ),
        ],
    ),
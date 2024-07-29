from dash import Dash, html
import pandas as pd
from components import year_dropdown, month_dropdown
from components import bar_chart
from components import pie_chart


def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.H3('Average Money Spent Per Month'),
            pie_chart.render(app, data),
            html.Hr(),
            html.Div(className='dropdown-container',children=year_dropdown.render(app, data)),
            html.Div(className='dropdown2-container',children=month_dropdown.render(app, data)),
            #html.Div(className='bar-chart',children=bar_chart.render(app, data))
            bar_chart.render(app, data),
            
        ]
    )
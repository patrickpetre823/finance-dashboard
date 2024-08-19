from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from . import ids
import plotly.graph_objects as go


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        Input(ids.MONTH_DROPDOWN, "value")
    )
    def update_bar_chart(months_selected: list) -> html.Div:
    

        filtered_data = data[data["monat"].isin(months_selected)]

        if data.shape[0] == 0:
            return html.Div("No Data selected")
                   
        color_map={
                "Wohnen": "#636efa",
                "Nahrungsmittel": "#ef553b",
                "Telekommunikation": "#ff6692",
                "Verkehr": "#00cc96",
                "Essen gehen": "#ab63fa",
                "Inneneinrichtung": "#ffa15a",
                "Gesundheit": "#19d3f3",
                "Freizeit":  "#b6e880",
                }


        fig = px.histogram(
              filtered_data,
              x=filtered_data['monat'],
              y=filtered_data['Betrag (€)'],
              color=filtered_data["consumption_categories"],
              labels={'sum of y':'Money Spent',
                      'x' : 'Monat'},
              text_auto=True,
              range_y = [0, -2500],
              color_discrete_map=color_map
        )

        fig.update_xaxes(categoryorder='array', categoryarray= ['January', 'February', 'March', 'April', 'May', 'June','July','August','September','October','November', 'December' ])

        fig.update_layout(font=dict(family='Arial', size=16, color='#909090'),
                          template='seaborn')
    
       
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:

    #@app.callback(
    #    Output(ids.BAR_CHART, "children"),
    #    Input(ids.YEAR_DROPDOWN, "value")
    #)
    def update_bar_chart(data: pd.DataFrame) -> html.Div:
        #filtered_data = data.query("jahr == 2024")
        #print(filtered_data)
        if data.shape[0] == 0:
            return html.Div("No Data selected")
        
        def create_pivot_table(data: pd.DataFrame) -> pd.DataFrame:
            #print(data.columns)
            pt = data.pivot_table(
                  values="Betrag (€)",
                  index="consumption_categories",
                  aggfunc="sum",
                  fill_value=0
            )
            return pt.reset_index().sort_values("Betrag (€)", ascending=False)
        
        fig = px.bar(
              create_pivot_table(data),
              x=data['monat'],
              y=data['Betrag (€)'],
              color=data["consumption_categories"]
        )
        fig.show()
        #create_pivot_table(data)
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)
    # 
    # 
    # fig = px.bar(data, x=data["monat"], y=data['Betrag (€)'], color='consumption_categories')
    bar_chart = update_bar_chart(data)
    #return html.Div(id= ids.BAR_CHART)
    return html.Div(children=[html.H6("Monthly costs"), bar_chart],)
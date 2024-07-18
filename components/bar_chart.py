from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    print("1111111111111111111111111111")
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        Input(ids.YEAR_DROPDOWN, "value")
    )
    def update_bar_chart(years: list[str]) -> html.Div:
        print("2222222222222222222222222222")
        filtered_data = data.query("year in @years")
        if filtered_data.shape[0] == 0:
            return html.Div("No Data selected")
        
        def create_privot_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(
                  values=data["Betrag (€)"],
                  index=data['consumption_categories'],
                  aggfunc="sum",
                  fill_value=0
            )
            print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
            print(data["Betrag (€)"])
            return pt.reset_index().sort_values("Betrag (€)", ascending=False)
        
        fig = px.bar(
              create_pivot_table(),
              x=data['consumptions_categories'],
              y=data['Betrag (€)'],
              color=data["consumption_categories"]
        )
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)
    # 
    # 
    # fig = px.bar(data, x=data["monat"], y=data['Betrag (€)'], color='consumption_categories')

    return html.Div(id= ids.BAR_CHART)
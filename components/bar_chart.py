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
    def update_bar_chart(data: pd.DataFrame) -> html.Div:

        if data.shape[0] == 0:
            return html.Div("No Data selected")

        def create_pivot_table(data: pd.DataFrame) -> pd.DataFrame:
            #print(data.columns)
            pt = data.pivot_table(
                  values="Betrag (€)",
                  index="consumption_categories",
                  aggfunc="sum",
                  fill_value=0,
                  margins=True,
            )
            print(pt)
            return pt.reset_index()
            #return pt.reset_index().sort_values("Betrag (€)", ascending=False)
        
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
              data,
              x=data['monat'],
              y=data['Betrag (€)'],
              color=data["consumption_categories"],
              labels={'sum of y':'Money Spent',
                      'x' : 'Monat'},
              text_auto=True,
              range_y = [0, -3000],
              color_discrete_map=color_map
        )

        fig.update_xaxes(categoryorder='array', categoryarray= ['January', 'February', 'March', 'April', 'May', 'June','July','August','September','October','November', 'December' ])

        fig.update_layout(font=dict(family='Arial', size=16, color='#909090'),
                          template='seaborn')


        dfs = data.groupby('monat')['Betrag (€)'].sum()
        print(dfs)
        print(type(dfs))
        print(dfs[1])
        
        
        
        # Add annotation

        #fig.add_trace(go.Scatter(
        #    x=data['monat'], 
        #    y=dfs[:],
        #    text=dfs[:],
        #    mode='text',
        #    textposition='top center',
        #    textfont=dict(
        #        size=18,
        #    ),
        #    showlegend=False
        #))

        
        
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)
    # 
    # 
    # fig = px.bar(data, x=data["monat"], y=data['Betrag (€)'], color='consumption_categories')
    bar_chart = update_bar_chart(data)
    #return html.Div(id= ids.BAR_CHART)
    return html.Div(children=[html.H6("Monthly costs"), bar_chart],)
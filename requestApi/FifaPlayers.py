from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbs
# import File
Players = pd.read_csv("C:\\Users\\cochiagha\Documents\\Dash\\fifa_soccer_players.csv")

playerNames = Players["long_name"].values
average_age = Players["age"].mean()
average_height = Players["height_cm"].mean()
average_weight = Players["weight_kg"].mean()
# Define Components

#---- Navigation bar
navbar = dbs.NavbarSimple(
    brand= "Fifa Players",
    children=[
        dbs.Row(
            children=[
                dbs.Col(children= [
                    
                    html.P(children = [
                            "Source: ",                                 # Souce label
                            html.A( children="Sofifa",                   # Reference Link
                            href="http://sofifa.com",
                            target= "_blank",
                            style={"color":"black"})
                        ],
                        style={"color":"black"}
                    )
                ]
                
                )
            ]
        )
    ],
    color="primary",
    fluid=True
)


# Card grid for displaying player information

card = html.Div([
    dbs.Row( children = [
            html.H1(children="Player Features", style={"textAlign":"center"}),
            dbs.Col(children=[
                dbs.Card(children=[
                        html.H4(children="Average Age"),
                        html.H5(children=f"The average age is {average_age}")                
                ],
                    body =True,
                    style = {"textAlign":"center","color":"white"},
                    color="lightblue"
                )
                ]),
            dbs.Col(children=[
                dbs.Card(children=[
                        html.H4(children="Average Height"),
                        html.H5(children=f"The average height is {average_height}")                
                ],
                    body = True,
                    style = {"textAlign":"center","color":"white"},
                    color="lightblue"
                )
                ]),
            dbs.Col(children=[
                dbs.Card(children=[
                        html.H4(children="Average Weight"),
                        html.H5(children=f"The average weight is {average_weight}")                
                ],
                    body = True,
                    style = {"textAlign":"center","color":"white"},
                    color="lightblue"
                )
                ])
        ],
    
    )
]
)


lineBreak = html.Br()
dropDownLabel = html.Label(children="Player Names:")
playerNameDrpDwn = dcc.Dropdown(options = playerNames, value=playerNames[0] )    # Default value




app = Dash(external_stylesheets=[dbs.themes.CYBORG])


app.layout = html.Div([
    navbar,
    card
]
     
)

if __name__ == "__main__":
    app.run_server(debug = True)
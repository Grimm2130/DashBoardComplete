from dash import Dash, html, Input, Output, State, dcc
import pandas as pd
import plotly as Plotly
import plotly.express as px
import plotly.graph_objects as go

pd.options.plotting.backend = "plotly"
# Set up the data
avocadoes = pd.read_csv("C:\\Users\\cochiagha\\Documents\\Dash\\avocado.csv")

# up the default variabls for the Dashboard
regions = avocadoes['geography'].unique()
selectedRegion = regions[0]
filteredData = avocadoes[ (avocadoes["geography"]==selectedRegion)]

# Graph definition
lineGraph = px.line(filteredData, x = "date", y = "average_price", color="type", title = f"Average avocado prices for {selectedRegion}")

# Page Layout
title = html.H1(children="Avocado Prices")
dropDownTitle = html.H3(children="State Regions")
regionDropdown = dcc.Dropdown(options=regions, value=selectedRegion)
Avocado_Average_Price_Graph = dcc.Graph()

app = Dash()
# Define the HTML components
app.layout = html.Div(children=[
    title,
    dropDownTitle,
    regionDropdown,
    Avocado_Average_Price_Graph
])

@app.callback(
    Output(component_id = Avocado_Average_Price_Graph, component_property= "figure"),
    Input(component_id=regionDropdown, component_property="value")
)
def changeRegion(selected_region):
    filteredData = avocadoes[ (avocadoes["geography"]==selected_region)]
    lineGraph = px.line(filteredData, x = "date", y = "average_price", color="type", title = f"Average avocado prices for {selected_region}")
    return lineGraph


if (__name__ == "__main__"):
    app.run_server()
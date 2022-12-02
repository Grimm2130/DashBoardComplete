from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import urllib.request as url
import pandas as pd
import ssl
import json
from pprint import pprint
import numpy as np

#---------------------- Get the data from the API -------------------------------------
myUrl = "https://localhost:7072/api/Wine"
context = ssl._create_unverified_context()
myRequest = url.urlopen(myUrl, context=context)

print("MY request code: " + str(myRequest.getcode()))

data = myRequest.read()
data= json.loads(data)
wines = pd.DataFrame(data)
# for i in wines.columns:
#     print(i)

# ------------------ Add layout components ---------------------


# Header Container and Text
Header = html.Div(children = [                          
    html.H1(children="My Dash Board"),  
    ],
    style={"textAlign":"center", "fontSize":50}
)

#Text entry for user file
UserInput = html.Div([dcc.Input(placeholder="Search for ticker on yahoo Finance",
    style={"width": "50%"})
    ]
)

# button For validating inputs and outputting the database
submitButton = html.Button(children="Submit")

# ---- Tab 1 Definition ---------


# -- Define cascading inputs for data entry
inputSegment = html.Div(
    children = [
        dbc.Row(
            children = [
                
            ]
        )
    ]
)

# ----- Define the format for the Pie chart for the item's distribution

# Group the columns bay the data names
winesNames = wines.groupby("name").count()
# Select for the first coulmn of the graph
winesNames = winesNames[winesNames.columns[:1]]
# Plot the pie graph
winePieChart = dcc.Graph(
    figure= go.Figure( data=[
        go.Pie(
            # data, 
            values= list(winesNames[winesNames.columns[0]].values) , # List of values in the first column
            labels=list(winesNames.index))                              # List of names index coulmn
        ]
    )
)

# --- Define the format for the datatable ------

dataTable = dash_table.DataTable(data = data[-10:-1])

Tab1 = dcc.Tab(
    label="Data Table",
    children= [
        winePieChart,
        dataTable
        ]
)

# ---- Graph Tab Definition ---------

wineCols = wines.columns[2:]
# Selected item in col
selection = np.array(wines[wineCols[0]])
# list of Colums from data table
ColumnSelectionBar = dcc.Dropdown(
    options=wineCols, value=[wineCols[0]]
)
# Figure to plot
figure= dcc.Graph(
        figure=go.Figure(data = [
            go.Histogram(x=selection)
        ]
    )
)  
# ---------- Tab declaration including contents ------------
GraphTab = dcc.Tab(
    label = " ".join(wines[wineCols[0]].name.split("_")).capitalize()+".",
    children=[
        ColumnSelectionBar,
        figure
    ]
)

# --------------- Tab collection ------------
pageLayout = dcc.Tabs(
    children=[
        Tab1,
        GraphTab
    ]
)

#--------------- Call the Dash Api -------------------------
app = Dash(external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div(
    children=[
        Header, 
        # UserInput,
        # submitButton,
        pageLayout
    ]
)

# Call back to enable the graph to be changeable
@app.callback(
    Output(component_id=figure, component_property="figure"),
    Output(component_id=GraphTab, component_property="label"),
    Input(component_id=ColumnSelectionBar, component_property="value")
)
def changeGraphItem(newCol):
    labelName = " ".join(wines[newCol].name.split("_")).capitalize()+"."
    selection = np.array(wines[newCol])
    figure=go.Figure(data = [
            go.Histogram(x=selection)
        ]
    )
    return figure, labelName


if __name__ == "__main__":
    app.run_server(debug = True)
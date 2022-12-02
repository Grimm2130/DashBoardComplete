from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
from Models.DocReader import DocReader

# read in the files
dataFile = "C:\\Users\\cochiagha\\Documents\\Dash\\world_happiness.csv"
readerObject = DocReader(dataFile)
worldData =  readerObject.getData()          # return dataFrame object
regions = worldData['region'].unique()
features = list(worldData.select_dtypes(include ='float64 int32 int64'.split()).columns)            # Y axis OPtions
countries = readerObject.getItems('country')

# Call Dash object
app = Dash()

# ------ Graph definitions Default --------
selectedFeature = "happiness_score"
selectedCountry = "United States"
lineFig = px.line(worldData[worldData['country'] == selectedCountry], x = 'year', y = selectedFeature, title = f"happiness Score in The {selectedCountry}")



# ------ Http Elements -------
header_1 = html.H1(children="World Happiness Dashboard")
aLineBreak = html.Br()
firstParagraph = html.P(children = "This dashboard...")
firstLink = html.A("World happiness Report Data Source", # Second Paragraph
                href="http://worldhappiness.report", # Refernce
                target="_blank")

# ------ Http Components -------
featureRadioItems = dcc.RadioItems(options= features,value=selectedFeature)             # Radio components of the features
regionRadioItems = dcc.RadioItems(options= regions, value='North America')                  # Radio components
countryDropDown = dcc.Dropdown(options= countries, value='United States' )                   # Radio components
submitButton = html.Button(children="Submit")
graph1 = dcc.Graph()

#------------- Description --------------------------
selectedMean = worldData[worldData['country'] == selectedCountry][selectedFeature].mean()
graphDescription = html.P( children = f"The average {' '.join(selectedFeature.split('_')).capitalize()} for {selectedCountry} is {selectedMean}")

# Call a layout
app.layout = html.Div(
    children = [
        header_1,
        aLineBreak,      # New Line
        firstParagraph,     # First pargraph
        firstLink,                     # Trigger opening a new Page
        aLineBreak,
        regionRadioItems,
        aLineBreak,
        featureRadioItems,                   # Radio components
        aLineBreak,
        submitButton,               # submit button here
        aLineBreak,
        countryDropDown,
        graph1,
        aLineBreak,
        graphDescription
    ]
)

# Change the countries in the drop down based on the input from 
@app.callback(
    Output(component_id=countryDropDown, component_property= 'options'),
    Output(component_id=countryDropDown, component_property= 'value'),
    Input(component_id=regionRadioItems, component_property='value')
)
def modifyDropDown(selected_region):
    ''' Change the Listed countries based on the regions selected'''
    # Filter for regions
    filteredRegions = worldData[worldData['region'] == selected_region]["country"].unique()
    filteredCountry = filteredRegions[0]
    return filteredRegions, filteredCountry

# Change the display of the Graph and description text based on the selected drop down item
@app.callback(
    Output(component_id = graph1, component_property = "figure"),
    Output(component_id=graphDescription, component_property="children"),
    Input(component_id= submitButton, component_property="n_clicks" ),
    State(component_id=countryDropDown, component_property="value"),
    State(component_id=featureRadioItems, component_property="value"),
)
def changeDisplayItem(buttonClicked, selected_country, selected_feature):
    selectedCountry = selected_country
    # Select the country to be used for the plot
    newFilter = worldData[worldData['country'] == selectedCountry]
    # Define new Plot for the selected country, Specify the feature to plot
    lineFig = px.line(newFilter,  x = 'year', y = selected_feature, title = f"happiness Score in The {selectedCountry}")
    # Define a new graph description
    selectedMean = worldData[worldData['country'] == selected_country][selected_feature].mean()
    graphDescription = html.P( children = f"The average {' '.join(selected_feature.split('_')).capitalize()} for {selected_country} is {selectedMean}")
    return lineFig, graphDescription

if __name__ == "__main__":
    app.run_server(debug = True)
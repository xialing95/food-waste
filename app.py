import dash
import math
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
raw_waste = pd.read_csv('data/food_waste_GHG.csv')
waste_comp = pd.read_csv('data/waste_composition.csv')
GHG_comp = pd.read_csv('data/waste_composition.csv')
waste_comp_available_date = waste_comp['Date'].unique()

fig = px.bar(raw_waste, x='date', y=['2015_GHG_est', '2020_GHG_est'])
# Change the bar mode
fig.update_layout(barmode='group')

app.layout = html.Div(
    [
    html.H1(['Analysis of Food Waste at MIT'], style={'text-align':'center'}),

    # Introduction
    dbc.Row(
        dbc.Col(
            html.H4("Our goal is to halve the food waste emitted GHG at MIT."), 
            style={'text-align':'center', 'marginBottom': 70})),
    
    # raw data and estimated percentage waste to tons/month
    dbc.Row(
        dbc.Col([
            # Description 
            html.Div(["First let's get an idea of how much food waste we are generating at MIT dining. \
                MIT Office of Sustainability provided the measured weight of food waste collected at MIT \
                service for the from 2009-2019. Let's compare the measured data to estimated food waste \
                generated for all dining enrolled student every month based on the percentage amount wasted."], 
                style={'text-align':'center', 'marginBottom':70}),

            # Total Figure
            dcc.Graph(id ='wasteFig'),
            dcc.Slider(
                id='wastedSlider',
                min = 0,
                max = 50,
                value = 20,
                step = 1,
                marks={
                    0: '0% Wasted',
                    50: '50% Wasted'})
            ], width = 8), 
        justify="center"),

    # BIG TEXT Description on energy and mass
    dbc.Row(
        dbc.Col(
            html.H4(id='wastedValLabel'), style={'text-align':'center', 'marginBottom': 100, 'marginTop': 50},
            width = 6), 
            justify="center"),

    # Descritpion of mass and GHG breakdown
    dbc.Row(
        dbc.Col(
            html.Div(["From research done in urban areas, we can estimate the compostion of the food waste\
                generated in MIT dining. From that, let's simplifiy the model and select represented food for\
                for each food group, therefore we can estimate the GHG emission."], 
            style={'text-align':'center', 'marginBottom': 50}), 
            width = 8),
        justify="center"),

    # plots of mass and GHG emission composition calculation 
    dbc.Row(
        [
            dbc.Col([ 
                dcc.Dropdown(
                    id = 'wasteCompDate',
                    options = [{'label': i, 'value': i} for i in waste_comp_available_date],
                    value = '2015-10'),
                dcc.Graph(id = 'wasteComp')]), 

            dbc.Col([
                dcc.Dropdown(
                    id = 'GHGCompDate',
                    options = [{'label': i, 'value': i} for i in waste_comp_available_date],
                    value = ''),
                dcc.Graph(id = 'GHGCompFig')])
        ],
        justify="around"),

    # Descritpion of GHG model comparison 
    dbc.Row(
        dbc.Col(
            html.Div(["There are different ways to reduce food waste GHG emission by half. \
                The model is calculated with an esimated 200 tons of food waste per year. \
                The base model assumes all 200 tons of food waste is going to the landfill. \
                Production emission is the GHG emission from the production of food waste shown above. \
                Compost offset is the amount of GHG offset by composting based on the selected percentage of food waste.\
                Anaerobic offset is the amount of GHG offset by dry anaerobic digestion based on the selected percentage of food waste. \
                The rest percentage of food waste goes to the landfilled."], 
            style={'text-align':'center', 'marginBottom': 0}), 
            width = 8),
        justify="center"),

    # plot of GHG total 
        dbc.Row(
        dbc.Col([
            
            # Total Figure
            dcc.Graph(id ='GHGCompareFig1'),

            # html.Label('Total Waste'),
            # dcc.Slider(
            #     id='totalWaste1',
            #     min = 100,
            #     max = 200,
            #     value = 20,
            #     step = 1,
            #     marks={
            #         100: '100 tons',
            #         150: '150 tons',
            #         200: '200 tons'}), 

            html.Label('Food Reduction', id='FoodRedLabel'),        
            dcc.Slider(
                id='productionReduce1',
                min = 0,
                max = 90,
                value = 20,
                step = 1,
                marks={
                    0: '0%',
                    25: '25%',
                    50: '50%', 
                    75: '75%',
                    90: '90%'}),

            html.Label('Percentage Compost', id = 'CompostLabel'),                         
            dcc.Slider(
                id='compostSlider1',
                min = 0,
                max = 100,
                value = 0,
                step = 1,
                marks={
                    0: '0%',
                    100: '100%'}), 
            
            html.Label('Percentage Anaerobic', id = 'AnaerobicLabel'),                        
            dcc.Slider(
                id='Anaerobic1',
                min = 0,
                max = 100,
                value = 0,
                step = 1,
                marks={
                    0: '0%',
                    100: '100%'}), 
            ], width = 8), 
        justify="center"),

        # Description 
        dbc.Row(
        dbc.Col(
            html.H4(id='GHGCompareText1'), style={'text-align':'center', 'marginBottom': 100, 'marginTop': 50},
            width = 6), 
            justify="center")

], style={'marginBottom': 100, 'marginTop': 70})

# calculate the tons wasted on campus
def wasteCal(value):
    #weight in Ib
    studentEnroll = 1708.0
    mealPerStudent = 1.2
    mealPerWeek = 14
    weekPerMonth= 4

    wasteAllStudent = studentEnroll*mealPerStudent*(value/100)
    wastePerMonth = (wasteAllStudent*mealPerWeek*weekPerMonth)/2000

    calPerStudent= 2000
    # 1 cal to 0.001162 watt hour
    energyAllStudent = studentEnroll*calPerStudent*(value/100)
    energyPerMonth = (energyAllStudent*mealPerWeek*weekPerMonth)*0.001162
    return wastePerMonth, energyPerMonth

# calcualte GHG tons emission and offset
def GHGEmissionCal(totalWaste, compPercent, prodRedPercent, anaPercent):
    #weight in Ib/Ib
    productionEmssion = 1.662
    landfillEmissionRate = 0.374

    compostOffset = -0.19841
    anaerobicOffset = -0.110231

    landfillPercent = 100-compPercent-anaPercent

    prodEmission = totalWaste*productionEmssion*(100-prodRedPercent)/100
    compEmission = totalWaste*(1-prodRedPercent/100)*compostOffset*compPercent/100
    anaEmission = totalWaste*(1-prodRedPercent/100)*anaerobicOffset*anaPercent/100
    landfillEmission = totalWaste*(1-prodRedPercent/100)*landfillEmissionRate*landfillPercent/100

    return prodEmission, compEmission, anaEmission, landfillEmission

# update anaerobic slider value
@app.callback(
    [Output('Anaerobic1', 'max'), 
    Output('Anaerobic1', 'marks')],
    Input('compostSlider1', 'value'))
def setMaxAnaerobic(compostValue):
    maxValue = 100-compostValue
    return maxValue, {0: '0%', maxValue : str(maxValue)+'%' }

# plot comparision of GHG between no composing or reducing and with composting
@app.callback([Output('CompostLabel', 'children'),
    Output('AnaerobicLabel', 'children'),
    Output('GHGCompareFig1', 'figure'), 
    Output('GHGCompareText1', 'children')],
    #Input('totalWaste1', 'value'),
    Input('compostSlider1', 'value'), 
    Input('productionReduce1', 'value'),
    Input('Anaerobic1', 'value')
)
def updateCompareFig1(compostSlider, productionReduce, Anaerobic):
    GHGList1 = GHGEmissionCal(200, compostSlider, productionReduce, Anaerobic)
    GHGBase = GHGEmissionCal(200, 0, 0, 0)
    baseSum = sum(GHGBase)
    List1Sum = sum(GHGList1)
    
    betterPercentage = (baseSum-List1Sum)/baseSum*100
   
    label1=['Production Emission', 'Compost Offset', 'Anaerobic Offset', 'Landfill Emission']

    compareGHGfig = go.Figure(data = [
        go.Bar(name='Base Model', x=label1, y=GHGBase),
        go.Bar(name='Your Model', x = label1, y=GHGList1), 

    ])    
    
    compareGHGfig.update_layout(
        barmode='group',
        title={
            'text': 'Yearly GHG Emission Model Comparison (tons)',
            'x':0.5,
            'xanchor':'center'
        }
    )

    return '{:.1f} percent of the waste going to Composting'.format(compostSlider), \
        '{:.1f} percent of the waste going to Anaerobic Digester'.format(Anaerobic), \
        compareGHGfig, \
            'Base model total GHG emission is {:.2f} ton. '.format(baseSum) + \
                'Your model total GHG emission is {:.2f} ton. '.format(List1Sum) + \
                    'Your model reduce food waste GHG emission by {:.2f} percent. '.format(betterPercentage)
    
# Update written value
@app.callback(
    Output('wastedValLabel', component_property='children'),
    [Input(component_id="wastedSlider", component_property='value')])
def update_output_div2(value):
    return 'If we throw away {} percent of the food,'.format(value) , \
        html.Br(), 'we are wasting {:.2f} tons of food per month.'.format(wasteCal(value)[0]), \
        html.Br(), 'That is {:.2f}  watt hour of energy!'.format(wasteCal(value)[1])

# Update waste with line graphics
# TO DO: highlight month with student on campus, and average percentage when they are on campus
@app.callback(
    Output('wasteFig', 'figure'),
    [Input(component_id="wastedSlider", component_property='value')])
def update_wasteFig_div(value):
    waste_fig = px.bar(raw_waste, x='date', y='tons')
    waste_fig.update_layout(
        title={
            'text': 'Measured Food Wasted at MIT dining per month (tons)',
            'x':0.5,
            'xanchor':'center'
        }
    )
    waste_fig.add_trace(
    go.Scatter(
            y=[wasteCal(value)[0], wasteCal(value)[0]],
            x=['2019-12', '2009-1'],
        )
    )
    return waste_fig

# Plot waste distribution
@app.callback(
    Output('wasteComp', 'figure'),
    [Input('wasteCompDate', 'value')])
def update_wasteComp_div(date_value):
    wasteCompFilter = waste_comp[waste_comp['Date'] == date_value]
    wasteCompFig = px.sunburst(wasteCompFilter, path =['parent', 'food'], values = 'Percentage')
    wasteCompFig.update_layout(
        title={
        'text': 'Waste Composition in {}'.format(date_value),
        'x':0.5,
        'xanchor':'center'
    })

    return wasteCompFig

# Plot GHG contribution
@app.callback(
    Output('GHGCompFig', 'figure'),
    [Input('wasteCompDate', 'value')])
def update_wasteComp_div(date_value):
    GHGCompFilter = GHG_comp[GHG_comp['Date'] == date_value]
    GHGCompFig = px.sunburst(GHGCompFilter, path =['parent', 'food'], values = 'GHG_estimation')
    GHGCompFig.update_layout(
        title={
        'text': 'GHG emission based on waste composition in {}'.format(date_value),
        'x':0.5,
        'xanchor':'center'
    })

    return GHGCompFig

if __name__ == '__main__':
    app.run_server(debug=True)
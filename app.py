import os
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')
app.css.config.serve_locally=True
app.config['suppress_callback_exceptions']=True

server = app.server

diamonds = pd.read_csv('https://github.com/Stanley008/Project---Data/blob/master/diamonds.csv?raw=true')
#diamonds = pd.read_csv('diamonds.csv')

diamonds.drop(['Unnamed: 0'] , axis=1 , inplace=True)
diamonds = diamonds[(diamonds[['x','y','z']] != 0).all(axis=1)]

app = dash.Dash()

app.layout = html.Div(children=[
    
    html.H1(
        children='ICA2 Project - Programming Fundamentals'
    ),
    html.H3(
        children='Diamonds Statistics 2017'
    ),
    
    dcc.Markdown('''
## The data was downloaded from [Kaggle](https://www.kaggle.com/shivam2503/diamonds/version/1).

The data in this project represents 53940 diamonds with 10 values regarding it's carat, cut, color, clarity, depth, table, price, x-diameter, y-diameter, z-diameter.

*For further information about diamonds visit this electronical [encyklopedia](https://www.encyclopedia.com/earth-and-environment/minerals-mining-and-metallurgy/mineralogy-and-crystallography/diamond). If you are interested in **15 amazing diamonds facts** visit this [page](https://www.brilliantearth.com/news/15-amazing-facts-about-diamonds/).*

This project was created as an assignment *ICA2* at the end of semester by **Stanislav Brusnicky** (Prague College).

Choose a type of data for further investigation: 
    '''),
    
dcc.Dropdown(
        id = 'dropdown-input',
        options=[
            {'label': 'Price by cut', 'value': 'price'},
            {'label': 'Carat by cut', 'value': 'carat'},
            {'label': 'Depth by cut', 'value': 'depth'},
            {'label': 'Table by cut', 'value': 'table'},
        ],
        value='depth'
    ),
    
dcc.RadioItems(
    options=[
        {'label': 'Histogram', 'value': 'hist'},
        {'label': 'Box plot', 'value': 'box'},
        {'label': 'Scatter plot', 'value': 'scatter'},
        {'label': 'Bar plot', 'value': 'bar'},
    ],
    value='hist', # we dont need this, its the first value we want to output
    id = 'radio-input'
),
     dcc.Graph(
        id='example-graph',
    )
    
])


@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='radio-input', component_property='value'),
    Input(component_id='dropdown-input', component_property='value')]
)

def update_figure(plot_type, plot_data):
    if plot_data == 'price':
        first = diamonds[diamonds.cut == 'Fair'].price
        second = diamonds[diamonds.cut == 'Good'].price
        third = diamonds[diamonds.cut == 'Very Good'].price
        fourth = diamonds[diamonds.cut == 'Premium'].price
        fifth = diamonds[diamonds.cut == 'Ideal'].price
        title = "Price by Cut"
    elif plot_data == 'carat':
        first = diamonds[diamonds.cut == 'Fair'].carat
        second = diamonds[diamonds.cut == 'Good'].carat
        third = diamonds[diamonds.cut == 'Very Good'].carat
        fourth = diamonds[diamonds.cut == 'Premium'].carat
        fifth = diamonds[diamonds.cut == 'Ideal'].carat
        title = "Carat by Cut"
    elif plot_data == 'depth':
        first = diamonds[diamonds.cut == 'Fair'].depth
        second = diamonds[diamonds.cut == 'Good'].depth
        third = diamonds[diamonds.cut == 'Very Good'].depth
        fourth = diamonds[diamonds.cut == 'Premium'].depth
        fifth = diamonds[diamonds.cut == 'Ideal'].depth
        title = "Depth by Cut"
    else:
        first = diamonds[diamonds.cut == 'Fair'].table
        second = diamonds[diamonds.cut == 'Good'].table
        third = diamonds[diamonds.cut == 'Very Good'].table
        fourth = diamonds[diamonds.cut == 'Premium'].table
        fifth = diamonds[diamonds.cut == 'Ideal'].table
        title = "Table by Cut"
        
    if plot_type == 'hist':
        plot_function = go.Histogram
    elif plot_type == 'box':
        plot_function = go.Box
    elif plot_type == 'bar':
        plot_function = go.Bar
    else:
        plot_function = go.Scatter

    trace1 = plot_function(x = first, opacity = 0.75, name = 'Fair')
    trace2 = plot_function(x = second, opacity = 0.75, name = 'Good')
    trace3 = plot_function(x = third, opacity = 0.75, name = 'Very Good')
    trace4 = plot_function(x = fourth, opacity = 0.75, name = 'Premium')
    trace5 = plot_function(x = fifth, opacity = 0.75, name = 'Ideal')

    data = [trace1, trace2, trace3, trace4, trace5]

    figure={
        'data': data,
        'layout': {
            'title': title,
        },

    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
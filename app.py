import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

x=pd.DataFrame({'col':np.random.normal(size=1000)})
app.layout = html.Div(children=[
    html.H1(children=['Hello Dash', 'I am Jair']),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=px.histogram(x, x='col'))

        
])

'''{
    'data': [
        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
    ],
    'layout': {
        'title': 'Dash Data Visualization'
    }
}'''
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
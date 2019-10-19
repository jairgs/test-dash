import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px
import pandas as pd
from apirequest import getdata
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from scipy.stats import percentileofscore


df_main=getdata('493911')
df=df_main.copy()
df=df.sort_values('TIME_PERIOD', ascending=True)
df['party']=['pri']*8*4+['pan']*4*12+['pri']*4*6+['morena']*2

df['OBS_VALUE']=df['OBS_VALUE'].astype('float')
df['gwt']=df['OBS_VALUE'].pct_change()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def line():
    fig=go.Figure()

    # Create scatter trace of text labels
    fig.add_trace(go.Scatter(
        x=[2, 3.5, 6],
        y=[1, 1.5, 1],
        text=["Vertical Line",
            "Horizontal Dashed Line",
            "Diagonal dotted Line"],
        mode="text",
    ))

    # Set axes ranges
    fig.update_xaxes(range=[0, 7])
    fig.update_yaxes(range=[0, 2.5])

    # Add shapes
    fig.update_layout(
        shapes=[
            # Line Vertical
            go.layout.Shape(
                type="line",
                x0=1,
                y0=0,
                x1=1,
                y1=2,
                line=dict(
                    color="RoyalBlue",
                    width=3
                )
            ),
            # Line Horizontal
            go.layout.Shape(
                type="line",
                x0=2,
                y0=2,
                x1=5,
                y1=2,
                line=dict(
                    color="LightSeaGreen",
                    width=4,
                    dash="dashdot",
                ),
            ),
            # Line Diagonal
            go.layout.Shape(
                type="line",
                x0=4,
                y0=0,
                x1=6,
                y1=2,
                line=dict(
                    color="MediumPurple",
                    width=4,
                    dash="dot",
                ),
            ),
        ]
    )
    return fig

def histo():
    gwt=df['gwt'].dropna()
    fig = ff.create_distplot([gwt*100], ['Crecimiento Trimestral'],
        show_hist=True, show_rug=False, show_curve=True, bin_size=.5)
    fig.add_trace(go.Scatter(x=[gwt.iloc[-1], gwt.iloc[-1]], y=[0,.6], name='Último Trimestre', mode='lines', line={'dash':'dash', 'color':'crimson'}))
    fig.update_layout(title='Distribución del Crecimiento Trimestral', legend_orientation="h")
    return fig
histo()

#fig2=px.bar(df, x='TIME_PERIOD', y='gwt', color='party', category_orders=df['TIME_PERIOD'])
colors=['crimson']*8*4+['darkblue']*4*12+['crimson']*4*6+['maroon']*2
fig2=go.Figure()
fig2.add_trace(
    go.Bar(x=df['TIME_PERIOD'], y=df['gwt'], marker_color=colors))
fig2.update_layout(title='Crecimiento Trimestral del PIB Desestacionalizado a Precios Constantes')


#x=pd.DataFrame({'col':np.random.normal(size=1000)})
app.layout = html.Div(children=[
    html.H1(children='Visualización del Crecimiento Trimestral', style={'textAlign':'center'}),

    html.Div(children='Esta app actualiza en tiempo real los últimos datos del PIB publicados por INEGI', style={'textAlign':'center'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='whatever', figure=fig2)
            ], className='eight columns'), 
        html.Div([
            dcc.Graph(id='whatever2', figure=histo()), 
            html.Div(children='Último trimestre ('+df['TIME_PERIOD'].iloc[-1]+'): Percentil '+str(int(round(percentileofscore(df['gwt'].dropna(), df['gwt'].dropna().iloc[-1]), 0))), style={'textAlign':'center', 'backgroundColor':'GhostWhite'}, className='button')
            ], className='four columns') 
    ], className='row')
])


if __name__ == '__main__':
    app.run_server(port='8060', debug=True)
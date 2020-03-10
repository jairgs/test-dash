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
import dash_bootstrap_components as dbc

with open('Token') as file:
    Token=str(file.read())

df_main=getdata('493911', Token=Token)
df=df_main.copy()
df=df.sort_values('TIME_PERIOD', ascending=True)
party=['pri']*8*4+['pan']*4*12+['pri']*4*6
party+=['morena']*(df.shape[0]-len(party))
df['party']=party


colors=['crimson']*8*4+['darkblue']*4*12+['crimson']*4*6
colors+=['maroon']*(df.shape[0]-len(colors))



df['OBS_VALUE']=df['OBS_VALUE'].astype('float')
df['gwt']=df['OBS_VALUE'].pct_change()


external_stylesheets = ['assets/css/bootstrap.css']#['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
    fig.update_layout(title='Distribución del Crecimiento Trimestral', legend_orientation="h", margin={'l': 0, 'r': 0, 't': 50, 'b': 50})
    return fig
histo()

#fig2=px.bar(df, x='TIME_PERIOD', y='gwt', color='party', category_orders=df['TIME_PERIOD'])
fig2=go.Figure()
fig2.add_trace(
    go.Bar(x=df['TIME_PERIOD'], y=df['gwt'], marker_color=colors))
fig2.update_layout(
    margin={'l': 0, 'r': 0, 't': 50, 'b': 50}, 
    title='Crecimiento Trimestral del PIB'
)


#x=pd.DataFrame({'col':np.random.normal(size=1000)})
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(html.Img(src='assets/GitHub-Mark-32px.png'), 
        href="http://github.com/jairgs/test-dash"))
    ],
    brand="PIB Dashboard",
    brand_href="#",
    sticky="top",
    color="primary",
    dark=True
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Descripción"),
                        html.P(
                            """\
                        Esta app actualiza en tiempo real los últimos datos del PIB publicados por INEGI. 
                        """
                        ), 
                        html.P("Se utiliza el PIB desestacionalizado a precios de 2003.")
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        html.H2("Crecimiento"),
                        dcc.Graph(
                            figure=fig2
                        ),
                    ]
                ),
                dbc.Col(
                    [
                    html.H2("Distribución"),
                    dcc.Graph(figure=histo()), 
                    html.P('Último trimestre ('+df['TIME_PERIOD'].iloc[-1]+'): Percentil '+str(int(round(percentileofscore(df['gwt'].dropna(), df['gwt'].dropna().iloc[-1]), 0))), style={'textAlign':'center', 'backgroundColor':'GhostWhite'}, className='button')
                    ], md=3)
            ]
        )
    ],
    className="mt-4",
)

app.layout = html.Div([navbar, body])


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run_server(host='0.0.0.0', port=port, debug=False)
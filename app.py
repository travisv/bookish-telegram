import pandas as pd
import pathlib
from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('data').resolve()
df = pd.read_feather('data/financials.feather')

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
app.title = 'Financial Analysis'

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Financial Analysis",
    brand_href="#",
    color="primary",
    dark=True,
)

app.layout = html.Div([
    navbar,
    html.Div(children=[
        html.Hr(),
        html.Label('Tickers: '),
        dcc.Dropdown(df['Ticker'].unique(), id='ticker-dropdown', value='AAPL', style={'width':'120px'}),
        html.Br(),
        dcc.Graph('figure1'),
        dbc.Button('Button')
    ], style={'margin-left':'10px'})
])


@app.callback(Output('figure1', 'figure'), Input('ticker-dropdown', 'value'))
def render_figure1(ticker):
    return px.bar(df[df['Ticker']==ticker], x='Year', y='Revenues')


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

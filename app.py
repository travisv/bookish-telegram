import pandas as pd
import pathlib
from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('data').resolve()
df = pd.read_feather('/Users/travis/bookish-telegram/data/financials.feather')
tickers_options = [{'label':tick, 'value':tick} for tick in df['Ticker'].unique()]

search_navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
            dbc.Col(dbc.NavbarBrand("Financial Dashboard")),
            #dbc.NavbarBrand("Search", href="#"),
            dbc.NavbarToggler(id="navbar-toggler3"),
            dbc.Collapse(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Select(id='ticker-dropdown', options=tickers_options, value='AMD')
                        ),
#                        dbc.Col(
#                            dbc.Button(
#                                "Search", color="primary", className="ms-2"
#                            ),
#                            # set width of button column to auto to allow
#                            # search box to take up remaining space.
#                            width="auto",
#                        ),
                    ],
                    # add a top margin to make things look nice when the navbar
                    # isn't expanded (mt-3) remove the margin on medium or
                    # larger screens (mt-md-0) when the navbar is expanded.
                    # keep button and search box on same row (flex-nowrap).
                    # align everything on the right with left margin (ms-auto).
                    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                    align="center",
                ),
                id="navbar-collapse3",
                navbar=True,
            ),
        ]
    ),
    className="mb-5",
    color='dark',
    dark=True
)

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
app.title = 'Financial Analysis'
app.layout = html.Div([
    search_navbar,
    html.Div(children=[
        dcc.Dropdown(df.columns[13:], id='metric-dropdown', placeholder='Select a metric'),
        html.Br(),
        dcc.Graph(id='figure1'),
        html.Hr(),
        dcc.Graph(id='price-graph'),
    ], style={'margin-left':'10px'})
])

@app.callback(Output('figure1', 'figure'), Output('price-graph', 'figure'),
              Input('ticker-dropdown', 'value'), Input('metric-dropdown', 'value'),
              prevent_initial_call=True)
def render_figure1(ticker, metric):
    price = yf.download(ticker).reset_index()
    fig1 = px.bar(df[df['Ticker']==ticker], x='Year', y=metric)
    fig1.update_xaxes(range=[2000,2020], title_text='')
    fig1.update_yaxes(title_text='')
    price_fig = px.line(price, x='Date', y='Adj Close', log_y=True)
    price_fig.update_yaxes(tickformat='.2f', title_text='')
    price_fig.update_xaxes(title_text='Year')
    return fig1, price_fig

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)


### Notes

'''
dff = df[df['Ticker']==ticker]
fig = make_subplots(rows=2, cols=1)
fig.add_trace(go.Scatter(x=price['Date'], y=price['Adj Close']), row=1, col=1)
fig.add_trace(go.Bar(x=dff['Year'], y=dff['Revenues']), row=2, col=1)
fig.layout.height = 900
fig.update_yaxes(type='log')




'''

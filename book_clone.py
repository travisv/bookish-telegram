from urllib.parse import parse_qs, unquote
import plotly
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, callback_context, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State, ALL, ALLSMALLER, MATCH
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import yfinance as yf
pd.options.display.max_columns = None


# Initialize App
app = Dash(__name__, title='Finance App',
           external_stylesheets=[dbc.themes.SPACELAB])
# Load data
all_df = pd.read_feather('data/us_annuals.feather')
df = pd.read_csv('data/industry_annuals.csv')
industries = df.industry.unique().tolist()
industry_tickers = pd.read_csv('data/industry_tickers.csv')

# Main page layout
main_layout = html.Div([
    html.Div([
        dbc.NavbarSimple([
            dbc.DropdownMenu([
                dbc.DropdownMenuItem(industry, href=industry)
                for industry in industries], label='Select industry'),],
            brand='Home',brand_href='/', color='primary', dark=True,
            className='font-weight-bold'),
        dbc.Row([
            dbc.Col(lg=1, md=1, sm=1),
            dbc.Col([
                dcc.Location(id='location'),
                html.Div(id='main_content')
            ], lg=10),
        ]),
        html.Br(),
    ], style={'backgroundColor': '#E5ECF6'})
])

# Dashboard 1
industry_dashboard = dbc.Container([
    html.Br(),
    html.H1(id='industry_heading'),
    dbc.Row([
        dbc.Col(dcc.Graph(id='industry_page_graph')),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label('Select indicator:'),
            dcc.Dropdown(id='industry_page_indicator_dropdown',
                         placeholder='Choose an indicator',
                         value='revenue',
                         options=[{'label': indicator, 'value': indicator}
                                  for indicator in df.columns]),
        ]),
        dbc.Col([
            dbc.Label('Select industries:'),
            dcc.Dropdown(id='industry_page_industry_dropdown',
                         placeholder='Select one or more countries to compare',
                         multi=True,
                         options=[{'label': i, 'value': i}
                                  for i in industries]),
        ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([html.Div(id='ticker_sidebar')]),
    ]),
    html.Br(), html.Br(),
    #        html.Div(id='country_table')
], fluid=True)

# Dashboard 2
indicators_dashboard = dbc.Container([
    #html.H1("Indicators Dashboard")
    html.Br(),
    html.H1(id='company_heading'),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='company_price_graph'),
            dcc.Graph(id='company_page_graph'),
            html.Div(id='table-container',
                     children=[
                         dash_table.DataTable(
                             id='table',
                             columns=[{'name': i, 'id': i}
                                      for i in all_df.columns],
                             style_table={'overflowx': 'auto'}
                         )
                     ]),
        ]),
    ]),

])

# Validation
app.validation_layout = html.Div([
    main_layout,
    indicators_dashboard,
    industry_dashboard
])

# Layout
app.layout = main_layout


@app.callback(Output('main_content', 'children'),
              Input('location', 'pathname'))
def display_content(pathname):
    if unquote(pathname[1:]) in industries:
        return industry_dashboard
    else:
        return indicators_dashboard

@app.callback(Output('ticker_sidebar', 'children'),
              Input('industry_page_industry_dropdown', 'value'))
def display_ticker_sidebar(industry):
    tmp = industry_tickers[industry_tickers['industry'].isin(industry)]
    tickers = tmp['symbol'].unique().tolist()
    cards = html.Div([dbc.CardGroup([
        dbc.Card(
            dbc.CardBody([
                dbc.CardLink(t, href=t),
                html.P('Some info about this company', className='card-text'),
            ])) for t in tickers]),
    ])
    return cards

@app.callback(Output('industry_page_industry_dropdown', 'value'),
              Input('location', 'pathname'))
def set_dropdown_values(pathname):
    if unquote(pathname[1:]) in industries:
        industry = unquote(pathname[1:])
        return [industry]

@app.callback(Output('industry_heading', 'children'),
              Output('industry_page_graph', 'figure'),
              Input('location', 'pathname'),
              Input('industry_page_industry_dropdown', 'value'),
              Input('industry_page_indicator_dropdown', 'value'))
def plot_industry_charts(pathname, industries, indicator):
    if (not industries) or (not indicator):
        raise PreventUpdate
    if unquote(pathname[1:]) in industries:
        industry = unquote(pathname[1:])
        dff = df[df['industry'].isin(industries)]
        fig = px.line(dff, x='year', y=indicator,
                      title='<b>' + str(indicator).capitalize() + '</b><br>',
                      color='industry')
        fig.layout.paper_bgcolor = '#E5ECF6'
        fig.layout.template = 'ggplot2'
        return ', '.join(industries) + ' Data', fig


@app.callback(Output('company_heading', 'children'),
              Output('company_price_graph', 'figure'),
              Output('company_page_graph', 'figure'),
              Output('table', 'data'),
              Input('location', 'pathname'))
def render_company_page(pathname):
    ticker = unquote(pathname[1:])
    dff = all_df[all_df['symbol'] == ticker]
    fig = px.bar(dff, x='period_end_date', y='revenue')
    dff = dff.dropna(how='all', axis=1)
    tab = dff.to_dict('records')


    prices = yf.download(ticker).reset_index()
    price_fig = px.line(prices, x='Date', y='Adj Close')

    return f'{ticker}: ', price_fig, fig, tab

app.run_server(debug=True, port=8033)

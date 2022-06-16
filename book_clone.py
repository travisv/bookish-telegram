from urllib.parse import parse_qs, unquote
import plotly
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, callback_context, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State, ALL, ALLSMALLER, MATCH
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
pd.options.display.max_columns = None


# Initialize App
app = Dash(__name__, title='Finance App', external_stylesheets=[dbc.themes.COSMO])
# Load data
df = pd.read_csv('data/industry_annuals.csv')
industries = df.industry.unique().tolist()
# Main page layout
main_layout = html.Div([
    html.Div([
    dbc.NavbarSimple([
            dbc.DropdownMenu([
                dbc.DropdownMenuItem(industry, href=industry) for industry in industries
            ], label='Select industry'),
    ], brand='Home',brand_href='/', light=True),
    dbc.Row([
        dbc.Col(lg=1, md=1, sm=1),
        dbc.Col([

            dcc.Location(id='location'),
            html.Div(id='main_content')
        ], lg=10),
    ])
], style={'backgroundColor': '#E5ECF6'})
])
# Dashboard 1
industry_dashboard = html.Div([
    html.Br(),
        html.H1(id='industry_heading'),
        dbc.Row([
            dbc.Col(dcc.Graph(id='industry_page_graph'))
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
        html.Br(), html.Br(),
#        html.Div(id='country_table')
])
# Dashboard 2
indicators_dashboard = html.Div([
    html.H1("Indicators Dashboard")
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

@app.callback(Output('industry_page_industry_dropdown', 'value'),
              Input('location', 'pathname'))
def set_dropdown_values(pathname):
    if unquote(pathname[1:]) in industries:
        industry = unquote(pathname[1:])
        return [industry]

@app.callback(Output('industry_heading', 'children'),
              Output('industry_page_graph', 'figure'),
              #Output('industry_table', 'children'),
              Input('location', 'pathname'),
              Input('industry_page_industry_dropdown', 'value'),
              Input('industry_page_indicator_dropdown', 'value'))
def plot_industry_charts(pathname, industries, indicator):
    if (not industries) or (not indicator):
        raise PreventUpdate
    if unquote(pathname[1:]) in industries:
        industry = unquote(pathname[1:])
    #df = poverty[poverty['is_country'] & poverty['Country Name'].isin(countries)]
    dff = df[df['industry'].isin(industries)]
    fig = px.line(dff,
                  x='year',
                  y=indicator,
                  #title='<b>' + indicator + '</b><br>' + ', '.join(countries),
                  color='industry'
                  )
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig.layout.template = 'ggplot2'
    #table = country_df[country_df['Short Name'] == countries[0]].T.reset_index()
    #if table.shape[1] == 2:
    #    table.columns = [countries[0] + ' Info', '']
    #    table = dbc.Table.from_dataframe(table)
    #else:
    #    table = html.Div()
    return indicator + ' Data', fig #, table


app.run_server(debug=True, port=8033)

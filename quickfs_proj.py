import os
#from dotenv import load_dotenv
#from quickfs import QuickFS
from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
#load_dotenv()

# load the key from the enviroment variables
#api_key = os.environ['quickfs_api_key']
#client = QuickFS(api_key)
## Usage history
#resp = client.get_usage()
#print(f'Current usage total: {resp}')
#nyse = client.get_supported_companies('US', 'NYSE')
df = pd.read_csv('data/industry_annuals.csv')
df['ppe_/_da'] = df['cfi_ppe_purchases'] * -1 / df['cfo_da']
industries = df['industry'].sort_values().dropna().unique()
metrics = list(df.columns)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.layout = html.Div([
    dcc.Dropdown([{'label':tick, 'value':tick}
                  for tick in industries], id='industry-dropdown', value='Banks'),
    dcc.Dropdown([{'label':metric, 'value':metric}
                  for metric in metrics], id='metric-dropdown', value='revenue'),
    dcc.Graph(id='bar-fig'),
    dcc.Graph(id='line-fig'),
    dash_table.DataTable(id='table', data=df.to_dict('records'), columns=[{'name':i, 'id':i} for i in df.columns])
])



@app.callback(Output('table', 'data'),
              Input('industry-dropdown', 'value'))
def render_table(industry):
    mask = df['industry'] == industry
    dff = df[mask]
    data = dff.to_dict('records')
    columns = [{'name': i, 'id': i} for i in dff.columns]
    return [dash_table.DataTable(data=data, columns=columns)]


@app.callback(Output('bar-fig', 'figure'),
              Output('line-fig', 'figure'),
              Input('industry-dropdown', 'value'),
              Input('metric-dropdown', 'value'))
def render_bar_fig(industry, metric):
    mask = df['industry'] == industry
    dff = df[mask]
    bar_fig = px.bar(dff, x='year', y=metric, range_x=[2000,2022])
    line_fig = make_subplots(specs=[[{"secondary_y": True}]])
    line_fig.add_trace(go.Scatter(x=dff['year'],
                                  y=dff['ppe_/_da'], mode='lines',
                                  name='PPE / DA'))
    line_fig.add_trace(go.Scatter(x=dff['year'],
                                  y=dff['roe'], mode='lines',
                                  name='ROE'), secondary_y=True)
    return bar_fig, line_fig


if __name__ == '__main__':
    app.run_server(debug=True)




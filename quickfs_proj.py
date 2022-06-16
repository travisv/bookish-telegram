import os
from dotenv import load_dotenv
from quickfs import QuickFS
from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import plotly.express as px
#import dash_table as dt

load_dotenv()

# load the key from the enviroment variables
#api_key = os.environ['quickfs_api_key']
#client = QuickFS(api_key)
## Usage history
#resp = client.get_usage()
#print(f'Current usage total: {resp}')
#nyse = client.get_supported_companies('US', 'NYSE')
df = pd.read_pickle('data/clean_annual.pickle')
df['ppe_/_da'] = df['cfi_ppe_purchases'] * -1 / df['cfo_da']
industries = df['industry'].sort_values().dropna().unique()
metrics = list(df.columns[9:])

app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown([{'label':tick, 'value':tick}
                  for tick in industries], id='industry-dropdown', value='Banks'),
    dcc.Dropdown([{'label':metric, 'value':metric}
                  for metric in metrics], id='metric-dropdown', value='revenue'),
    dcc.Graph(id='bar-fig'),
])


@app.callback(Output('bar-fig', 'figure'), Input('industry-dropdown', 'value'),
              Input('metric-dropdown', 'value'))
def render_bar_fig(industry, metric):
    mask = df['industry'] == industry
    dff = df[mask]
    dff = dff.groupby(['industry', 'year']).sum().reset_index()
    fig = px.bar(dff, x='year', y=metric, range_x=[2000,2022])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)




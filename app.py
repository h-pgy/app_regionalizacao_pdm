import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import random

#abre dados
df = pd.read_csv('dados_regionalizacao_pdm.csv', sep = ';')
#precisa arrumar a coluna para dar merge depois
df['codigo_subs'] = df['codigo_subs'].apply(lambda x: str(int(x)) if pd.notnull(x) else '')
df['codigo_zonas'] = df['codigo_zonas'].apply(lambda x: str(int(x)) if pd.notnull(x) else '')

df['valor'].fillna(0, inplace=True)

#abre shapes e arrumar projeção
subs = gpd.read_file('mapas/subs/SIRGAS_SHP_subprefeitura_polygon.shp')
subs.set_crs(epsg='31983', inplace=True)
subs.to_crs(epsg=4326,inplace=True)
zonas = gpd.read_file('mapas/regioes/SIRGAS_REGIAO5.shp')
zonas.set_crs(epsg='31983', inplace=True)
zonas.to_crs(epsg=4326, inplace=True)

secretarias = df['secretaria'].unique()
metas = df['numero_meta'].unique()

def metas_por_secretaria(secretaria):

    mask = df['secretaria']==secretaria

    return df[mask]['numero_meta'].unique()

def filtrar_por_meta(meta_num):

    mask = df['numero_meta']==meta_num
    
    return df[mask]

def merge_subs(df):

    merged = pd.merge(subs, df, left_on='sp_codigo', right_on='codigo_subs', how='left')
    merged['valor'].fillna(0, inplace=True)

    return merged

def merge_zonas(df):

    merged = pd.merge(zonas, df, left_on='COD_REG_5', right_on='codigo_zonas', how='left')

    merged['valor'].fillna(0, inplace=True)

    return merged

def decidir_plot(df):

    if df['codigo_subs'].isnull().all():

        return merge_zonas(df)
    
    return merge_subs(df)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Regionalização PDM'

app.layout = html.Div([
    html.H1('Regionalização: Programa de Metas 2021-2024'),
    dcc.Graph(id="choropleth"),
    html.Div(children=[
    dcc.Dropdown(
        id='dropdown-secretarias',
        options=[
            {'label': secretaria, 'value': secretaria}
            for secretaria in secretarias
        ],
        value='',
        style={'display': 'inline-block',
        'width' : '40%',
        'height': '20px',
        'padding': '10px',
        'text-align': 'left',},
    ),
    dcc.Dropdown(
        id='dropdown-metas',
        options=[
            {'label': meta, 'value': meta}
            for meta in metas
        ],
        value=random.choice(metas),
        style={'display': 'inline-block',
        'width' : '40%',
        'height': '20px',
        'padding': '10px',
        'text-align': 'right',},
    ),
    ])
])

@app.callback(
    dash.dependencies.Output('dropdown-metas', 'options'),
    [dash.dependencies.Input('dropdown-secretarias', 'value')])
def update_metas(value):
    
    metas = metas_por_secretaria(value)
    return [{'label': meta, 'value': meta}
            for meta in metas
        ]

@app.callback(
    Output("choropleth", "figure"), 
    [Input("dropdown-metas", "value")])
def display_choropleth(meta):

    data = filtrar_por_meta(meta)
    geo_df = decidir_plot(data)

    fig = px.choropleth(
        geo_df,
        geojson=geo_df.geometry,
        locations=geo_df.index,
        color = 'valor',
        color_continuous_scale = 'Blues'
        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig

app.run_server(debug=True)
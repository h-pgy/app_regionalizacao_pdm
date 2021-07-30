import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import random
from utils import (metas_por_secretaria, filtrar_por_meta, 
    decidir_plot, prep_shapefiles, prep_data)

#abre os dados utilizados no dash
df = prep_data()

#abre shapes e arrumar projeção
subs, zonas = prep_shapefiles()

secretarias = df['secretaria'].unique()
metas = df['numero_meta'].unique()



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Regionalização PDM'
server = app.server

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
        placeholder="Secretaria Responsável",
        style={'display': 'inline-block',
        'width' : '40%',
        'height': '20px',
        'padding': '10px',
        'text-align': 'center',},
    ),
    dcc.Dropdown(
        id='dropdown-metas',
        options=[
            {'label': meta, 'value': meta}
            for meta in metas
        ],
        value=random.choice(metas),
        placeholder="Número da meta",
        style={'display': 'inline-block',
        'width' : '40%',
        'height': '20px',
        'padding': '10px',
        'text-align': 'center',
        'position': 'relative'},
    ),
    ])
])

@app.callback(
    dash.dependencies.Output('dropdown-metas', 'options'),
    [dash.dependencies.Input('dropdown-secretarias', 'value')])
def update_metas(secretaria):
    
    metas = metas_por_secretaria(df, secretaria)
    return [{'label': meta, 'value': meta}
            for meta in metas
        ]

@app.callback(
    Output("choropleth", "figure"), 
    [Input("dropdown-metas", "value")])
def display_choropleth(meta):

    data = filtrar_por_meta(df, meta)
    geo_df = decidir_plot(data, subs, zonas)

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

if __name__ == "__main__":

    app.run_server(debug=True)
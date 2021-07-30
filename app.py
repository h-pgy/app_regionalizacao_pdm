import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import random
from utils import (metas_por_secretaria, filtrar_por_meta, 
    decidir_plot, prep_shapefiles, prep_data, get_meta_data)
from front_end import simple_jumbotron, navbar, card_meta

#abre os dados utilizados no dash
df = prep_data()

#abre shapes e arrumar projeção
subs, zonas = prep_shapefiles()

secretarias = df['secretaria'].unique()
metas = df['numero_meta'].unique()



external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Regionalização PDM'
server = app.server

app.layout = html.Div([
    #cabeçalho
    html.Div([
    navbar,
    ]),
    #explicação app
    html.Div([
        simple_jumbotron,
        #botoes
        html.Div(
            children=[
                html.H6('Escolha a Secretaria Responsável'),
                dcc.Dropdown(
                    id='dropdown-secretarias',
                    options=[
                        {'label': secretaria, 'value': secretaria}
                        for secretaria in secretarias
                    ],
                    value='',
                    placeholder="Secretaria Responsável",
                    style={'padding':'5px'}
                ),
                html.H6('Escolha a meta que deseja visualizar'),
                dcc.Dropdown(
                    id='dropdown-metas',
                    options=[
                        {'label': meta, 'value': meta}
                        for meta in metas
                    ],
                    value=random.choice(metas),
                    placeholder="Número da meta",
                    style={'padding':'5px'}
                    
                )
            ],
            style={'float':'left', 'width' : '50%', 'padding':'50px'}
            ), 
        ], 
        className='flex-container',
        ),
    html.Div([
        dcc.Graph(id="choropleth", style = {'display' : 'inline-block', 'width': '80%', 'float' : 'left'}),
        card_meta
        ],
    className='flex-container'
    ),
    
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

@app.callback(
    Output("card-meta", "children"), 
    [Input("dropdown-metas", "value")])
def display_card_meta(meta):


    num, desc, indicador, secretaria = get_meta_data(df, meta)
    children = [
            html.H4(f"Meta {num}", className="card-title"),
            html.H6("Descrição da meta", className="card-subtitle"),
            html.P(
                desc,
                className="card-text",
            ),
            html.H6("Indicador:", className="card-subtitle"),
            html.P(
                indicador,
                className="card-text",
            ),
            html.H6("Secretaria(s) Responsável:", className="card-subtitle"),
            html.P(
                secretaria,
                className="card-text",
            )
        ]

    return children


if __name__ == "__main__":

    app.run_server(debug=True)
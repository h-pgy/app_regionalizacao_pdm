import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


simple_jumbotron = dbc.Jumbotron(
    [
        html.H2("Regionalização: Programa de Metas 2021-24", className="display-5"),
        html.P(
            "Aplicação que permite visualizar a regionalizaçaõ das Metas do "
            "Programa de Metas 2021-2024.",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P(
            "Secretaria Executiva de Planejamento e Entregas Prioritárias"
            "da Secretaria de Governo da Prefeitura Municipal de São Paulo"
        ),
    ],
    style = {'height' : '5', 'float' : 'left'}
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("PDM 2021-2024", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Nossos Portais", header=True),
                dbc.DropdownMenuItem("Portal SEPEP", href="#"),
                dbc.DropdownMenuItem("Portal Prefeitura", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Mais",
        ),
    ],
    brand="SEPEP",
    color="primary",
    dark=True,
)

card_meta = dbc.Card(
    dbc.CardBody(
    id = 'card-meta',),
    style={"width": "30%", 'display' : 'inline-block', 'float' : 'left'},
)
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, dcc, html, Dash, callback
import numpy as np
import plotly.graph_objs as go

dash.register_page(__name__, path="/")

localidad = ['BARRIOS UNIDOS', 'ENGATIVÁ', 'SUMAPAZ', 'TEUSAQUILLO', 'LA CANDELARIA',
             'SANTA FE', 'SUBA', 'FONTIBÓN', 'LOS MÁRTIRES', 'SAN CRISTOBAL', 'USME', 'PUENTE ARANDA',
             'USAQUÉN', 'BOSA', 'CIUDAD BOLÍVAR', 'RAFAEL URIBE URIBE', 'KENNEDY', 'CHAPINERO', 'TUNJUELITO',
             'ANTONIO NARIÑO']

style = {"padding": "1rem 1rem"}

# Crear mapa
mapbox_access_token = "pk.eyJ1IjoiYWx0b3ItYmFnaCIsImEiOiJjbDN4a2V6cXkzMTd0M2RwbjhheXM4dW1oIn0.gVUcxM-EHq5Se4_MOv-_4Q"

data_map = go.Scattermapbox(
    lat=['4.654587'],
    lon=['-74.093552'],
    mode='markers'
)

layout_mapa = go.Layout(title="Mapa de Bogotá",
                   mapbox=dict(
                       accesstoken=mapbox_access_token,
                       zoom=10,
                       style='open-street-map',
                       bearing=0,
                       center=go.layout.mapbox.Center(
                           lat=4.65,
                           lon=-74.09
                       )
                   ))

figure = go.Figure(data=data_map, layout=layout_mapa)


# layout página
layout = html.Div(children=[
    dbc.Row([
        dbc.Col([
            html.Div(
                   [
                   dbc.Label("Ingrese la dirección del inmueble"),
                   dbc.Input(id="input-dirección", placeholder='', persistence=True, persistence_type="session"),
                   ], style=style
                   ),
            html.Div([
                    dbc.Label("Ingrese la localidad del inmueble"),
                    dcc.Dropdown(options=localidad,
                                 placeholder="",
                                 id="dropdown-localidad",
                                 persistence=True, persistence_type="session"),
                    ],
                    style=style
                    ),
            html.Div([
                dbc.Label("Seleccione el estrato socioeconómico"),
                dcc.Dropdown(options=[1, 2, 3, 4, 5, 6], id="dropdown-estrato", placeholder="seleccione...",
                             persistence=True, persistence_type="session")
                    ],
                    style=style
           ),
            html.Div([
               dbc.Label("Introduzca el número de habitaciones"),
               dbc.Input(id="input-habitaciones", placeholder="1", type="number", min=1,
                         persistence=True, persistence_type="session")
                ],
               style=style
            ),
            html.Div([
               dbc.Label("Introduzca el número de baños"),
               dbc.Input(id="input-baños", placeholder="1", type="number", min=1,
                         persistence=True, persistence_type="session")
                ],
               style=style
            ),
            html.Div([
               dbc.Label("Introduzca el área en metros cuadrados"),
               dbc.Input(id="input-m2", placeholder="25", type="number", min=10,
                         persistence=True, persistence_type="session")
                ],
               style=style
            ),
            html.Div([
                dbc.Label("¿Con qué más cuenta el inmueble?"),
                dbc.Checklist(
                    options=[
                        {'label': 'Arriendo', 'value': 'Arriendo'},
                        {'label': 'Compra/Venta', 'value': 'Compra/Venta'},
                    ], id='características-adicionales',
                    persistence=True, persistence_type="session"
                )
                ],
                style=style
                )
        ], align="start", width=4),
        dbc.Col([
            html.Div([
                dcc.Graph(figure=figure)]),
            html.Hr(),
            html.Div([dbc.Button("Enviar formulario", size="lg", className="me-1",
                                 id="boton_state", n_clicks=0, color="danger")]),
            html.Div(id="alerta", children=[], style=style)
        ], style=style, width=8)
    ])
])


@callback(
    Output("intermediate-value", "data"),
    Input("boton_state", "n_clicks"),
    [State("dropdown-localidad", "value"),
     State("dropdown-estrato", "value"),
     State("input-habitaciones", "value"),
     State("input-baños", "value"),
     State("input-m2", "value")]
)
def diccionario_prediccion(n_clicks, localidad, estrato, habitaciones, baños, m2):
    if n_clicks > 0:
        data = pd.DataFrame.from_dict({"baños": [baños],
                         "cuartos":[habitaciones],
                         "localidad": [localidad],
                         "estrato": [estrato],
                         "área": [m2]
                         })
        if not data.isnull().values.any():
            data_json = data.to_json(orient="split")
            return data_json


@callback(
    Output("alerta", "children"),
    [Input("boton_state", "n_clicks"),
     Input("intermediate-value", "data")]
)
def crear_alerta(n_clicks, data):
    df = pd.read_json(data, orient="split")
    check_NaN = df.isnull().values.any()
    if n_clicks > 0:
        if check_NaN:
            children = dbc.Alert("Por favor diligencie todos los campos para ver su resultado", color="primary")
            return children
        else:
            children = dbc.Alert("Perfecto! Por favor continúe a la página de resultados", color="success")
            return children


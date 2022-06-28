import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, dcc, html, Dash, callback
import pandas
import numpy
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
                   dbc.Input(id="input-dirección", placeholder=''),
                   ], style=style
                   ),
            html.Div([
                    dbc.Label("Ingrese la localidad del inmueble"),
                    dcc.Dropdown(options=localidad,
                                 placeholder="",
                                 id="dropdown-localidad"),
                    ],
                    style=style
                    ),
            html.Div([
                dbc.Label("Seleccione el estrato socioeconómico"),
                dcc.Dropdown(options=[1, 2, 3, 4, 5, 6], id="dropdown-estrato", placeholder="seleccione...")
                    ],
                    style=style
           ),
            html.Div([
               dbc.Label("Introduzca el número de habitaciones"),
               dbc.Input(id="input-habitaciones", placeholder="1", type="number", min=1)
                ],
               style=style
            ),
            html.Div([
               dbc.Label("Introduzca el número de baños"),
               dbc.Input(id="input-baños", placeholder="1", type="number", min=1)
                ],
               style=style
            ),
            html.Div([
               dbc.Label("Introduzca el área en metros cuadrados"),
               dbc.Input(id="input-m2", placeholder="25", type="number", min=10)
                ],
               style=style
            ),
            html.Div([
                dbc.Label("¿Con qué más cuenta el inmueble?"),
                dbc.Checklist(
                    options=[
                        {'label': 'Parqueadero', 'value': 'parqueadero'},
                        {'label': 'Jardín', 'value': 'Jardín'},
                        {'label': 'Parque recreativo', 'value': 'Parque recreativo'},
                        {'label': 'Gimnasio', 'value': 'Gimnasio'},
                    ], id='características-adicionales'
                )
                ],
                style=style
                )
        ], align="start", width=4),
        dbc.Col([
            html.Div([
                dcc.Graph(figure=figure)])
        ], style=style, width=8)
    ])
])


@callback(
    Output("intermediate-value", "data"),
    [Input("dropdown-localidad", "value"),
     Input("dropdown-estrato", "value"),
     Input("input-habitaciones", "value"),
     Input("input-baños", "value"),
     Input("input-m2", "value")]
)
def diccionario_prediccion(localidad, estrato, habitaciones, baños, m2):
    data = pd.DataFrame.from_dict({"baños": [baños],
                     "cuartos":[habitaciones],
                     "localidad": [localidad],
                     "estrato": [estrato],
                     "área": [m2]
                     })
    data_json = data.to_json(orient="split")
    return data_json

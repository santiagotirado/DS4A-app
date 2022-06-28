import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, Dash, callback
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import statsmodels.formula.api as smf
import statsmodels.api as sm


dash.register_page(__name__, path="/resultados")

style = {"padding": "1rem 1rem"}

#dummy function
localidad = ['BARRIOS UNIDOS', 'ENGATIVÁ', 'SUMAPAZ', 'TEUSAQUILLO', 'LA CANDELARIA',
             'SANTA FE', 'SUBA', 'FONTIBÓN', 'LOS MÁRTIRES', 'SAN CRISTOBAL', 'USME', 'PUENTE ARANDA',
             'USAQUÉN', 'BOSA', 'CIUDAD BOLÍVAR', 'RAFAEL URIBE URIBE', 'KENNEDY', 'CHAPINERO', 'TUNJUELITO',
             'ANTONIO NARIÑO']


def create_dummy(data, seed, size):
    np.random.seed(seed)
    df = pd.DataFrame()
    df["baños"] = np.random.randint(1, 12, size=size, dtype="int8")
    df["cuartos"] = np.random.randint(1, 20, size=size, dtype="int8")
    df["localidad"] = np.random.choice(localidad, size=size)
    df["localidad"] = df["localidad"].astype("category")
    df["estrato"] = np.random.randint(1, 7, size=size, dtype="int8")
    df["área"] = np.random.randint(10, 500, size=size, dtype="int16")
    df["valor_dolar"] = np.random.randint(8000, 250000, size=size, dtype="int32")
    model = smf.ols("valor_dolar ~ estrato + área + localidad + cuartos + baños", data=df).fit()
    prediction = model.predict(data)
    return prediction


# Components
def tarjeta_resultados(titulo, contenido):
    children = html.Div([
        html.H3(titulo, className="ms-1"),
        html.Hr(className="my-2"),
        html.H3(contenido, className="ms-1")
    ], className="h-100 p-5 bg-light border rounded-3"
    )
    return children

#Layout

layout = html.Div(children=[
    dbc.Row([
        dbc.Col(id="resultado-precio", children=[], style=style),
        dbc.Col(id="precio-m2", children=[], style=style)
    ]),
    dbc.Row(
        html.Div(id="tabla_valores", children=[], style=style)
    )
])


#Functions

@callback(
    Output("resultado-precio", "children"),
    Input("intermediate-value", "data")
)
def precio_total_inmueble(data):
    df = pd.read_json(data, orient="split")
    prediction = create_dummy(data=df, seed=23, size=100_000)[0]
    children = tarjeta_resultados(titulo="El precio del inmueble es: ", contenido=str(int(prediction)))
    return children

@callback(
    Output("precio-m2", "children"),
    Input("intermediate-value", "data")
)
def precioXm2(data):
    df = pd.read_json(data, orient="split")
    prediction = create_dummy(data=df, seed=23, size=100_000)[0]
    m2 = prediction / df.iloc[0, 4]
    children = tarjeta_resultados(titulo="El precio por metro cuadrado es de: ", contenido=str(int(m2)))
    return children

@callback(
    Output("tabla_valores", "children"),
    Input("intermediate-value", "data")
)
def tabla_costos_adicionales(data):
    df = pd.read_json(data, orient="split")
    prediction = create_dummy(data=df, seed=23, size=100_000)[0]
    data = {"Derechos notariales": ["Derechos notariales", int(prediction)*0.004, int(prediction)*0.004],
            "IVA": ["IVA", int(prediction)*0.19, int(prediction)*0.19],
            "Retefuente": ["Retefuente", 0, int(prediction)*0.01],
            "Boleta fiscal/Benficiencia": ["Boleta fiscal/Benficiencia", int(prediction)*0.01, 0],
            "Registro": ["Registro", int(prediction)*0.00861, 0],
            "Otros gastos": ["Otros gastos", 100000, 100000]}
    dff = pd.DataFrame.from_dict(data, orient="index", columns=["Tipo de gasto", "Comprador", "Vendedor"])
    children = dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)
    return children
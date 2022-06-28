import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, Dash


app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL], use_pages=True, suppress_callback_exceptions=True)

# Estilos
navbar_style = {
    "padding": "1rem 1rem",
    "background-color": "#e6cbf5",
}

contenido_style = {"padding": "2rem 1rem"}

# Componentes de base
navbar = html.Div([
    html.H3("Predicción de precio de bienes raíces en Bogotá"),
    dbc.Nav([
        dbc.NavLink("Inicio", href="/", active="exact"),
        dbc.NavLink("Resultados", href="/resultados", active="exact"),
        dbc.NavLink("Nosotros", href="/nosotros", active="exact")
    ], pills=True, fill=True)
], style=navbar_style)


contenido = html.Div(id="contenido-página", children=[], style=contenido_style)


# Layout de la página
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    dcc.Store(id="intermediate-value"),
    dcc.Store(id="trial"),
    dash.page_container
])



# Correr aplicación

if __name__=='__main__':
    app.run_server(debug=True, port=3000)
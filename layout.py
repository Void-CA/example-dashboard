from dash import html, dcc

# Definición del layout
layout = html.Div([
    html.H1("Dashboard limpio y modular", style={"textAlign": "center"}),

    dcc.Dropdown(
        id="dropdown-feature",
        options=[
            {"label": "Opción 1", "value": 'sepal_width'},
            {"label": "Opción 2", "value": "value2"}
        ],
        placeholder="Selecciona una opción"
    ),

    dcc.Graph(id="main-graph"),

    html.Div(id="output-container")
])

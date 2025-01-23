from dash import Dash

# Inicializar la aplicación
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Para desplegar en un servidor

# Importar layout y callbacks
from layout import layout
from callbacks import register_callbacks

# Establecer layout
app.layout = layout

# Registrar callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)

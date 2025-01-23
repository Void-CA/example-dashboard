from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Dataset de ejemplo
df = px.data.iris()

def register_callbacks(app):
    @app.callback(
        Output("main-graph", "figure"),
        Input("dropdown-feature", "value")
    )
    def update_graph(selected_feature):
        if selected_feature is None:
            return {}
        fig = px.scatter(df, x=selected_feature, y="sepal_length", color="species",
                         title=f"Relación entre {selected_feature} y sepal_length")
        return fig

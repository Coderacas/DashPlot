import pickle

with open("graficas.pkl", "rb") as f:
    grafs_dict = pickle.load(f)

import dash
from dash import dcc, html

app = dash.Dash(__name__)

graf_options = [{"label": grafs_dict[g]["title"], "value": g} for g in grafs_dict]

app.layout = html.Div([
    dcc.Dropdown(
        id="graf-selector",
        options=graf_options,
        value=list(grafs_dict.keys())[0]
    ),

    html.H2(id="graf-title"),

    dcc.Graph(id="graf-placeholder")
])

from dash.dependencies import Input, Output

@app.callback(
    [Output("graf-title", "children"),
     Output("graf-placeholder", "figure")],
    [Input("graf-selector", "value")]
)
def update_graph(selected_graf):
    data = grafs_dict[selected_graf]
    return data["title"], data["figure"]

app.run()
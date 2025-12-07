"""
DASHBOARD INTERACTIVO – ACTIVIDAD PLOTLY & DASH
Autor: Oscar Méndez Sánchez
"""

# ==========================================================
#                     IMPORTACIONES
# ==========================================================

import pickle
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# ==========================================================
#                CARGA DE GRÁFICAS DESDE PKL
# ==========================================================

with open("graficas.pkl", "rb") as f:
    grafs_dict = pickle.load(f)


# ==========================================================
#                DESCRIPCIONES DE LAS GRÁFICAS
# ==========================================================

descripciones = {
    "graf1": """La gráfica muestra que soundtrack es el género con mayor representación 
    en el DataSet, seguido por pop y por mezclas multigénero como country, pop, indie y folk, 
    lo que sugiere que la base de datos contiene una mezcla fuerte entre música comercial y 
    bandas sonoras. Aunque el top está relativamente equilibrado, la presencia dominante del 
    soundtrack indica que este tipo de contenido aparece de manera muy consistente.""",

    "graf2": """La gráfica evidencia que Taylor Swift domina ampliamente con más de 320 canciones, 
    superando con gran diferencia al resto de los artistas. Esto puede deberse a su amplio catálogo, 
    reediciones y múltiples versiones de álbumes. Otros artistas como The Weeknd o Lana Del Rey 
    presentan cantidades más equilibradas pero muy por debajo del volumen de Swift.""",

    "graf3": """Los álbumes completos contienen la mayor cantidad de canciones (más de 5800 registros), 
    confirmando que este formato sigue siendo el principal generador de contenido. Los singles representan 
    un volumen importante pero menor, mientras que las compilaciones son las menos frecuentes dentro del dataset.""",

    "graf4": """La gráfica muestra una tendencia creciente en el número de canciones lanzadas por año, 
    especialmente a partir de 2017. Se destaca un incremento fuerte en 2024 y un récord en 2025, 
    lo cual coincide con la proliferación del streaming y la facilidad para distribuir música globalmente.""",

    "graf5": """EEl álbum Nevermind (Super Deluxe Edition) encabeza la lista con 70 canciones, muy por encima 
    de los demás. Esto demuestra que las ediciones deluxe o ampliadas influyen mucho en el conteo de pistas. 
    Otros álbumes como Reputation Stadium Tour Surprise Song Playlist también destacan por estrategias modernas 
    de reediciones y versiones extendidas.""",

    "graf6": """El gráfico revela que solo el 25% de las canciones son explícitas, mientras que el 75% no contienen 
    contenido sensible. Esto indica que el dataset se inclina hacia música apta para todo público, especialmente 
    géneros como pop, folk o soundtrack, aunque géneros urbanos suelen aumentar la proporción explícita.""",

    "graf7": """La gráfica evidencia una estacionalidad marcada: enero es el mes con más lanzamientos, superando 
    los 1100 registros. Meses como junio, octubre y noviembre muestran picos importantes, lo que sugiere ciclos 
    comerciales asociados a temporadas de consumo, festividades o estrategias de lanzamiento anual.""",

    "graf8": """El scatter demuestra que la duración de la canción no está fuertemente relacionada con la popularidad. 
    La mayoría de los valores se concentran entre 2 y 5 minutos, sin tendencia clara. Las canciones explícitas 
    presentan una popularidad ligeramente mayor, como se confirma en los boxplots correspondientes.""",

    "graf9": """Los boxplots muestran que las canciones de álbumes completos mantienen una popularidad más consistente 
    y relativamente alta. Los singles presentan mayor variabilidad—pueden ser muy exitosos o muy poco escuchados—mientras 
    que las compilaciones suelen mostrar una popularidad más baja y menos dispersa.""",

    "graf10": """El análisis muestra que géneros como pop soul, corridos/música mexicana y alternative R&B presentan 
    las popularidades promedio más altas. Esto refleja una fuerte aceptación del público hacia estilos vocales, 
    melódicos y con presencia mediática significativa dentro del dataset."""
}


# ========= OBJETIVO (VERSIÓN REDUCIDA) =========

objetivo_general = """
Este dashboard presenta 10 visualizaciones interactivas creadas con Plotly 
para analizar un dataset musical de Kaggle. Explora tendencias, géneros, 
popularidad y patrones de lanzamiento seleccionando cualquiera de las gráficas 
desde el menú superior.
"""


# ==========================================================
#                CONFIGURACIÓN DE DASHBOARD
# ==========================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.COSMO]   # Fondo claro elegante
)

app.title = "Dashboard Plotly – Selección de Gráficas"


# ==========================================================
#                      OPCIONES DEL DROPDOWN
# ==========================================================

graf_options = [
    {"label": grafs_dict[g]["title"], "value": g}
    for g in grafs_dict
]


# ==========================================================
#                    LAYOUT PRINCIPAL
# ==========================================================

app.layout = dbc.Container(
    [
        html.Br(),

        # ------------------- ENCABEZADO EN RECUADRO -------------------
        html.Div(
            html.H1(
                "Dashboard Interactivo – Plotly",
                className="text-center",
                style={"color": "white", "margin": "0"}
            ),
            style={
                "backgroundColor": "#1AA6B7",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 10px rgba(0,0,0,0.3)"
            },
            className="mb-4"
        ),

        # ------------------- DROPDOWN -------------------
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="graf-selector",
                        options=graf_options,
                        value=None,                      # Sin selección inicial
                        placeholder="Selecciona una gráfica...",
                        clearable=True,
                        className="mb-4"
                    ),
                    width=6
                )
            ],
            justify="center"
        ),

        # ------------------- TÍTULO -------------------
        html.H3(id="graf-title", className="text-center mt-3"),

        # ------------------- GRÁFICA -------------------
        dcc.Graph(
            id="graf-placeholder",
            style={"height": "600px", "display": "none"}  # Oculto inicialmente
        ),

        # ------------------- DESCRIPCIÓN -------------------
        html.Div(
            id="graf-description",
            className="mt-4 p-3",
            style={
                "backgroundColor": "#ffffff",
                "borderRadius": "10px",
                "border": "1px solid #ddd",
                "fontSize": "18px",
                "lineHeight": "1.5",
                "color": "black",
                "maxWidth": "900px",
                "margin": "0 auto"
            }
        ),

        html.Br()
    ],
    fluid=True
)


# ==========================================================
#                     CALLBACK PRINCIPAL
# ==========================================================

@app.callback(
    [
        Output("graf-title", "children"),
        Output("graf-placeholder", "figure"),
        Output("graf-placeholder", "style"),
        Output("graf-description", "children")
    ],
    [Input("graf-selector", "value")]
)
def update_graph(selected_graf):

    # --- CUANDO NO HAY SELECCIÓN ---
    if selected_graf is None:
        return (
            "Bienvenido al Dashboard Interactivo",
            {},                         # Figura vacía
            {"display": "none"},         # OCULTA la gráfica
            objetivo_general
        )

    # --- CUANDO SÍ HAY SELECCIÓN ---
    data = grafs_dict[selected_graf]
    title = data["title"]
    fig = data["figure"]
    description = descripciones.get(selected_graf, "Descripción no disponible.")

    return (
        title,
        fig,
        {"height": "600px", "display": "block"},   # Mostrar gráfica
        description
    )


# ==========================================================
#                        RUN SERVER
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True, port=8052)

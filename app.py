import dash
from dash import Dash, html, dcc
from dash import Dash, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
from dash_iconify import DashIconify

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.MINTY])


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "12rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H6("Maladies chroniques", style={'font-size' : '30px'}),
        html.Hr(),
        html.P(
            "Ce site vous permet d'estimer la prédisposition à certaines maladies (aucune donnée n'est collectée)", className="lead"
        ),
        dbc.Nav(
            [   dmc.NavLink("Acceuil", href="/",
                  label="Acceuil",
                  icon=DashIconify(icon="bi:house-door-fill", height=16, color="#c2c7d0")
                            ),
                dmc.NavLink("Cancer du sein", href="/sein",
                  label="Cancer",
                  icon=DashIconify(icon="healthicons:oncology-outline", height=16, color="#c2c7d0")
                            ),
                dmc.NavLink("Maladies cardiaques", href="/cardiaque",
                  label="Cardiaque",
                  icon=DashIconify(icon="pepicons-print:heart-filled", height=16, color="#c2c7d0")
                            ),
                dmc.NavLink("Diabète sucré", href="/diabetes",
                  label="Diabète",
                  icon=DashIconify(icon="game-icons:fat", height=16, color="#c2c7d0")
                            ),
                dmc.NavLink("Maladies chroniques des reins", href="/rein",
                  label="Rein",
                  icon=DashIconify(icon="healthicons:kidneys", height=16, color="#c2c7d0")
                            ),
                dmc.NavLink("Maladies chroniques du foie", href="/foie",
                  label="Foie",
                  icon=DashIconify(icon="game-icons:liver", height=16, color="#c2c7d0")
                            )
                
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


app.layout = dbc.Container([dbc.Col(sidebar), 
                            dbc.Col(dash.page_container, style=CONTENT_STYLE) ])




if __name__ == '__main__':
    app.run(debug=True)
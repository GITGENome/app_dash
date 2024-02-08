import dash
from dash import html, dcc, callback, Input, Output, State, dash_table, Dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from joblib import dump, load
import pandas as pd

dash.register_page(__name__,
    title='La page de cancer du sein',
    name='La page de cancer du sein',
    path="/sein")


df=pd.read_csv('sein_vizual.csv')

fig = px.box(df, y=df.drop(columns=['diagnosis', 'Unnamed: 0']).columns, 

             color="diagnosis", color_discrete_sequence=px.colors.qualitative.Dark24_r 
        )

fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           xaxis_showgrid=False, yaxis_showgrid=False)


concave_points_worst = dcc.Input(id='concave_points_worst', type="number",
                                       # min=0, max=0.35,  
                                        placeholder='0.0-0.35'
                                        )
concave_pop = dbc.Popover(
                        dbc.PopoverBody("La valeur moyenne la plus élevée du nombre de parties concaves du contour"),
                        target="concave_points_worst",
                        trigger="click",)
texture_worst = dcc.Input(id='texture_worst', type="number",
                                      #  min=12, max=50,  
                                        placeholder='12-50'
                                        )
texture_pop = dbc.Popover(
                        dbc.PopoverBody("La valeur moyenne la plus élevée de l'écart-type pour les valeurs en niveaux de gris"),
                        target="texture_worst",
                        trigger="click",)
perimeter_worst = dcc.Input(id='perimeter_worst', type="number",
                                      #  min=50, max=300,  
                                        placeholder='50-300'
                                        )
perimeter_pop = dbc.Popover(
                        dbc.PopoverBody("La valeur la plus élevée de la tumeur centrale"),
                        target="perimeter_worst",
                        trigger="click",)
area_se = dcc.Input(id='area_se', type="number",
                                      #  min=5, max=600,  
                                        placeholder='5-600'
                                        )
area_pop = dbc.Popover(
                        dbc.PopoverBody("L'erreur standard estimée des surfaces de cellules cancéreuses"),
                        target="area_se",
                        trigger="click",)

alert_resuit = dbc.Alert(
            "Vous n'êtes pas à risque",
            id="salert-success",
            dismissable=True,
            is_open=True, color="success"
        )
alert_fall = dbc.Alert(
            "Attention! Vous êtes à risque",
            id="salert-attention",
            dismissable=True,
            is_open=True, color="danger"
        )

city_drop = dcc.Dropdown(
                                id='sein_city',
                                options=[
                                    {'label': 'Bordeaux', 'value': 'bordeaux'},
                                    {'label': 'Lille', 'value': 'lille'},
                                    {'label': 'Lyon', 'value': 'lyon'},
                                    {'label': 'Paris', 'value': 'paris'},
                                    {'label': 'Nantes', 'value': 'nantes'},
                                    {'label': 'Toulouse', 'value': 'toulouse'}
                                    
                                ],
                                value='Bordeaux')
button_rdv = html.Div(
    [
        dbc.Button(
            "Prendre RDV",
            href='cardio_link',
            external_link=True,
            color="danger", size='lg',
            id='sein_rdv'
        ),
    ]
)
modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Attention")),
                dbc.ModalBody(dbc.Alert("Les prédictions fournies sont à titre INFORMATIVE et ne remplacent pas un diagnostic médical professionnel", color = 'warning')),
                dbc.ModalFooter(
                ),
            ],
            id="modal",
            is_open=True,
        ),
    ]
)

layout = dbc.Container([modal,
    html.H1('Cancer du sein', style={'textAlign': 'center', 'margin-bottom' : '50px'}),
                        html.Div([html.H3('Veuillez remplir le formulaire :', style={'textAlign': 'center'}),
                                  dbc.Row([dbc.Col([html.H6('Moyenne des plus grands points concaves'),
                                                  concave_points_worst, concave_pop
                                                    ]),
                                           dbc.Col([html.H6('Déviation de la texture la plus grande'),
                                                    texture_worst, texture_pop]),
                                           dbc.Col([html.H6('Périmetre le plus haut'),
                                                    perimeter_worst, perimeter_pop])]), 
                                  dbc.Row([dbc.Col(),
                                           dbc.Col([html.H6('Ecart-type des surfaces'),
                                                    area_se, area_pop]),
                                           dbc.Col()])
                                  ], style={"background-color" : 'LightGray', "color":"black", "border-radius": "15px", "padding" : '25px'}),
                        html.H2("Votre risque d'avoir le cancer du sein maligne", style={'textAlign': 'center',  'margin-top' : '50px'}),
                        
                        dbc.Row(alert_resuit),
                        dbc.Row(alert_fall),
                        
                        html.Div([dbc.Row(dcc.Graph(id='sein_risk'))]),
                        dbc.Row(html.H6('Choisissez votre ville pour prendre RDV chez le spécialiste', style={'margin-bottom' : '10px'})),
                        dbc.Row([dbc.Col(city_drop, width=3),
                                dbc.Col()], style={'margin-bottom' : '10px'}),                                                                                             
                        dbc.Row(button_rdv),
                        html.H2('Le science derrière la prédiction', style={'textAlign': 'center',  'margin-top' : '50px'}),

                        html.Div([dbc.Row([dbc.Col(html.H6("""La corrélation entre les caractéristiques est claire, précise et élevée.
                                                           Plusieurs caractéristiques de cellules montrent une distribution très claire pour le malin et le bénin.
                                                           L'utilisation de caractéristiques distinctives permet d'obtenir un score de prédiction pour le type de tumeur de 0,98""")
                                    , style={'margin-top' : '70px'}),
                                          dbc.Col(dcc.Graph(figure=fig), style={'flex':6})]),
                                  dbc.Row()]),
                        html.H3('Bibliographie',style={'textAlign': 'center',  'margin-top' : '50px'}),
                        html.Div([
                            dbc.ListGroup([
                                dbc.ListGroupItem("Street, W.N., Wolberg, W.H., Mangasarian, O.L., 1993. Nuclear feature extraction for breast tumor diagnosis, in: Acharya, R.S., Goldgof, D.B. (Eds.), . Presented at the IS&T/SPIE’s Symposium on Electronic Imaging: Science and Technology, San Jose, CA, pp. 861–870. https://doi.org/10.1117/12.148698", href="https://www.researchgate.net/publication/2512520_Nuclear_Feature_Extraction_For_Breast_Tumor_Diagnosis")
                            ])])                           
])


@callback(Output('sein_risk', 'figure'),
          Output("salert-attention", "is_open"),
          Output('salert-success', 'is_open'),
          Output('sein_rdv', 'href'),
          [Input('concave_points_worst', 'value'),
           Input('texture_worst', 'value'),
           Input('perimeter_worst', 'value'),
           Input('area_se', 'value'),
           Input('sein_city', 'value')
           ],
           [State("salert-attention", "is_open" ),
            State('salert-success', 'is_open')])
def on_button_click(concave, texture_worst, perimeter_worst, area_se, city, is_open1, is_open2):
    responses = {'perimeter_worst' : perimeter_worst or 0, 
                  'texture_worst' : texture_worst or 0,
                  'concave points_worst' : concave or 0,
                  'area_se' : area_se or 0
                }
    model_sein = load('regression_model_saved_sein.joblib')
    X_patient = pd.DataFrame(responses.values(), responses.keys()).T
    
    proba = model_sein.predict_proba(X_patient)[0][1]*100
    
    
    fig = go.Figure(go.Indicator(
            domain = {'x': [0, 1], 'y': [0, 1]},
            value = proba,
            mode = "gauge+number",
            title = {'text': "Probabilité (en %) d'avoir un cancer du sein maligne"},
            gauge = {'axis': {'range': [0, 100], 'tickcolor': "darkblue"},
                    'bar': {'color': "black"},
                    'steps' : [
                        {'range': [0, 30], 'color': "#E4F3EF"},
                        {'range': [30, 60], 'color': "#FFF5E1"},
                        {'range': [60, 100], 'color': "#FFE4DC"}]}))
    
    if proba>=50:
        is_open1=True
        is_open2=False
    if proba<50:
        is_open1=False
        is_open2=True    
    if 0<proba<20:
        is_open2=True
    if concave is None or texture_worst is None or perimeter_worst is None or area_se is None:
        is_open2=False

    link = 'https://www.doctolib.fr/oncologue-medical/'+ city

    return fig, is_open1, is_open2, link
import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd 
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from joblib import dump, load
import numpy as np

dash.register_page(__name__, path='/foie')

Model_foie = load("foie_model_saved.joblib")

df_feature = pd.read_csv('feature_importance_foie.csv')

fig_importance = px.bar(df_feature.sort_values('Importance', ascending=False), x='Feature', y='Importance', 
                        color='Importance', color_continuous_scale='tealrose_r')

fig_importance.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis_showgrid=False, yaxis_showgrid=False)
fig_importance.update_traces(textposition="outside", 
                              marker_line_color='rgb(8,48,107)',
                              marker_line_width=1.5, opacity=0.6)

slider_foie_age = dcc.Slider(10,
                        100,
                        1,
                        value = 50,
                        marks = None,
                        tooltip={"placement": "bottom", 
                                 "always_visible": True},
                        id='foie_age')

dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown')

input_foie_gender = dcc.Dropdown(options=[
                                    {'label': 'Homme', 'value': 'Male'},
                                    {'label': 'Femme', 'value': 'Female'}
                                ],id = "foie_gender")
                                


input_foie_total_bilirubin = dcc.Input(
                              type='number',
                              id='foie_total_bilirubin')

input_foie_alkaline_phosphotase = dcc.Input(
                              type='number',
                              id='foie_alkaline_phosphotase')

input_foie_alamine_aminotransferase = dcc.Input(
                              type='number',
                              id='foie_alamine_aminotransferase')

input_foie_albumin = dcc.Input(
                              type='number',
                              id='foie_albumin')

input_foie_albumin_globulin = dcc.Input(
                              type='number',
                              id='foie_albumin_globulin')

city_drop = dcc.Dropdown(
                                id='foie_city',
                                options=[
                                    {'label': 'Bordeaux', 'value': 'bordeaux'},
                                    {'label': 'Lille', 'value': 'lille'},
                                    {'label': 'Lyon', 'value': 'lyon'},
                                    {'label': 'Paris', 'value': 'paris'},
                                    {'label': 'Nantes', 'value': 'nantes'},
                                    {'label': 'Toulouse', 'value': 'toulouse'}
                                    
                                ],
                                value='bordeaux')

foie_fig = go.Figure(go.Indicator(
                domain = {'x': [0, 1], 'y': [0, 1]},
                value = 0,
                mode = "gauge+number",
                title = {'text': "Taux de risque"},
                delta = {'reference': 0.5},
                gauge = {'axis': {'range': [0, 1], 'tickcolor': "darkblue"},
                                'bar': {'color': "black"},
                                'steps' : [
                                {'range': [0, 0.3], 'color': "lightgreen"},
                                {'range': [0.3, 0.6], 'color': "yellow"},
                                {'range': [0.6, 1], 'color': "red"}]}))

alert_resuit = dbc.Alert(
            "Vous n'etes pas à risque",
            id="foie_alert-success",
            dismissable=True,
            is_open=False, color="success")

alert_fall = dbc.Alert(
            "Attention! Vous etes à risque",
            id="foie_alert-attention",
            dismissable=True,
            is_open=False, color="danger")

button_rdv_foie = html.Div(
    [
        dbc.Button(
            "Prendre RDV",
            href='foie_link',
            external_link=True,
            color="danger", size='lg',
            id='foie_rdv'
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

##################
# DEBUT DU LAYOUT
##################

layout = html.Div([modal,
                      
                        html.H1('Maladie du foie', style={'textAlign': 'center', 'margin-bottom' : '50px'}),
                        html.Div([  
                                html.H3("Veuillez remplir le formulaire :  ", style={'textAlign': 'center'}),
                                html.Div([
                                        "Choisissez votre âge : ",
                                        slider_foie_age 
                                        ]),
                                html.Br(),

                                html.Div([
                                        dbc.Row([
                                                dbc.Col([
                                                        html.Div("Indiquez le genre : "),
                                                        input_foie_gender
                                                        ]),
                                                dbc.Col([
                                                        html.Div("Indiquez le taux d\'alamine aminotransferase: "),
                                                        input_foie_alamine_aminotransferase,
                                                        dbc.Tooltip("Taux sain : 10 - 40 (U/L)",
                                                                target = 'foie_alamine_aminotransferase',
                                                                placement = 'right'
                                                                )
                                                        ]),
                                                dbc.Col([
                                                        html.Div("Indiquez le taux d'alkaline phosphotase : "),
                                                        input_foie_alkaline_phosphotase,
                                                        dbc.Tooltip("Taux sain : 30 - 125 (U/L)",
                                                                target = 'foie_alkaline_phosphotase',
                                                                placement = 'right'
                                                                )
                                                        ])
                                                ]),
                                        
                                html.Br(),
                                html.Div([
                                        dbc.Row([
                                                dbc.Col([
                                                        html.Div("Indiquez le taux d\'albumin: "),
                                                        input_foie_albumin,
                                                        dbc.Tooltip("Taux sain : 3.4 - 5.4 (g/dL)",
                                                                target = 'foie_albumin',
                                                                placement = 'right'
                                                                )
                                                        ]),
                                                dbc.Col([
                                                        html.Div("Indiquez le taux de bilirubine : "),
                                                        input_foie_total_bilirubin,
                                                        dbc.Tooltip("Taux sain : 0.3 - 1.9 (mg/dL)",
                                                                target = 'foie_total_bilirubin',
                                                                placement = 'right'
                                                                )
                                                        ]),
                                                dbc.Col([html.Div('Indiquez le ratio album/globulin :'),
                                                         input_foie_albumin_globulin,
                                                        dbc.Tooltip("Taux sain : 1.1-2.5",
                                                                target = 'foie_albumin_globulin',
                                                                placement = 'right'
                                                                )
                                                        ])])
                                                ])
                                        
                                        ]),
                                ],style={"background-color" : 'LightGray', "color":"black", "border-radius": "15px", "padding" : '25px'}),
                                html.Br(), 
                                html.H2("Votre predisposition aux maladies chroniques du foie", style={'textAlign': 'center',  'margin-top' : '50px'}),

                                html.Div([alert_resuit,
                                          alert_fall,
                                        dcc.Graph(id="foie_fig")       
                                ]),
                        html.Br(),
                        dbc.Row(html.H6('Choisissez votre ville pour prendre RDV chez le spécialiste', style={'margin-bottom' : '10px'})),
                        dbc.Col(city_drop,width=3, style={'margin-bottom' : '10px'}),
                        dbc.Row(button_rdv_foie),
                        html.H2('Le science derrière la prédiction', style={'textAlign': 'center',  'margin-top' : '50px'}),
                        html.Div([dbc.Row([dbc.Col(html.H6("""Il existe plusieurs variables liées à la maladie chronique du foie. Le modèle de prédiction a été 
                                                           sélectionné parmi 5 modèles de machine learning différents. Ce modèle a été amélioré en combinant les 
                                                           réponses de 3 modèles pour atteindre un score supérieur à 0,75. Dans notre modèle, certaines variables sont plus
                                                            corrélées que d'autres. Le graphique nous montre les variables les plus importantes ; celles qui se trouvent en tête 
                                                           sont l'alanine aminotransférase et la phosphatase alcaline. Lorsque le foie est touché, ces enzymes qui restent habituellement
                                                            dans le foie sont parfois libérées dans le sang.                                                           
                                                            """)
                                     , style={'margin-top' : '70px'}),
                                         dbc.Col(dcc.Graph(figure=fig_importance), style={'flex':2})]),
                                   dbc.Row()]),
                        html.H3('Bibliographie',style={'textAlign': 'center',  'margin-top' : '50px'}),
                        html.Div([
                            dbc.ListGroup([
                                dbc.ListGroupItem("Liu Y, Méric G, Havulinna AS, Teo SM, Åberg F, Ruuskanen M, Sanders J, Zhu Q, Tripathi A, Verspoor K, Cheng S, Jain M, Jousilahti P, Vázquez-Baeza Y, Loomba R, Lahti L, Niiranen T, Salomaa V, Knight R, Inouye M. Early prediction of incident liver disease using conventional risk factors and gut-microbiome-augmented gradient boosting. Cell Metab. 2022 May 3;34(5):719-730.e4. doi: 10.1016/j.cmet.2022.03.002", href="https://pubmed.ncbi.nlm.nih.gov/35354069/"),
                                dbc.ListGroupItem("Lala V, Zubair M, Minter DA. Liver Function Tests. [Updated 2023 Jul 30]. In: StatPearls. Treasure Island (FL): StatPearls Publishing; 2023 Jan", href="https://www.ncbi.nlm.nih.gov/books/NBK482489/"),
                                dbc.ListGroupItem("Xu L, Yuan Y, Che Z, Tan X, Wu B, Wang C, Xu C, Xiao J. The Hepatoprotective and Hepatotoxic Roles of Sex and Sex-Related Hormones. Front Immunol. 2022 Jul 4;13:939631. doi: 10.3389/fimmu.2022.939631", href="https://pubmed.ncbi.nlm.nih.gov/35860276/"),
                                dbc.ListGroupItem("Zhang J, Wang T, Fang Y, Wang M, Liu W, Zhao J, Wang B, Wu Z, Lv Y, Wu R. Clinical Significance of Serum Albumin/Globulin Ratio in Patients With Pyogenic Liver Abscess. Front Surg. 2021 Nov 30;8:677799. doi: 10.3389/fsurg.2021.677799.", href="https://pubmed.ncbi.nlm.nih.gov/34917645/")
                            ])])  
                        ])

@callback(
    Output('foie_fig', 'figure'),
    Output("foie_alert-attention", "is_open"),
    Output('foie_alert-success', 'is_open'),
    Output('foie_rdv', 'href'),

    [Input("foie_age", "value"),
     Input("foie_gender", "value"),
     Input('foie_total_bilirubin', 'value'),
     Input('foie_alkaline_phosphotase', 'value'),
     Input('foie_alamine_aminotransferase', 'value'),
     Input('foie_albumin', 'value'),
     Input('foie_albumin_globulin', 'value'),
     Input('foie_city', 'value')
     ],
     [State("foie_alert-attention", "is_open" ),
      State('foie_alert-success', 'is_open')]
)

def foie(foie_age, foie_gender, foie_total_bilirubin, foie_alkaline_phosphotase, foie_alamine_aminotransferase, foie_albumin, foie_albumin_globulin , city, is_open1, is_open2):
        dico_foie = {"Age":foie_age or 0,
                 "Gender":foie_gender or 'Male',
                 "Total_Bilirubin":foie_total_bilirubin or 0,
                 "Alkaline_Phosphotase":foie_alkaline_phosphotase or 0,
                 "Alamine_Aminotransferase":foie_alamine_aminotransferase or 0,
                 "Albumin" : foie_albumin or 0,
                 "Albumin_and_Globulin_Ratio":foie_albumin_globulin or 0,     
                 }
    
        X_patient = pd.DataFrame(dico_foie.values(), dico_foie.keys()).T
        proba = Model_foie.predict_proba(X_patient)[0][0]*100

        if proba>=50 and dico_foie["Albumin_and_Globulin_Ratio"]!=0:
                is_open1=True
                is_open2=False
        elif proba<50:
                is_open1=False
                is_open2=True    
        if 0<proba<=30:
                is_open2=True
        if dico_foie["Albumin_and_Globulin_Ratio"]==0:
                is_open2=False
                is_open1=False
                

        fig_foie = go.Figure(go.Indicator(
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        value = proba,
                        mode = "gauge+number",
                        title = {'text': "Probabilité (en %) d'avoir une maladie du foie"},
                        delta = {'reference': 0.5},
                        gauge = {'axis': {'range': [0, 100], 'tickcolor': "darkblue"},
                                        'bar': {'color': "black"},
                                        'steps' : [
                                                {'range': [0, 30], 'color': "#E4F3EF"},
                                                {'range': [30, 60], 'color': "#FFF5E1"},
                                                {'range': [60, 100], 'color': "#FFE4DC"}]}))
        
        link = "https://www.doctolib.fr/hepatologue/"+city,
        
        return fig_foie, is_open1, is_open2, link





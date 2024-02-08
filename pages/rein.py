import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd 
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from joblib import dump, load
import plotly.express as px


dash.register_page(__name__, path='/rein')

Model_rein = load("renale_model_saved.joblib")

df_coef_rein = pd.read_csv("rein_distribution" )
fig_importance = px.scatter_3d(df_coef_rein, x = "0",
                                y = "1",
                                z = "2",
                                color = "3",
                                color_discrete_sequence=px.colors.qualitative.Pastel,
                                labels={"3" : "Malade"}
                    ) 





########################
# DECLARATION DES INPUTS
########################

slider_rein_age = dcc.Slider(10,
                        100,
                        1,
                        value = 50,
                        marks = None,
                        tooltip={"placement": "bottom", 
                                 "always_visible": True},
                        id='rein_age')

input_rein_bp  = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_blood_pressure')

input_rein_sg = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_specific_gravity')

input_rein_al = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_albumin')

input_rein_su = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_sugar')

input_rein_bgr = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_blood_glucose_random')

input_rein_bu = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_blood_urea')

input_rein_sc = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_serum_creatinine')

input_rein_sod = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_sodium')

input_rein_pot = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_potassium')

input_rein_pcv = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_packed_cell_volume')

input_rein_wc = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_white_blood')

input_rein_rc = dcc.Input(placeholder = '',min=0,
                              type='number',
                              value='',
                              id='rein_red_blood')

alert_resuit = dbc.Alert(
            "Vous n'etes pas à risque",
            id="rein_calert-success",
            dismissable=True,
            is_open=False, color="success")

alert_fall = dbc.Alert(
            "Attention! Vous etes à risque",
            id="rein_calert-attention",
            dismissable=True,
            is_open=False, color="danger")

button_rdv_rein = html.Div(
    [
        dbc.Button(
            "Prendre RDV",
            href='rein_link',
            external_link=True,
            color="danger", size='lg',
            id='rein_rdv'
        ),
    ]
)

city_drop = dcc.Dropdown(
                                id='rein_city',
                                options=[
                                    {'label': 'Bordeaux', 'value': 'bordeaux'},
                                    {'label': 'Lille', 'value': 'lille'},
                                    {'label': 'Lyon', 'value': 'lyon'},
                                    {'label': 'Paris', 'value': 'paris'},
                                    {'label': 'Nantes', 'value': 'nantes'},
                                    {'label': 'Toulouse', 'value': 'toulouse'}
                                    
                                ],
                                value='bordeaux')

rein_fig = go.Figure(go.Indicator(
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
                        
                        html.H1('Maladie rénale',  style={'textAlign': 'center', 'margin-bottom' : '50px'}),
                        html.Div([
                                html.H3("Veuillez remplir le formulaire : ", style={'textAlign': 'center'}),
                                html.Div([
                                        "Choisissez votre âge : ",
                                        slider_rein_age 
                                        ]),

                                html.Br(),
                                html.Div([
                                        dbc.Row([
                                        dbc.Col([
                                                html.Div("Indiquez la pression sanguine (mmHg): "),
                                                input_rein_bp,
                                                dbc.Tooltip("Taux sain :  < 140/90 mmHG",
                                                        target = 'rein_blood_pressure',
                                                        placement = 'right'
                                                        ),                                                
                                                ]),
                                        dbc.Col([
                                                html.Div("Indiquez la densité urinaire : "),
                                                input_rein_sg,
                                                dbc.Tooltip("taux sain : 1,005 - 1,030",
                                                                target = 'rein_specific_gravity',
                                                                placement = 'right'
                                                                ),
                                                ]),
                                        dbc.Col([
                                                html.Div("Indiquez le taux d'albumine (mmol/L) : "),
                                                input_rein_al,
                                                dbc.Tooltip("Taux sain : 0,51 - 1,030 (mmol/L)",
                                                                target = 'rein_albumin',
                                                                placement = 'right'
                                                                ),
                                                ])
                                                ])
                                        ]),
                                html.Br(),
                                html.Div([
                                        dbc.Row([
                                        dbc.Col([
                                                html.Div("Indiquez le taux de sucre dans l'urine (mg/dL): "),
                                                input_rein_su,
                                                dbc.Tooltip("Taux sain : < 15 (mg/dL)",
                                                                target = 'rein_sugar',
                                                                placement = 'right'
                                                                ),
                                                ]),
                                        dbc.Col([
                                                html.Div("Indiquez le taux de sucre aleatoire dans le sang (mg/dL) : "),
                                                input_rein_bgr,
                                                dbc.Tooltip("Taux sain : 70 - 180 (mg/dL)",
                                                                target = 'rein_blood_glucose_random',
                                                                placement = 'right'
                                                                ),
                                                ]),
                                        dbc.Col([
                                                html.Div("Indiquez le taux d'urée sanguine (g/L) : "),
                                                input_rein_bu,
                                                dbc.Tooltip("Taux sain : 0,18 - 0,45 (g/L)",
                                                                target = 'rein_blood_urea',
                                                                placement = 'right'
                                                                ),
                                                ])
                                                ])
                                        ]),

                                html.Br(),
                                html.Div([
                                        dbc.Row([
                                        dbc.Col([
                                                html.Div("Indiquez le taux de créatinine sérique (mmol/L) : "),
                                                input_rein_sc,
                                                dbc.Tooltip("Taux sain : 2,5 - 8,2 (mmol/L)",
                                                                target = 'rein_serum_creatinine',
                                                                placement = 'right'
                                                                ),
                                                ]),
                                        dbc.Col([
                                                html.Div("Indiquez le taux de sodium (mEq/L) : "),
                                                input_rein_sod,
                                                dbc.Tooltip("Taux sain : 136 - 145 (mEq/L)",
                                                                target = 'rein_sodium',
                                                                placement = 'right'
                                                                ),
                                                ]),
                                        dbc.Col([
                                                html.Div("Indiquez le taux de potassium (mEq/L) : "),
                                                input_rein_pot,
                                                dbc.Tooltip("Taux sain : 3,5 - 5,1 (mEq/L)",
                                                                target = 'rein_potassium',
                                                                placement = 'right'
                                                                ),
                                                ])
                                                ])
                                        ]),
                                html.Br(),
                                html.Div([
                                        dbc.Row([
                                        dbc.Col([
                                                html.Div("Indiquez le volume globulaire (hématocrite) : "),
                                                input_rein_pcv,
                                                dbc.Tooltip("Taux sain : 35-49 %",
                                                                target = 'rein_packed_cell_volume',
                                                                placement = 'right'
                                                                ),
                                                ]),
                                        dbc.Col([
                                                html.Div("Indiquez le nombre de globules blancs : "),
                                                input_rein_wc,
                                                dbc.Tooltip("Taux sain : 4000 - 10000 (/mm3)",
                                                                target = 'rein_white_blood',
                                                                placement = 'right'
                                                                ),
                                                ]),
                                        dbc.Col([
                                                html.Div("Indiquez le nombre de globules rouges (M/µL) : "),
                                                input_rein_rc,
                                                dbc.Tooltip("Taux sain : 4.1 - 5.6 (M/µL)",
                                                                target = 'rein_red_blood',
                                                                placement = 'right'
                                                                ),
                                                ])
                                                ])
                                        ]),
                                ], style={"background-color" : 'LightGray', "color":"black", "border-radius": "15px", "padding" : '25px'}),
                        html.Br(),
                        html.H2("Votre prédisposition aux maladies chroniques des reins", style={'textAlign': 'center',  'margin-top' : '50px'}),
                        html.Div([
                                        dbc.Row(alert_resuit),
                                        dbc.Row(alert_fall),        
                                ]),
                        html.Br(),
                        html.Div([
                                        dcc.Graph(id = "rein_fig", figure =  rein_fig)       
                                ]),
                        html.Br(),

                        dbc.Row(html.H6('Choisissez votre ville pour prendre RDV chez le spécialiste', style={'margin-bottom' : '10px'})),
                        dbc.Row([dbc.Col(city_drop, width=3),
                                dbc.Col()], style={'margin-bottom' : '10px'}),                                                                                             
                        dbc.Row(button_rdv_rein),
                        html.Br(),
                        html.H3('Prédiction derrière la science', style={'textAlign': 'center'}),
                        dbc.Row([
                            dbc.Col([
                                html.P("""
                                      Il existe plusieurs variables qui sont liées à la maldie rénale chronique, elle même liée a des maladies comme le diabète et l'hypertension. Le modèle de prédiction à été selectionné parmi 5 modèles de machine learning différents. Ce modèle a été amélioré, ce  qui nous permet d'obtenir un score de prédiction de maladie proche de 0.9.
                                        Dans notre modèle, certaines variables sont plus corrélées que d'autres. Le graphique montre que parmi les variables les plus importantes se trouve en tête le taux d'albumine, le volume de cellules groupées et la densité urinaire. Lorsque les reins sont sain, ils filtrent l'albumine et on retrouve un fable taux de celle-ci dans les urines. Lorsque les reins sont endommagés, ils filtrent moins bien et laisse donc passer de l'albumine.  
                                   """)
                            ]),                            
                            dbc.Col(dcc.Graph(figure=fig_importance), style={'flex' : 2}),                            
                        ]),
                html.H3('Bibliographie',style={'textAlign': 'center',  'margin-top' : '50px'}),
                html.Div([
                        dbc.ListGroup([
                                dbc.ListGroupItem("Cruz, D.N., Goh, C.Y., Haase‐Fielitz, A., Ronco, C., Haase, M., 2010. Early Biomarkers of Renal Injury. Congest. Heart Fail. 16. https://doi.org/10.1111/j.1751-7133.2010.00163.x", href="https://pubmed.ncbi.nlm.nih.gov/20653708/"),
                                dbc.ListGroupItem("Coresh, J., Wei, G.L., McQuillan, G., Brancati, F.L., Levey, A.S., Jones, C., Klag, M.J., 2001. Prevalence of High Blood Pressure and Elevated Serum Creatinine Level in the United States: Findings From the Third National Health and Nutrition Examination Survey (1988-1994). Arch. Intern. Med. 161, 1207. https://doi.org/10.1001/archinte.161.9.1207", href="https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/648077"),
                                dbc.ListGroupItem("Raymond Vanholder, Tessa Gryp, Griet Glorieux, Urea and chronic kidney disease: the comeback of the century? (in uraemia research), Nephrology Dialysis Transplantation, Volume 33, Issue 1, January 2018, Pages 4–12, https://doi.org/10.1093/ndt/gfx039", href="https://pubmed.ncbi.nlm.nih.gov/28407121/"),
                                dbc.ListGroupItem("Kwon, Y.E., Oh, D.-J., Kim, M.J., Choi, H.M., 2020. Prevalence and Clinical Characteristics of Asymptomatic Pyuria in Chronic Kidney Disease. Ann. Lab. Med. 40, 238–244. https://doi.org/10.3343/alm.2020.40.3.238", href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6933061/"),
                                dbc.ListGroupItem("Kuwabara, M., Hisatome, I., Roncal-Jimenez, C.A., Niwa, K., Andres-Hernando, A., Jensen, T., Bjornstad, P., Milagres, T., Cicerchi, C., Song, Z., Garcia, G., Sánchez-Lozada, L.G., Ohno, M., Lanaspa, M.A., Johnson, R.J., 2017. Increased Serum Sodium and Serum Osmolarity Are Independent Risk Factors for Developing Chronic Kidney Disease; 5 Year Cohort Study. PLOS ONE 12, e0169137. https://doi.org/10.1371/journal.pone.0169137", href="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0169137"),
                                dbc.ListGroupItem("Nickolas, T.L., Barasch, J., Devarajan, P., 2008. Biomarkers in acute and chronic kidney disease. Curr. Opin. Nephrol. Hypertens. 17, 127–132. https://doi.org/10.1097/MNH.0b013e3282f4e525", href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7879424/"),
                                dbc.ListGroupItem("Elliott, J. (2023). Therapeutics of managing reduced red cell mass associated with chronic kidney disease – Is there a case for earlier intervention? Journal of Veterinary Pharmacology and Therapeutics, 46, 145–157. https://doi.org/10.1111/jvp.13127", href="https://pubmed.ncbi.nlm.nih.gov/37036059/"),
                                dbc.ListGroupItem("Warrens H, Banerjee D, Herzog CA. Cardiovascular Complications of Chronic Kidney Disease: An Introduction. Eur Cardiol. 2022 May 13;17:e13. doi: 10.15420/ecr.2021.54. PMID: 35620357; PMCID: PMC9127633.", href="https://pubmed.ncbi.nlm.nih.gov/35620357/"),
                                dbc.ListGroupItem("Takase, H., Kawakatsu, N., Hayashi, K. et al. Urinary Na/K ratio is a predictor of developing chronic kidney disease in the general population. Hypertens Res 47, 225–232 (2024). https://doi.org/10.1038/s41440-023-01399-4", href="https://www.nature.com/articles/s41440-023-01399-4"),
                                dbc.ListGroupItem("Shaikh H, Hashmi MF, Aeddula NR. Anemia of Chronic Renal Disease. [Updated 2023 Feb 24]. In: StatPearls. Treasure Island (FL): StatPearls Publishing; 2023 Jan", href="https://www.ncbi.nlm.nih.gov/books/NBK539871/")
                ])])
                        ])

@callback(
    Output('rein_fig', 'figure'),
    Output("rein_calert-attention", "is_open"),
    Output('rein_calert-success', 'is_open'),
    Output('rein_rdv', 'href'),

    [Input("rein_age", "value"),
     Input('rein_blood_pressure', 'value'),
     Input('rein_specific_gravity', 'value'),
     Input('rein_albumin', 'value'),
     Input('rein_sugar', 'value'),
     Input('rein_blood_glucose_random', 'value'),
     Input('rein_blood_urea', 'value'),
     Input('rein_serum_creatinine', 'value'),
     Input('rein_sodium', 'value'),
     Input('rein_potassium', 'value'),
     Input('rein_packed_cell_volume', 'value'),
     Input('rein_white_blood', 'value'),
     Input('rein_red_blood', 'value'),
     Input('rein_city', 'value')
     ],
     [State("rein_calert-attention", "is_open" ),
      State('rein_calert-success', 'is_open')]
)

def rein(rein_age, rein_blood_pressure, rein_specific_gravity, rein_albumin, rein_sugar, rein_blood_glucose_random, rein_blood_urea, rein_serum_creatinine,rein_sodium, rein_potassium, rein_packed_cell_volume, rein_white_blood, rein_red_blood, city, is_open1, is_open2):

    responses = {'age' : rein_age or 0, 'bp': rein_blood_pressure or 0, 'sg' : rein_specific_gravity or 0,
                'al' : rein_albumin or 0, 'su' : rein_sugar or 0,
                'bgr' : rein_blood_glucose_random or 0, 'bu' : rein_blood_urea or 0,
                'sc' : rein_serum_creatinine or 0, 'sod' : rein_sodium or 0,
                'pot' : rein_potassium or 0, 'pcv' : rein_packed_cell_volume or 0,
                'wc' : rein_white_blood or 0, 'rc' : rein_red_blood or 0}

    X_patient = pd.DataFrame(responses.values(), responses.keys()).T
    proba = Model_rein.predict_proba(X_patient)[0][0]*100
#     non_empty_inputs = [value for value in responses.values() if value != 0 ]

#     if len(non_empty_inputs) == 11 :
        
#         if proba>=50:
#             is_open1=True
#             is_open2=False
#         if proba<50:
#             is_open1=False
#         if proba<20 and proba >0:
#             is_open2=True
#     else:
#         proba = 0
#         is_open1 = False
#         is_open2 = False
    
    rein_fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = proba,
    mode = "gauge+number",
    title = {'text': "Probabilité (en %) d'avoir une maladie renale"},
    delta = {'reference': 0.5},
    gauge = {'axis': {'range': [0, 100], 'tickcolor': "darkblue"},
                    'bar': {'color': "black"},
                    'steps' : [
                        {'range': [0, 30], 'color': "#E4F3EF"},
                        {'range': [30, 60], 'color': "#FFF5E1"},
                        {'range': [60, 100], 'color': "#FFE4DC"}]}))
    

    link = "https://www.doctolib.fr/nephrologue/"+city,

    if proba>=50:
        is_open1=True
        is_open2=False
    if proba<50:
        is_open1=False
        is_open2=True    
    if 0<proba<20:
        is_open2=True
    if rein_age or rein_blood_pressure or rein_specific_gravity or rein_albumin or rein_sugar or rein_blood_glucose_random or rein_blood_urea or rein_serum_creatinine or rein_sodium or rein_potassium or rein_packed_cell_volume or  rein_white_blood or rein_red_blood is None:
        is_open2=False
    
    return rein_fig, is_open1, is_open2, link
import dash
from dash import html, dcc, callback, Input, Output, State, dash_table, Dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from joblib import dump, load

import pandas as pd

dash.register_page(__name__, path="/diabetes")
########################################## CSV et ML

df_imp= pd.read_csv('features_imp_diabet.csv')

model_rf = load('model_rf.joblib')



###########################################

slider_age = dcc.Slider(10,
                        100,
                        1,
                        value = 50,
                        marks = None,
                        tooltip={"placement": "bottom", 
                                 "always_visible": True},
                        id='diab_slider_age')

input_pregnancies = dcc.Input(placeholder = 'Nombre de grossesses',
                              type='number',
                              value='',
                              min = 0,
                              id='diab_input_preg')

input_glucose = dcc.Input(placeholder = 'Taux de glucose',
                              type='number',
                              value='',
                              min = 0,
                              id='diab_input_gluc')

input_insulin = dcc.Input(placeholder = 'Taux d\'insuline',
                              type='number',
                              value='',
                              min = 0,
                              id='diab_input_insu')

input_blood_p = dcc.Input(placeholder = 'Pression sanguine',
                              type='number',
                              value='',
                              min = 0,
                              id='diab_input_blood_p')

input_imc = dcc.Input(placeholder = 'IMC',
                              type='number',
                              value='',
                              min = 0,
                              id='diab_input_imc')

input_pedigree = dcc.Input(placeholder = 'DPF',
                              type='number',
                              value='',
                              min = 0,
                              max = 4,
                              id='diab_input_pedigree')

alert_resuit = dbc.Alert(
            "Vous n'êtes pas à risque",
            id="dalert-success",
            dismissable=True,
            is_open=True, color="success"
        )
alert_fall = dbc.Alert(
            "Attention! Vous etes à risque",
            id="dalert-attention",
            dismissable=True,
            is_open=True, color="danger"
        )
button_rdv = html.Div(
                dbc.Button(
                    "Prendre RDV",
                    href='cardio_link',
                    external_link=True,
                    color="danger", size='lg',
                    id='diab_rdv'
                            ),
                    )

city_drop = dcc.Dropdown(
                                id='diab_city',
                                options=[
                                    {'label': 'Bordeaux', 'value': 'bordeaux'},
                                    {'label': 'Lille', 'value': 'lille'},
                                    {'label': 'Lyon', 'value': 'lyon'},
                                    {'label': 'Marseille', 'value': 'marseille'},
                                    {'label': 'Nantes', 'value': 'nantes'},
                                    {'label': 'Paris', 'value': 'paris'},
                                    {'label': 'Toulouse', 'value': 'toulouse'},
                                    
                                    
                                ],
                                value='bordeaux')

fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    # value = ModelEn.predict_proba(X_patient)[0][0],
    value = 0,
    mode = "gauge+number+delta",
    title = {'text': "Risk assessment"},
    delta = {'reference': 0.5},
    gauge = {'axis': {'range': [0, 1], 'tickcolor': "darkblue"},
             'bar': {'color': "black"},
             'steps' : [
                 {'range': [0, 0.2], 'color': "green"},
                 {'range': [0.2, 0.5], 'color': "yellow"},
                 {'range': [0.5, 0.8], 'color' : "orange"},
                 {'range': [0.8, 1], 'color': "red"}]},
    ))


pie = go.Figure(data=[go.Pie(labels=df_imp['features'], 
                       values=df_imp['importance'], 
                       hole =0.3,
                       pull = [0.2, 0, 0, 0, 0, 0, 0 ])]).update_layout(title = 'Importance des variables dans le modèle de prédiciton',
                 title_x = 0.5,
                 title_y = 0.10)
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


layout = html.Div([modal,
    html.H1('Diabètes', style={'textAlign': 'center', 'margin-bottom' : '50px'}),
    html.Div([html.H3('Veuillez remplir le formulaire :', style={'textAlign': 'center'}),
        "Choisissez votre âge : ",
        slider_age,
        html.Br(),
            dbc.Row([
                dbc.Col([
                        html.Div("Indiquez le nombre de grossesses : "),
                        input_pregnancies,
                        ]),
                dbc.Col([
                        html.Div("Indiquez le taux de glucose (mg/dl) : "),
                        input_glucose,
                        dbc.Tooltip("Taux sain :  < 140 mg/dl",
                                    target = 'diab_input_gluc',
                                    placement = 'right'
                                    ),
                        ]),
                dbc.Col([
                        html.Div("Indiquez l'IMC : "),
                        input_imc
                        ])
                    ]),
        html.Br(),
            dbc.Row([
                dbc.Col([
                        html.Div("Indiquez le Diabetes Pedigree Function : "),
                        input_pedigree
                        ]),
                dbc.Col([
                        html.Div("Indiquez le taux d'insuline : "),
                        input_insulin   
                        ]),
                dbc.Col([
                        html.Div("Indiquez le pression sanguine (mm/Hg) : "),
                        input_blood_p
                        ])
                    ]),
                ],  style={"background-color" : 'LightGray', "color":"black", "border-radius": "15px", "padding" : '25px'}),
    
    html.Div([
            html.H2('Votre predisposition aux diabètes', style={'textAlign': 'center',  'margin-top' : '50px'}),
            dbc.Row(alert_resuit),
            dbc.Row(alert_fall), 
            ]),
    html.Div([
                dcc.Graph(figure = fig, id = 'jauge_diabete')       
            ]),
    html.Br(),
    dbc.Row(html.H6('Choisissez votre ville pour prendre RDV chez le spécialiste', style={'margin-bottom' : '10px'})),
    dbc.Row([dbc.Col(city_drop, width=3),
            dbc.Col()], style={'margin-bottom' : '10px'}),                                                                                             
    dbc.Row(button_rdv),
    html.H2('Le science derrière la prediction', style={'textAlign': 'center',  'margin-top' : '50px'}),

    html.Div([
            dbc.Row([
                dbc.Col(
                    html.P("""Il existe plusieurs variables qui sont très liées au diabète. Le modèle de prédiction à été selectionné parmi 5 modèles de machine learning différents. Ce modèle a été amélioré, ce  qui nous permet d'obtenir un score de prédiction de maladie proche de 0.9.
                                        Dans notre modèle, certaines variables sont plus importantes que d'autres. Le graphique montre que parmi les variables les plus importantes se trouve en tête la pression sanguine.  En effet, l'hypertension artérielle et le diabète sont deux maladies qui s'entretiennent entre elle. Un patient hypertendu présente plus de risques de développer du diabète et inversemment."""),
                               style={'margin-top' : '30px'}
                        ),
                    dbc.Col(dcc.Graph(figure=pie), style={'flex':2})
                    ]),
            ]),
    html.H3('Bibliographie',style={'textAlign': 'center',  'margin-top' : '50px'}),
    html.Div([
            dbc.ListGroup([
                dbc.ListGroupItem("Ma, Y., Xiong, J., Zhang, X., Qiu, T., Pang, H., Li, X., Zhu, J., Wang, J., Pan, C., Yang, X., Chu, X., Yang, B., Wang, C., Zhang, J., 2021. Potential biomarker in serum for predicting susceptibility to type 2 diabetes mellitus: Free fatty acid 22:6. J. Diabetes Investig. 12, 950–962. https://doi.org/10.1111/jdi.13443", href="https://pubmed.ncbi.nlm.nih.gov/33068491/"),
                dbc.ListGroupItem("Ruiz-Alejos, A., Carrillo-Larco, R.M., Miranda, J.J., Gilman, R.H., Smeeth, L., Bernabé-Ortiz, A., 2020. Skinfold thickness and the incidence of type 2 diabetes mellitus and hypertension: an analysis of the PERU MIGRANT study. Public Health Nutr. 23, 63–71. https://doi.org/10.1017/S1368980019001307", href="https://pubmed.ncbi.nlm.nih.gov/31159908/"),
                dbc.ListGroupItem("Wang, Q., Jokelainen, J., Auvinen, J., Puukka, K., Keinänen-Kiukaanniemi, S., Järvelin, M.-R., Kettunen, J., Mäkinen, V.-P., Ala-Korpela, M., 2019. Insulin resistance and systemic metabolic changes in oral glucose tolerance test in 5340 individuals: an interventional study. BMC Med. 17, 217. https://doi.org/10.1186/s12916-019-1440-4", href="https://pubmed.ncbi.nlm.nih.gov/31779625/"),
                dbc.ListGroupItem("Zhang, Yuanyuan, Nie, J., Zhang, Yan, Li, J., Liang, M., Wang, G., Tian, J., Liu, C., Wang, B., Cui, Y., Wang, X., Huo, Y., Xu, X., Hou, F.F., Qin, X., 2020. Degree of Blood Pressure Control and Incident Diabetes Mellitus in Chinese Adults With Hypertension. J. Am. Heart Assoc. 9, e017015. https://doi.org/10.1161/JAHA.120.017015", href="https://www.ahajournals.org/doi/10.1161/JAHA.120.017015"),                
                dbc.ListGroupItem("Kouhkan A, Najafi L, Malek M, Baradaran HR, Hosseini R, Khajavi A, Khamseh ME. Gestational diabetes mellitus: Major risk factors and pregnancy-related outcomes: A cohort study. Int J Reprod Biomed. 2021 Oct 10;19(9):827-836. doi: 10.18502/ijrm.v19i9.9715", href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8548751/"),                
                dbc.ListGroupItem("Wang Q, Jokelainen J, Auvinen J, Puukka K, Keinänen-Kiukaanniemi S, Järvelin MR, Kettunen J, Mäkinen VP, Ala-Korpela M. Insulin resistance and systemic metabolic changes in oral glucose tolerance test in 5340 individuals: an interventional study. BMC Med. 2019 Nov 29;17(1):217. doi: 10.1186/s12916-019-1440-4.", href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6883544/"),                
                dbc.ListGroupItem("Menke A., Rust K.F. Associations Between Trends in Race/Ethnicity, Aging, and Body Mass Index With Diabetes Prevalence in the United States 2 September 2014Volume 161, Issue 5, Page: 328-335", href="https://www.acpjournals.org/doi/10.7326/M14-0286"),                
                dbc.ListGroupItem("Deberneh HM, Kim I. Prediction of Type 2 Diabetes Based on Machine Learning Algorithm. Int J Environ Res Public Health. 2021 Mar 23;18(6):3317. doi: 10.3390/ijerph18063317.", href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8004981/"),                
                dbc.ListGroupItem("Lyssenko V, Jonsson A, Almgren P, Pulizzi N, Isomaa B, Tuomi T, Berglund G, Altshuler D, Nilsson P, Groop L. Clinical risk factors, DNA variants, and the development of type 2 diabetes. N Engl J Med. 2008 Nov 20;359(21):2220-32. doi: 10.1056/NEJMoa0801869.", href="https://pubmed.ncbi.nlm.nih.gov/19020324/"),
                dbc.ListGroupItem("De Tata V. Age-related impairment of pancreatic Beta-cell function: pathophysiological and cellular mechanisms. Front Endocrinol (Lausanne). 2014 Sep 3;5:138. doi: 10.3389/fendo.2014.0013", href="https://pubmed.ncbi.nlm.nih.gov/25232350/")
                ])])
])
    ################################################################## callback


@callback(
    Output('jauge_diabete', 'figure'),
    Output("dalert-attention", "is_open"),
    Output('dalert-success', 'is_open'),
    Output('diab_rdv', 'href'),
    [Input('diab_input_preg', 'value'),
    Input('diab_input_gluc', 'value'),
    Input('diab_input_insu', 'value'),
    Input('diab_input_blood_p', 'value'),
    Input('diab_input_imc', 'value'),
    Input('diab_input_pedigree', 'value'),
    Input('diab_slider_age', 'value'),
    Input('diab_city', 'value')],
    [State("dalert-attention", "is_open"),
    State('dalert-success', 'is_open')]
)

def update_city_selected(pregnancies, glucose, insuline,  pression_sang,  imc, pedigree, age, city, is_open1, is_open2):
    # Je prends soit la valeur indiquée dans la case, soit 0 (pour éviter des erreurs)

    responses = {'Pregnancies' : pregnancies or 0, 'Glucose': glucose or 0, 'BloodPressure' : pression_sang or 0, 
                'Insulin' : insuline or 0, 'BMI' : imc or 0, 
                'DiabetesPedigreeFunction' : pedigree or 0, 'Age' : age }
    

    X_patient = pd.DataFrame(responses.values(), responses.keys()).T
    # proba = model_rf.predict_proba(X_patient)[0][0]


    non_empty_inputs = [value for value in responses.values() if value != 0] 
    if len(non_empty_inputs) == 6 :
        proba = model_rf.predict_proba(X_patient)[0][1]*100
        if proba>=50:
            is_open1=True
            is_open2=False
        if proba<50:
            is_open1=False    
        if proba<20 and proba >0:
            is_open2=True
    else:
        proba = 0
        is_open1 = False
        is_open2 = False
        
    

    fig = go.Figure(go.Indicator(
            domain = {'x': [0, 1], 'y': [0, 1]},
            value = proba,
            mode = "gauge+number",
            title = {'text': "Probabilité (en %) d'avoir un diabète"},
            gauge = {'axis': {'range': [0, 100], 'tickcolor': "darkblue"},
                    'bar': {'color': "black"},
                    'steps' : [
                        {'range': [0, 30], 'color': "#E4F3EF"},
                        {'range': [30, 60], 'color': "#FFF5E1"},
                        {'range': [60, 100], 'color': "#FFE4DC"}]}))

    link = "https://www.doctolib.fr/diabetologue/"+city,
        
    return fig ,is_open1, is_open2, link
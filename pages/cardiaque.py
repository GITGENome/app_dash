import dash
from dash import html, dcc, callback, Input, Output, State, dash_table, Dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from joblib import dump, load
import pandas as pd


dash.register_page(__name__, 
                   path="/cardiaque")

#FIGURE OF FEATURE IMPORTANCE#
list_importance = [0, 0.02645161,  0.05612903, -0.00580645, -0.01354839, -0.00193548,
 -0.01677419,  0.06064516,  0.03290323,  0.03419355,  0.01032258,  0.02967742,
  0.04]     
list_features = ['age', 'sex', 'douleur', 'pression art', 'cholesterol', 'haut glucose', 'ECG', 'fréq cardiaque',
       'angine', 'segment ST depression', 'segment ST pente', 'vaisseaux majeurs', 'thalassémie']
fig_importance = px.line_polar(theta=list_features, r=list_importance, line_close=True,
                    color_discrete_sequence=px.colors.sequential.Plasma,
                   )


#TABLE#
table_cardiac_head = [
    html.Thead(html.Tr([html.Th("Facteurs de risque"), html.Th("Rôle dans la maladie"), html.Th("Valeur normale")]))
]
row1 = html.Tr([html.Td("Thalassemia"), html.Td("La thalassémie est une maladie génétique caractérisée par l'hémoglobine altérée et la réduction de sa capacité à transporter l'oxygène. En raison de l'altération de sa structure, le fer a une affinité réduite pour l'hémoglobine, ce qui entraîne une augmentation du fer ionisé dans le sang. Le fer va s'accumuler dans le muscle cardiaque, entraînant un dysfonctionnement cardiaque."), html.Td('maladie génétique')])
row2 = html.Tr([html.Td("Nombre de vaisseaux majeurs colorés par fluoroscopie"), html.Td("Cela correspond au nombre de vaisseaux sanguins majeurs colorés lors d'une procédure de fluoroscopie, souvent utilisée pour évaluer la santé cardiaque, en particulier lors d'une angiographie coronarienne. Ce nombre peut indiquer le degré de vascularisation des artères coronaires, et des valeurs anormalement basses peuvent suggérer une altération de l'irrigation sanguine vers le cœur. Une faible coloration des vaisseaux majeurs peut être associée à des maladies cardiaques, telles que la maladie coronarienne, où les artères coronaires peuvent être obstruées, limitant ainsi le flux sanguin vers le muscle cardiaque. Cependant, une interprétation précise nécessite une évaluation clinique complète et d'autres investigations médicales"), html.Td('Le moins possible')])
row3 = html.Tr([html.Td("Dépression du segment ST induite par l'exercice par rapport au repos"), html.Td("Une augmentation à long terme du risque d'infarctus du myocarde ou de la nécessité future d'un pontage coronarien a été observée chez des hommes d'âge moyen en bonne santé présentant une dépression du segment ST, même après ajustement pour les facteurs de risque. Cela met en lumière une valeur pronostique potentielle de cette observation."), html.Td('Le moins que 0.1 mV')])
row4 = html.Tr([html.Td("Angine induite par l'exercice"), html.Td("L'angine de poitrine induite par l'exercice, parfois désignée sous le terme 'Exang' (pour Exercise-Induced Angina), est une manifestation particulière de l'angine de poitrine. Elle se produit pendant ou après un effort physique. L'angine de poitrine, un symptôme fréquent de la maladie coronarienne, représente une forme de maladie cardiaque."), html.Td("L'absence de douleur")])
row5 = html.Tr([html.Td("La fréquence cardiaque maximale atteinte"), html.Td("La fréquence cardiaque maximale est influencée par divers facteurs, tels que l'âge, le sexe, la génétique et le niveau de condition physique, diminuant généralement avec l'âge. Bien que la fréquence cardiaque maximale en elle-même ne soit pas un indicateur direct de maladies cardiaques, elle peut être utilisée comme un outil dans l'évaluation globale de la condition cardiovasculaire."), html.Td("220 moins l'âge en années")])

table_body = [html.Tbody([row1, row2, row3, row4, row5])]

table_cardiac = dbc.Table(table_cardiac_head + table_body, 
                          bordered=True,
                            color='dark',
                            hover=True,
                            responsive=True,
                            striped=True,)



                                                  ########
                                               #BOOTSTRAP ELEMENTS
                                                   #######   
                                                                       

                        
age_slider = dcc.Slider(id='cardio_age', min=20, max=100, step=1, value=45,
                    marks = None,
                        tooltip={"placement": "bottom",
                                 "always_visible": True})
cp_slider = dcc.Slider(id='cardio_cp', min=0, max=3, step=1, value=0)
cp_pop = dbc.Popover(
                        dbc.PopoverBody("Le niveau de douleur thoracique ressentie: 0 - insupportable, 3 - pas ressentie"),
                        target="cardio_cp",
                        trigger="click",)
sex_drop = dcc.Dropdown(id='cardio_sex',
                                options=[
                                    {'label': 'Homme', 'value': 1},
                                    {'label': 'Femme', 'value': 0}
                                ])
thestbps_input = dcc.Input(id='cardio_thestbps', type="number",
                                        min=50, max=220, step=1,
                                        placeholder='mmHg')
exang_drop =  dcc.Dropdown(
                                id='cardio_exang',
                                options=[
                                    {'label': 'Oui', 'value': 1},
                                    {'label': 'No', 'value': 0}
                                ])
restecg_drop = dcc.Dropdown(
                                id='cardio_restecg',
                                options=[
                                    {'label': 'Abnormal', 'value': 0},
                                    {'label': 'Normal', 'value': 1},
                                    {'label': 'Normal', 'value': 2}
                                ]
                                )                                                          
restecg_pop = dbc.Popover(
                            dbc.PopoverBody("The prognostic importance of major ECG abnormalities is strongly influenced by the presence of symptomatic"),
                            target="cardio_restecg",
                            trigger="click",
                    )                                      
chol_input = dcc.Input(id='cardio_chol', type="number",
                                        min=120, max=580, step=1,
                                        placeholder='mg/dl')
fbs_drop = dcc.Dropdown(
                                id='cardio_fbs',
                                options=[
                                    {'label': '=< 120 mg/dl', 'value': 0},
                                    {'label': '> 120 mg/dl', 'value': 1}
                                    
                                ]
                                )
slope_drop = dcc.Dropdown(
                                id='cardio_slope',
                                options=[
                                    {'label': '0', 'value': 0},
                                    {'label': '1', 'value': 1},
                                    {'label': '2', 'value': 2}
                                ]
                                )
slope_pop = dbc.Popover(
                            dbc.PopoverBody("Pente du segment ST à l'effort maximal par rapport de resultat ECG"),
                            target="cardio_slope",
                            trigger="click",
                    )
thal_drop = dcc.Dropdown(
                                id='cardio_thal',
                                options=[
                                    {'label': '0', 'value': 0},
                                    {'label': '1', 'value': 1},
                                    {'label': '2', 'value': 2},
                                    {'label': '3', 'value': 3}
                                    
                                ]
                                )
thal_pop = dbc.Popover(
                            dbc.PopoverBody("La thalassémie est une maladie génétique caractérisée par le hemoglobin altérée et la réduction de sa capacité de transporter l'oxygène"),
                            target="cardio_thal",
                            trigger="click",
                    )
thalach_input = dcc.Input(id='cardio_thalach', type="number",
                                           min=60, max=250, step=1,
                                           placeholder='60-250')
thalach_pop = dbc.Popover(
                        dbc.PopoverBody("Fréquence cardiaque maximale atteinte pendant l'exercise"),
                        target="cardio_thalach",
                        trigger="click",
                            )
ca_slider = dcc.Slider(id='cardio_ca', min=0, max=4, step=1)
ca_pop = dbc.Popover(
                        dbc.PopoverBody("Nombre de vaisseaux majeurs colorés par fluoroscopie"),
                        target="cardio_ca",
                        trigger="click",
                            )
oldpeak_input = dcc.Input(id='cardio_oldpeak', type="number",
                                        min=0, max=2, step=0.1, 
                                        placeholder='0.0-2.0'
                                        )
oldpeak_pop = dbc.Popover(
                        dbc.PopoverBody("Dépression du segment ST induite par l'exercice par rapport au repos par rapport de ECG"),
                        target="cardio_oldpeak",
                        trigger="click",
                            )
alert_resuit = dbc.Alert(
            "Vous n'etes pas à risque",
            id="calert-success",
            dismissable=True,
            is_open=True, color="success"
        )
alert_fall = dbc.Alert(
            "Attention! Vous etes à risque",
            id="calert-attention",
            dismissable=True,
            is_open=True, color="danger"
        )
button_rdv = html.Div(
    [
        dbc.Button(
            "Prendre RDV",
            href='cardio_link',
            external_link=True,
            color="danger", size='lg',
            id='cardio_rdv'
        ),
    ]
)
city_drop = dcc.Dropdown(
                                id='cardio_city',
                                options=[
                                    {'label': 'Bordeaux', 'value': 'bordeaux'},
                                    {'label': 'Lille', 'value': 'lille'},
                                    {'label': 'Lyon', 'value': 'lyon'},
                                    {'label': 'Paris', 'value': 'paris'},
                                    {'label': 'Nantes', 'value': 'nantes'},
                                    {'label': 'Toulouse', 'value': 'toulouse'}
                                    
                                ],
                                value='Bordeaux')
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

                                                  ##########
                                                   # LAYOUT#
                                                        
                                                  ##########

    
layout = html.Div([modal,
    html.H1('Maladies cardiaques', style={'textAlign': 'center', 'margin-bottom' : '50px'}),
    html.Div([html.H3('Veuillez remplir le formulaire', style={'textAlign': 'center'}),
              html.H6('Choisissez votre age'),
            dbc.Row(age_slider, style={'margin-bottom' : '20px', 'margin-left' : '10px', 'margin-right' : '10px'}),
            dbc.Row([dbc.Col([html.H6('Choisissez le genre'),
                            sex_drop 
                            ]),
                    dbc.Col([html.H6('Cholestérol sérique'),
                            chol_input 
                            ]),                             
                #    dbc.Col([html.H6('Douleur thoracique'),
                #            cp_slider, cp_pop
                #            ]),
                    dbc.Col([html.H6('Type de thalassémie'),
                            thal_drop, 
                            thal_pop]),
                    dbc.Col([html.H6('Résultats électrocardiogramme au repos'),
                            restecg_drop, restecg_pop
                            ])                                
                    ], style={'margin-bottom' : '25px'}),
          
            dbc.Row([dbc.Col([html.H6('Fréquence cardiaque maximale'),
                            thalach_input, 
                            thalach_pop]),                    
                    dbc.Col([html.H6('Sucre dans le sang à jeun'),
                            fbs_drop
                            ]),
                    dbc.Col([html.H6("L'angine pendant l'exercice"),
                            exang_drop 
                            ]),
                    
                    dbc.Col([html.H6('Dépression du segment ST'),
                            oldpeak_input, 
                            oldpeak_pop]),
                    ], style={'margin-bottom' : '25px'}),

            dbc.Row([dbc.Col([html.H6('Pression artérielle au repos'),
                            thestbps_input 
                            ]),
                    dbc.Col(),
                    dbc.Col([html.H6('Nombre de vaisseaux majeurs'),
                            ca_slider, 
                            ca_pop]),
                    dbc.Col([html.H6('Pente du segment ST'),
                            slope_drop, 
                            slope_pop]),                   
            ])
            ], style={"background-color" : 'LightGray', "color":"black", "border-radius": "15px", "padding" : '25px'}),
    html.H2('Votre prédisposition aux maladies cardiaques', style={'textAlign': 'center',  'margin-top' : '50px'}),

    dbc.Row(alert_resuit),
    dbc.Row(alert_fall), 
    
    html.Div([dbc.Row(dcc.Graph(id='risk_fig'))]),
                                            
    dbc.Row(html.H6('Choisissez votre ville pour prendre RDV chez le spécialiste', style={'margin-bottom' : '10px'})),
    dbc.Row([dbc.Col(city_drop, width=3),
            dbc.Col()], style={'margin-bottom' : '10px'}),                                                                                             
    dbc.Row(button_rdv),

    html.H2('Le science derrière la prédiction', style={'textAlign': 'center',  'margin-top' : '50px'}),

    html.Div([dbc.Row([dbc.Col(html.H6("""Les maladies cardiaques font principalement référence aux conditions de vaisseaux sanguins obstrués ou rétrécis, entraînant un accident vasculaire cérébral, des douleurs thoraciques ou une angine de poitrine, et une crise cardiaque. D'autres types de maladies cardiaques, telles que celles affectant le rythme, la valve ou le muscle cardiaque, sont d'autres types de maladies cardiaques.
                                       A cause de cela, nous avons déterminé certains types de variables qui sont très liés à la maladie cardiaque.
                                       D'autre part, l'apprentissage automatique est crucial pour déterminer si quelqu'un a souffert d'une maladie cardiaque. Si ces conditions sont prédites à l'avance, les médecins auraient beaucoup plus facilement accès à des informations cruciales pour le traitement et le diagnostic des patients.
                                       Notre modèle de prédiction est basé sur 5 modèles de machine learning différents qui nous permettent d'obtenir un score de prédiction des maladies cardiaques proche de 0.9.
                                        """)
                                    , style={'margin-top' : '30px'}),
                       dbc.Col(dcc.Graph(figure=fig_importance), width=7)]),
            dbc.Row(table_cardiac)]),
    html.H3('Bibliographie',style={'textAlign': 'center',  'margin-top' : '50px'}),
    html.Div([
            dbc.ListGroup([
                dbc.ListGroupItem("Yusifov A., Woulfe K.C., Bruns D.R., 2022. Mechanisms and implications of sex differences in cardiac aging in J Cardiovasc Aging.HHS Author Manuscripts. https://doi.org/10.20517/jca.2022.01", href="https://pubmed.ncbi.nlm.nih.gov/35419571/"),
                dbc.ListGroupItem("Fox, K, Borer, J, Camm, A. et al. Resting Heart Rate in Cardiovascular Disease. J Am Coll Cardiol. 2007 Aug, 50 (9) 823–830. https://doi.org/10.1016/j.jacc.2007.04.079", href="https://www.sciencedirect.com/science/article/pii/S0735109707018232"),
                dbc.ListGroupItem("Walker M, Wood J. CARDIAC COMPLICATIONS IN THALASSAEMIA MAJOR. In: Cappellini MD, Cohen A, Porter J, et al., editors. Guidelines for the Management of Transfusion Dependent Thalassaemia (TDT) [Internet]. 3rd edition. Nicosia (CY): Thalassaemia International Federation; 2014. Chapter 4", href="https://www.ncbi.nlm.nih.gov/books/NBK269371/"),
                dbc.ListGroupItem("Grundy, S.M., n.d. Cholesterol and Coronary Heart Disease.", href="https://pubmed.ncbi.nlm.nih.gov/2141179/"),
                dbc.ListGroupItem("Park, C., Guallar, E., Linton, J.A., Lee, D.-C., Jang, Y., Son, D.K., Han, E.-J., Baek, S.J., Yun, Y.D., Jee, S.H., Samet, J.M., 2013. Fasting Glucose Level and the Risk of Incident Atherosclerotic Cardiovascular Diseases. Diabetes Care 36, 1988–1993. https://doi.org/10.2337/dc12-1577", href="https://pubmed.ncbi.nlm.nih.gov/23404299/"),
                dbc.ListGroupItem("Whincup PH, Wannamethee G, Macfarlane PW, Walker M, Shaper AG. Resting electrocardiogram and risk of coronary heart disease in middle-aged British men. J Cardiovasc Risk. 1995 Dec;2(6):533-43", href="https://pubmed.ncbi.nlm.nih.gov/8665372/"),
                dbc.ListGroupItem("Tamura, A., Nagao, K., Inada, T., & Tanaka, M. (2018). Exercise-induced vasospastic angina with prominent ST elevation: a case report. European Heart Journal - Case Reports, 2(4).", href="https://pubmed.ncbi.nlm.nih.gov/31020217/"),
                dbc.ListGroupItem("Marateb HR, Goudarzi S. A noninvasive method for coronary artery diseases diagnosis using a clinically-interpretable fuzzy rule-based system. J Res Med Sci. 2015 Mar;20(3):214-23. PMID: 26109965; PMCID: PMC4468223.", href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4468223/"),
                dbc.ListGroupItem("Kremastinos D.T., Farmakis D., Aessopos A. β-Thalassemia Cardiomyopathy. Circulation: Heart Failure. 2010;3:451–458", href="https://www.ahajournals.org/doi/10.1161/CIRCHEARTFAILURE.109.913863")
                ])])
])


@callback(
          Output('risk_fig', 'figure'),
        Output("calert-attention", "is_open"),
        Output('calert-success', 'is_open'),
        Output('cardio_rdv', 'href'),
    [Input('cardio_age', 'value'),
    Input('cardio_sex', 'value'),
    Input('cardio_thestbps', 'value'),
    Input('cardio_exang', 'value'),
    Input('cardio_restecg', 'value'),
    Input('cardio_chol', 'value'),
    Input('cardio_fbs', 'value'),
    Input('cardio_slope', 'value'),
    Input('cardio_thal', 'value'),
    Input('cardio_thalach', 'value'),
    Input('cardio_ca', 'value'),
    Input('cardio_oldpeak', 'value'),
    Input('cardio_city', 'value')
    ],
    [State("calert-attention", "is_open" ),
    State('calert-success', 'is_open')]
)
def update_city_selected(age, sex, thestbps, exang, restecg, chol, fbs, slope, thal, thalach, ca, oldpeak, city, is_open1, is_open2):
    responses = {'age' : age or 0, 'sex' : sex or 0, 'trestbps': thestbps or 0, 
                 'chol' : chol or 0, 'fbs' : fbs or 0, 'restecg' : restecg or 0, 
                'thalach': thalach or 0, 'exang': exang or 0, 'oldpeak': oldpeak or 0,
                'slope':slope or 0,'ca':ca or 0, 'thal':thal or 0}
    model_cardiac = load('regression_model_saved.joblib')
    X_patient = pd.DataFrame(responses.values(), responses.keys()).T
    
    proba = model_cardiac.predict_proba(X_patient)[0][0]*100    
        
    if proba>=50:
        is_open1=True
        is_open2=False
    if proba<50:
        is_open1=False    
    if 0<proba<20:
        is_open2=True
    if age or sex or thestbps or exang or restecg or chol or fbs or slope or thal or thalach or ca or oldpeak is None:
        is_open2=False
       
    
    fig = go.Figure(go.Indicator(
            domain = {'x': [0, 1], 'y': [0, 1]},
            value = proba,
            mode = "gauge+number",
            title = {'text': "Probabilité (en %) d'avoir une maladie cardiaque"},
            gauge = {'axis': {'range': [0, 100], 'tickcolor': "darkblue"},
                    'bar': {'color': "black"},
                    'steps' : [
                        {'range': [0, 30], 'color': "#E4F3EF"},
                        {'range': [30, 60], 'color': "#FFF5E1"},
                        {'range': [60, 100], 'color': "#FFE4DC"}]}))

    link = "https://www.doctolib.fr/cardiologue/"+city,
        
    
    return fig, is_open1, is_open2, link
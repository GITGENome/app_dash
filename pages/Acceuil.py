import dash
from dash import html, Output, Input, State, callback, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv('countries.csv')

dico = {'Maladie cardiaque' : """Les maladies cardio-neurovasculaires et leurs complications sont la première cause de décès dans le monde. En France, elles sont la deuxième cause de décès après les cancers, en étant responsable de plus de 140 000 morts chaque année en population générale. Ce n’est que chez les personnes âgées de 85 ans et plus qu’elles sont la première cause de décès. Elles sont aussi une cause majeure de maladie et de décès précoces, d’hospitalisation, et de handicap acquis. Jusqu’à 50 000 personnes font un arrêt cardiaque soudain chaque année, dont environ 5% survivent.""",
        'Maladie de foie' : """Le foie est un organe clé impliqué dans des fonctions métaboliques et de détoxification homéostatiques cruciales pour l'organisme humain. Ainsi, le foie est le point central d'un réseau d'organes tissant une série d'interactions complexes dans l'organisme, ce qui fait des lésions hépatiques une condition indésirable sous-jacente dans un ensemble de maladies. Les maladies hépatiques chroniques peuvent être principalement causées par des dysfonctionnements liés à l'alcool, le virus de l'hépatite B, le virus de l'hépatite C, des traitements médicamenteux ou une stéatose hépatique non alcoolique. Les patients atteints de maladies hépatiques nécessitent des suivis fréquents et une surveillance attentive, car les maladies hépatiques chroniques peuvent éventuellement conduire à la cirrhose ou au carcinome hépatocellulaire s'ils ne sont pas diagnostiqués à temps pour un traitement ou une intervention chirurgicale. Ces conditions liées aux maladies hépatiques chroniques sont devenues un fardeau mondial, dont les taux de mortalité associés ont augmenté au fil des ans, atteignant plus de 2 millions de décès dans le monde.""",
        'Maladie du rein' : """Les maladies rénales chroniques sont reconnues comme des problèmes de santé mondiaux significatifs. Et parce que ces conditions sont détectées trop tard dans l'évolution de la maladie, aucun traitement efficace n'a été développé pour minimiser les lésions rénales, modifier le cours de la maladie ou limiter la morbidité et la mortalité associées. La perte progressive de la fonction rénale peut conduire à une insuffisance rénale terminale chez les patients atteints de maladie rénale chronique, précipitant le besoin d'une thérapie de remplacement rénal. Une intervention rapide chez les patients atteints de maladie rénale chronique présentant un risque élevé d'insuffisance rénale terminale peut non seulement améliorer la qualité de vie de ces patients en retardant la progression de la maladie, mais aussi réduire la morbidité, la mortalité et les coûts de soins de santé résultant de la thérapie de remplacement rénal. Comme la progression de la maladie est généralement silencieuse, un modèle de prédiction fiable du risque d'insuffisance rénale terminale au stade précoce de la maladie rénale chronique peut être cliniquement essentiel. Un tel modèle est censé aider les médecins à prendre des décisions de traitement personnalisées pour les patients à haut risque, améliorant ainsi le pronostic global et réduisant la charge économique de cette maladie.""",
        'Cancer du sein' : """Dans le monde en développement, la mortalité due au cancer est l'un des principaux problèmes pour l'humanité. Même s'il existe de nombreuses façons de le prévenir avant qu'il ne se produise, certains types de cancer n'ont toujours aucun traitement. L'un des types de cancer les plus courants est le cancer du sein, et le diagnostic précoce est la chose la plus importante dans son traitement. Un diagnostic précis est l'un des processus les plus importants dans le traitement du cancer du sein. """,
        'Diabetes' : """Le diabète est une maladie chronique qui survient soit lorsque le pancréas ne produit pas suffisamment d'insuline, soit lorsque le corps ne peut pas utiliser efficacement l'insuline qu'il produit. La détection précoce du diabète peut être d'une grande utilité, surtout parce que la progression de la prédiabète au diabète de type 2 est assez élevée. Le diabète peut affecter n'importe quelle partie du corps avec le temps, entraînant différents types de complications. Les types les plus courants sont divisés en troubles micro et macrovasculaires. Les premiers sont des complications à long terme qui affectent les petits vaisseaux sanguins, notamment la rétinopathie, la néphropathie et la neuropathie. Les troubles macrovasculaires, en revanche, comprennent la maladie cardiaque ischémique, la maladie vasculaire périphérique et la maladie cérébrovasculaire."""}
dash.register_page(__name__, path='/')

year_slider = dcc.Slider(id='year', min=1990, max=2019, step=5, value=2019,
                         marks={i: '{}'.format(int(i)) for i in [1990, 1995, 2000, 2005, 2010, 2015, 2019]})


disease_drop = dcc.Dropdown(
                                id='disease_drop',
                                options=[
                                    {'label': 'Cardiaque', 'value': 'Maladie cardiaque'},
                                    {'label': 'Foie', 'value': 'Maladie de foie'},
                                    {'label': 'Rein', 'value': 'Maladie du rein'},
                                    {'label': 'Diabetes', 'value': 'Diabetes'},
                                    {'label': 'Cancer (sein)', 'value': 'Cancer du sein'}                                                                        
                                ],
                                value='Maladie cardiaque')
sex_drop = dcc.Dropdown(
                                id='sex_country',
                                options=[
                                    {'label': 'Homme', 'value': 'Male'},
                                    {'label': 'Femme', 'value': 'Female'},
                                    {'label': 'Tous', 'value': 'Both'}                                    
                                ],
                                value='Both')
measure_drop = dcc.Dropdown(
                                id='measure_country',
                                options=[
                                    {'label': 'Décès', 'value': 'Deaths'},
                                    {'label': 'Prévalence', 'value': 'Prevalence'},
                                    {'label': 'Incidence', 'value': 'Incidence'}                                    
                                ],
                                value='Deaths')

layout = html.Div([
    html.H1("Prédiction des maladies chroniques", style={'textAlign': 'center', 'text-decoration' : 'underline overline #2c5f4d', 'margin-bottom' : '30px'}),
    html.H6("""Selon l'OMS, les 10 principales causes de décès dans le monde sont responsables de 55 % des décès, et parmi ces 10 maladies, 7 ne sont pas contagieuses. Autrement dit, elles sont chroniques avec la possibilité de les prévoir et d'agir avant qu'elles ne deviennent irréversibles""", style={'margin-bottom' : '20px'}),
    html.H5('Veuillez-vous choisir la maladie'),
    html.Div(dbc.Row([dbc.Col(disease_drop, width=3),
             dbc.Col()])),
    html.H4('Epidémiologie mondiale', style={'textAlign' : 'center', 'margin-top' : '20px', 'margin-bottom' : '20px'}),
    html.Div([dbc.Row(dcc.Graph(id='carte')),
              dbc.Row([
                  dbc.Col(year_slider, width=5),
                  dbc.Col(sex_drop, style={'margin-left' : '10px', 'margin-right' : '10px'}),
                  dbc.Col(measure_drop)
                  ], style={ 'margin-right' : '170px'})]),

    html.Div(html.H6(id='text-description'))
])
    


@callback(Output('carte', 'figure'),
          Output('text-description', 'children'),
        [Input('disease_drop', 'value'),
         Input('year', 'value'),
         Input('sex_country', 'value'),
         Input('measure_country', 'value')])
def update_graph(disease, year, sex, measure):
    fig = px.choropleth(df[(df['measure_name']==measure) & (df['cause_name']==disease) & (df['year']==year) & (df['sex_name']==sex)],
                    locations="iso_alpha",
                    color="val",
                    color_continuous_scale='tealrose', labels={
                     "val": "% dans la population"
                     }
                    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(1,1,1,1)')

    return fig, dico[disease]
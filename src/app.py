import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

external_stylesheets = [dbc.themes.BOOTSTRAP,
                        'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
                        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.0/font/bootstrap-icons.css",
                        'https://use.fontawesome.com/releases/v5.8.1/css/all.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ]
                )

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(
        children=[
            html.H1('WORDLE', className='display-6 wordle-title'),
            html.Hr(className='title-sep')
        ],
        className='page-header'),
    html.Div(id='page-content', children=[], className='page-content'),
    dcc.Store(id='action-store'),
    dcc.Store(id='state-store', data={'current_word': 0, 'current_letter': 0, 'words': []}),
    dcc.Store(id='evaluation-trigger'),
    dcc.Store(id='evaluation-store', data=[]),
    dcc.Store(id='previous-guesses', data=[])
])

server = app.server


def load_all_words_into_set(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    d = {str.upper(x.strip()) for x in lines}
    return d


WORDS_SET = load_all_words_into_set('all_words.txt')



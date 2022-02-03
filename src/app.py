import json

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, ALL, MATCH, callback_context, State
from dash.exceptions import PreventUpdate

from evaluation_engine import get_output_classes, evaluate
from keyboard import keyboard_layout
from word_grid import grid_layout, message_box_layout

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
    html.Div(id='page-content', children=[html.Div([grid_layout(), message_box_layout(), keyboard_layout()])],
             className='page-content'),
    dcc.Store(id={'type': 'action-store', 'key': 0}),
    dcc.Store(id={'type': 'action-store', 'key': 1}),
    dcc.Store(id={'type': 'action-store', 'key': 2}),
    dcc.Store(id={'type': 'action-store', 'key': 3}),
    dcc.Store(id={'type': 'action-store', 'key': 4}),
    dcc.Store(id={'type': 'action-store', 'key': 5}),
    dcc.Store(id={'type': 'words-store', 'key': 0}, data=''),
    dcc.Store(id={'type': 'words-store', 'key': 1}, data=''),
    dcc.Store(id={'type': 'words-store', 'key': 2}, data=''),
    dcc.Store(id={'type': 'words-store', 'key': 3}, data=''),
    dcc.Store(id={'type': 'words-store', 'key': 4}, data=''),
    dcc.Store(id={'type': 'words-store', 'key': 5}, data=''),
    dcc.Store(id='current-word-store', data=0),
    dcc.Store(id='evaluations-store', data=[]),
    dcc.Store(id='previous-guesses', data=[]),
    dcc.Store(id={'type': 'word-update', 'key': 0}),
    dcc.Store(id={'type': 'word-update', 'key': 1}),
    dcc.Store(id={'type': 'word-update', 'key': 2}),
    dcc.Store(id={'type': 'word-update', 'key': 3}),
    dcc.Store(id={'type': 'word-update', 'key': 4}),
    dcc.Store(id={'type': 'word-update', 'key': 5}),
    dcc.Store(id={'type': 'word-evaluated', 'key': 0}),
    dcc.Store(id={'type': 'word-evaluated', 'key': 1}),
    dcc.Store(id={'type': 'word-evaluated', 'key': 2}),
    dcc.Store(id={'type': 'word-evaluated', 'key': 3}),
    dcc.Store(id={'type': 'word-evaluated', 'key': 4}),
    dcc.Store(id={'type': 'word-evaluated', 'key': 5}),
    dcc.Store(id='completed-store', data=False)
])

server = app.server


def load_all_words_into_set(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    d = {str.upper(x.strip()) for x in lines}
    return d


WORDS_SET = load_all_words_into_set('./all_words.txt')


@app.callback(
    [Output({'type': 'action-store', 'key': 0}, 'data'),
     Output({'type': 'action-store', 'key': 1}, 'data'),
     Output({'type': 'action-store', 'key': 2}, 'data'),
     Output({'type': 'action-store', 'key': 3}, 'data'),
     Output({'type': 'action-store', 'key': 4}, 'data'),
     Output({'type': 'action-store', 'key': 5}, 'data')],
    [Input({'type': 'keybutton', 'index': ALL}, 'n_clicks')],
    State('current-word-store', 'data'),
    State('completed-store', 'data')
)
def key_pressed(n_clicks_list, current_word, completed_status):
    if current_word > 5 or completed_status:
        raise PreventUpdate()
    if callback_context.triggered is not None:
        value = callback_context.triggered[0]['value']
        if value is not None:
            property_json_str = callback_context.triggered[0]['prop_id'].split('.')[0]
            if len(property_json_str) > 0:
                triggered_key = json.loads(property_json_str)['index']
                actions = [None for x in range(6)]
                actions[current_word] = triggered_key
                return actions
    raise PreventUpdate()


app.clientside_callback(
    """
    function(action, current_word, word) {
        
        if(action){
            var current_letter = 0;
            var new_word = '';
            if (word == null) {
                word = '';
            }
            
            if(word.length > 0) {
                current_letter = word.length;
            }
            if(current_word > 5) {
                throw window.dash_clientside.PreventUpdate;
            }
            if(action.length == 1){
                if(current_letter >= 5) {
                    throw window.dash_clientside.PreventUpdate;
                }
                new_word = word + action;
            } else if(action == 'backspace') {
                if(word.length == 0 || current_letter == 0){
                    throw window.dash_clientside.PreventUpdate;
                }
                new_word = word.slice(0, -1);
                current_letter -= 1;
            } else {
                throw window.dash_clientside.PreventUpdate;
            }
            return [true, new_word];
        }
        throw window.dash_clientside.PreventUpdate;
    }
    """,
    Output({'type': 'word-update', 'key': MATCH}, 'data'),
    Output({'type': 'words-store', 'key': MATCH}, 'data'),
    Input({'type': 'action-store', 'key': MATCH}, 'data'),
    State('current-word-store', 'data'),
    State({'type': 'words-store', 'key': MATCH}, 'data')
)


@app.callback(
    [Output('current-word-store', 'data'),
     Output('evaluations-store', 'data'),
     Output('previous-guesses', 'data'),
     Output('completed-store', 'data'),
     [Output({'type': 'word-evaluated', 'key': 0}, 'data'),
      Output({'type': 'word-evaluated', 'key': 1}, 'data'),
      Output({'type': 'word-evaluated', 'key': 2}, 'data'),
      Output({'type': 'word-evaluated', 'key': 3}, 'data'),
      Output({'type': 'word-evaluated', 'key': 4}, 'data'),
      Output({'type': 'word-evaluated', 'key': 5}, 'data')],
     Output('message-box', 'header'), Output('message-box', 'is_open')],
    Input('enter-button', 'n_clicks'),
    State('current-word-store', 'data'),
    State({'type': 'words-store', 'key': ALL}, 'data'),
    State('evaluations-store', 'data'),
    State('previous-guesses', 'data')
)
def enter_pressed(n_clicks, current_word, words, evaluations, previous_guesses):
    if n_clicks is not None:
        if current_word < 6:
            word = words[current_word]
            if len(word) != 5:
                raise PreventUpdate()
            if word not in WORDS_SET:
                return [current_word, evaluations, previous_guesses, False, [None for x in range(6)], 'Not in word list', True]
            if word in previous_guesses:
                return [current_word, evaluations, previous_guesses, False, [None for x in range(6)], 'Already guessed', True]
            evaluations, previous_guesses, completed_status = evaluate(word_to_evaluate=word,
                                                                       evaluations=evaluations,
                                                                       previous_guesses=previous_guesses)
            words_evaluated = [None for x in range(6)]
            words_evaluated[current_word] = True
            if completed_status:
                current_word = 6
            else:
                current_word += 1

            return [current_word, evaluations, previous_guesses, completed_status, words_evaluated, '', False]

    raise PreventUpdate()


app.clientside_callback(
    """
    function(data, word) {
        if(data) {
            var outputs = [];
            var count = 0;
            for(var i=0; i<word.length; i++) {
                count += 1;
                outputs.push(word[i]);      
            }
            for(var i=count; i<5; i++) {
                outputs.push('');
            }
            return outputs;
        }
    }
    """,
    [Output('word-0-letter-0', 'children'),
     Output('word-0-letter-1', 'children'),
     Output('word-0-letter-2', 'children'),
     Output('word-0-letter-3', 'children'),
     Output('word-0-letter-4', 'children')],
    Input({'type': 'word-update', 'key': 0}, 'data'),
    State({'type': 'words-store', 'key': 0}, 'data')
)


app.clientside_callback(
    """
    function(data, word) {
        if(data) {
            var outputs = [];
            var count = 0;
            for(var i=0; i<word.length; i++) {
                count += 1;
                outputs.push(word[i]);      
            }
            for(var i=count; i<5; i++) {
                outputs.push('');
            }
            return outputs;
        }
    }
    """,
    [Output('word-1-letter-0', 'children'),
     Output('word-1-letter-1', 'children'),
     Output('word-1-letter-2', 'children'),
     Output('word-1-letter-3', 'children'),
     Output('word-1-letter-4', 'children')],
    Input({'type': 'word-update', 'key': 1}, 'data'),
    State({'type': 'words-store', 'key': 1}, 'data')
)


app.clientside_callback(
    """
    function(data, word) {
        if(data) {
            var outputs = [];
            var count = 0;
            for(var i=0; i<word.length; i++) {
                count += 1;
                outputs.push(word[i]);      
            }
            for(var i=count; i<5; i++) {
                outputs.push('');
            }
            return outputs;
        }
    }
    """,
    [Output('word-2-letter-0', 'children'),
     Output('word-2-letter-1', 'children'),
     Output('word-2-letter-2', 'children'),
     Output('word-2-letter-3', 'children'),
     Output('word-2-letter-4', 'children')],
    Input({'type': 'word-update', 'key': 2}, 'data'),
    State({'type': 'words-store', 'key': 2}, 'data')
)


app.clientside_callback(
    """
    function(data, word) {
        if(data) {
            var outputs = [];
            var count = 0;
            for(var i=0; i<word.length; i++) {
                count += 1;
                outputs.push(word[i]);      
            }
            for(var i=count; i<5; i++) {
                outputs.push('');
            }
            return outputs;
        }
    }
    """,
    [Output('word-3-letter-0', 'children'),
     Output('word-3-letter-1', 'children'),
     Output('word-3-letter-2', 'children'),
     Output('word-3-letter-3', 'children'),
     Output('word-3-letter-4', 'children')],
    Input({'type': 'word-update', 'key': 3}, 'data'),
    State({'type': 'words-store', 'key': 3}, 'data')
)


app.clientside_callback(
    """
    function(data, word) {
        if(data) {
            var outputs = [];
            var count = 0;
            for(var i=0; i<word.length; i++) {
                count += 1;
                outputs.push(word[i]);      
            }
            for(var i=count; i<5; i++) {
                outputs.push('');
            }
            return outputs;
        }
    }
    """,
    [Output('word-4-letter-0', 'children'),
     Output('word-4-letter-1', 'children'),
     Output('word-4-letter-2', 'children'),
     Output('word-4-letter-3', 'children'),
     Output('word-4-letter-4', 'children')],
    Input({'type': 'word-update', 'key': 4}, 'data'),
    State({'type': 'words-store', 'key': 4}, 'data')
)


app.clientside_callback(
    """
    function(data, word) {
        if(data) {
            var outputs = [];
            var count = 0;
            for(var i=0; i<word.length; i++) {
                count += 1;
                outputs.push(word[i]);      
            }
            for(var i=count; i<5; i++) {
                outputs.push('');
            }
            return outputs;
        }
    }
    """,
    [Output('word-5-letter-0', 'children'),
     Output('word-5-letter-1', 'children'),
     Output('word-5-letter-2', 'children'),
     Output('word-5-letter-3', 'children'),
     Output('word-5-letter-4', 'children')],
    Input({'type': 'word-update', 'key': 5}, 'data'),
    State({'type': 'words-store', 'key': 5}, 'data')
)


@app.callback(
    [Output('word-0-letter-0-card', 'className'), Output('word-0-letter-1-card', 'className'),
     Output('word-0-letter-2-card', 'className'), Output('word-0-letter-3-card', 'className'),
     Output('word-0-letter-4-card', 'className')],
    Input({'type': 'word-evaluated', 'key': 0}, 'data'),
    State('evaluations-store', 'data')
)
def update_word_0(update_data, evaluations):
    if update_data is None or len(evaluations) == 0:
        raise PreventUpdate()
    output_classes = get_output_classes(evaluations[0])
    return output_classes


@app.callback(
    [Output('word-1-letter-0-card', 'className'), Output('word-1-letter-1-card', 'className'),
     Output('word-1-letter-2-card', 'className'), Output('word-1-letter-3-card', 'className'),
     Output('word-1-letter-4-card', 'className')],
    Input({'type': 'word-evaluated', 'key': 1}, 'data'),
    State('evaluations-store', 'data')
)
def update_word_1(update_data, evaluations):
    if update_data is None or len(evaluations) < 2:
        raise PreventUpdate()
    output_classes = get_output_classes(evaluations[1])
    return output_classes


@app.callback(
    [Output('word-2-letter-0-card', 'className'), Output('word-2-letter-1-card', 'className'),
     Output('word-2-letter-2-card', 'className'), Output('word-2-letter-3-card', 'className'),
     Output('word-2-letter-4-card', 'className')],
    Input({'type': 'word-evaluated', 'key': 2}, 'data'),
    State('evaluations-store', 'data')
)
def update_word_2(update_data, evaluations):
    if update_data is None or len(evaluations) < 3:
        raise PreventUpdate()
    output_classes = get_output_classes(evaluations[2])
    return output_classes


@app.callback(
    [Output('word-3-letter-0-card', 'className'), Output('word-3-letter-1-card', 'className'),
     Output('word-3-letter-2-card', 'className'), Output('word-3-letter-3-card', 'className'),
     Output('word-3-letter-4-card', 'className')],
    Input({'type': 'word-evaluated', 'key': 3}, 'data'),
    State('evaluations-store', 'data')
)
def update_word_3(update_data, evaluations):
    if update_data is None or len(evaluations) < 4:
        raise PreventUpdate()
    output_classes = get_output_classes(evaluations[3])
    return output_classes


@app.callback(
    [Output('word-4-letter-0-card', 'className'), Output('word-4-letter-1-card', 'className'),
     Output('word-4-letter-2-card', 'className'), Output('word-4-letter-3-card', 'className'),
     Output('word-4-letter-4-card', 'className')],
    Input({'type': 'word-evaluated', 'key': 4}, 'data'),
    State('evaluations-store', 'data')
)
def update_word_4(update_data, evaluations):
    if update_data is None or len(evaluations) < 5:
        raise PreventUpdate()
    output_classes = get_output_classes(evaluations[4])
    return output_classes


@app.callback(
    [Output('word-5-letter-0-card', 'className'), Output('word-5-letter-1-card', 'className'),
     Output('word-5-letter-2-card', 'className'), Output('word-5-letter-3-card', 'className'),
     Output('word-5-letter-4-card', 'className')],
    Input({'type': 'word-evaluated', 'key': 5}, 'data'),
    State('evaluations-store', 'data')
)
def update_word_5(update_data, evaluations):
    if update_data is None or len(evaluations) < 6:
        raise PreventUpdate()
    output_classes = get_output_classes(evaluations[5])
    return output_classes

import dash
from dash import html, Output, Input, State
from dash.exceptions import PreventUpdate

from app import app
from word import grid_layout
from keyboard import keyboard_layout


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname'),
               dash.dependencies.Input('url', 'search')])
def display_page(pathname, search):
    return html.Div([grid_layout(), keyboard_layout()])


def _get_query_params(params_str):
    params_list = params_str.split('&')
    params = dict()
    for param in params_list:
        key_value_list = param.split('=')
        if len(key_value_list) >= 2:
            params[key_value_list[0].replace('?', '')] = key_value_list[1]
    return params


@app.callback(
    [Output('word-{}-letter-{}'.format(x, y), 'children') for x in range(6) for y in range(5)],
    Input('state-store', 'data')
)
def state_changed(state_data):
    words = state_data['words']
    outputs = []
    if len(words) > 0:
        count = 0
        for word in words:
            for letter in word:
                count += 1
                outputs.append(letter)
        for i in range(count, 30):
            outputs.append('')
        return outputs

    raise PreventUpdate()


@app.callback(
    [Output('evaluation-store', 'data'), [Output('word-{}-letter-{}-card'.format(x, y), 'className') for x in range(6) for y in range(5)]],
    Input('evaluation-trigger', 'data'),
    [State('evaluation-store', 'data')]
)
def evaluate(word_to_evaluate, evaluations):
    if word_to_evaluate is None:
        raise PreventUpdate()

    evaluation_result = 'GGY__'
    evaluations.append(evaluation_result)
    output_classes = []
    if len(evaluations) > 0:
        for w in evaluations:
            for l in w:
                if l == 'G':
                    class_name = 'green-card'
                elif l == 'Y':
                    class_name = 'yellow-card'
                else:
                    class_name = 'gray-card'
                output_classes.append(class_name)

    for i in range(len(evaluations), 6):
        for j in range(5):
            output_classes.append('letter-card')

    return [evaluations, output_classes]


@app.callback(
    [Output('state-store', 'data'), Output('evaluation-trigger', 'data')],
    Input('action-store', 'data'),
    State('state-store', 'data')
)
def action_callback(input, state_data):

    if input is not None:
        word_to_evaluate = None
        current_word = state_data['current_word']
        current_letter = state_data['current_letter']
        words = state_data['words']

        if current_word > 5:
            raise PreventUpdate()

        if len(input) == 1:
            if current_letter >= 5:
                raise PreventUpdate()
            if len(words) == 0:
                words = ['']
            new_word = words[current_word] + input
            words[current_word] = new_word
            current_letter += 1

        elif input == 'backspace':
            if len(words) == 0 or current_letter == 0:
                raise PreventUpdate()
            new_word = words[current_word][:-1]
            words[current_word] = new_word
            current_letter -= 1

        elif input == 'enter':
            if current_letter != 5:
                raise PreventUpdate()
            word_to_evaluate = words[current_word]
            current_word += 1
            current_letter = 0
            words.append('')

        print(words)
        return [{'current_word': current_word, 'current_letter': current_letter, 'words': words}, word_to_evaluate]

    raise PreventUpdate()


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=True)

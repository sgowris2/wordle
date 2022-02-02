import dash_bootstrap_components as dbc
from dash import html, Output, Input
from dash.exceptions import PreventUpdate

from app import app


def grid_layout():
    return html.Div([
        word_layout(0),
        word_layout(1),
        word_layout(2),
        word_layout(3),
        word_layout(4),
        word_layout(5)
    ],
        className='word-grid'
    )


def word_layout(word_no):
    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody([' '],
                                         id='word-{}-letter-{}'.format(word_no, 0),
                                         className='letter-body')
                        ],
                        id='word-{}-letter-{}-card'.format(word_no, 0),
                        className='letter-card')],
                className='letter-column'),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody([' '],
                                         id='word-{}-letter-{}'.format(word_no, 1),
                                         className='letter-body')
                        ],
                        id='word-{}-letter-{}-card'.format(word_no, 1),
                        className='letter-card')],
                className='letter-column'),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody([' '],
                                         id='word-{}-letter-{}'.format(word_no, 2),
                                         className='letter-body')
                        ],
                        id='word-{}-letter-{}-card'.format(word_no, 2),
                        className='letter-card')],
                className='letter-column'),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody([' '],
                                         id='word-{}-letter-{}'.format(word_no, 3),
                                         className='letter-body')
                        ],
                        id='word-{}-letter-{}-card'.format(word_no, 3),
                        className='letter-card')],
                className='letter-column'),
            dbc.Col(
                [dbc.Card(
                    [
                        dbc.CardBody([' '],
                                     id='word-{}-letter-{}'.format(word_no, 4),
                                     className='letter-body')
                    ],
                    id='word-{}-letter-{}-card'.format(word_no, 4),
                    className='letter-card')],
                className='letter-column')
        ],
        className='word-row',
        id='word-{}'.format(word_no)
    )


def message_box_layout():
    layout = dbc.Toast(id='message-box', is_open=False, className='message-box')
    return layout


@app.callback(
    [Output('word-{}-letter-{}'.format(x, y), 'children') for x in range(6) for y in range(5)],
    Input('state-store', 'data')
)
def words_letters_changed(state_data):
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
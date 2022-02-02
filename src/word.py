import dash_bootstrap_components as dbc
from dash import html
from app import app
from dash import Input, Output, State
from dash.exceptions import PreventUpdate


def grid_layout():
    return html.Div([
        word_layout(0),
        word_layout(1),
        word_layout(2),
        word_layout(3),
        word_layout(4),
        word_layout(5)
    ],
        className='grid'
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

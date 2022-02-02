import dash_bootstrap_components as dbc
from dash import html
from app import app
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime


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


def evaluate_word(word):
    todays_word = get_todays_word()
    result = []
    for i in range(5):
        if word[i] == todays_word[i]:
            result.append('G')
        elif word[i] in todays_word:
            result.append('Y')
        else:
            result.append('_')
    return result


def get_todays_word():
    date = get_todays_date()
    assigned_words = get_assigned_words()
    if date not in assigned_words:
        assign_new_word(date)
        assigned_words = get_assigned_words()
    return assigned_words[date]


def get_assigned_words():
    return {'2022-02-02': 'HELLO'}


def assign_new_word(date):
    return {date: 'WORLD'}


def get_todays_date():
    return datetime.now().isoformat().split('T')[0]
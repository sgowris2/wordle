import json
from datetime import datetime
from random import randint

import dash_bootstrap_components as dbc
from dash import html


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


def evaluate_word(word):

    todays_word = get_todays_word()
    result = []
    guessed_letters = []

    for i in range(5):
        guessed_letters.append(word[i])
        if word[i] == todays_word[i]:
            result.append('G')
        elif word[i] in todays_word:
            result.append('Y')
        else:
            result.append('_')

    yellow_letter_indices = [x for x in range(5) if result[x] == 'Y']
    green_letter_indices = [x for x in range(5) if result[x] == 'G']
    remaining_letters = [todays_word[x] for x in range(5) if x not in green_letter_indices]

    for i in yellow_letter_indices:
        letter = word[i]
        if letter not in remaining_letters:
            result[i] = '_'
        else:
            remaining_letters[remaining_letters.index(letter)] = '.'

    return result


def get_todays_word():
    date: str = get_todays_date()
    assigned_words = get_assigned_words_dict()
    if date not in assigned_words:
        assign_new_word(date)
        assigned_words = get_assigned_words_dict()
    return assigned_words[date]


def get_assigned_words_dict() -> dict:
    with open('assigned_words.json', 'r') as f:
        words_dict = json.load(f)
    return words_dict


def assign_new_word(date: str):
    words_list = get_words_list()
    assigned_words_dict = get_assigned_words_dict()
    assigned_words_list = list(assigned_words_dict.values())
    while True:
        index = randint(0, len(words_list))
        new_word = str.upper(words_list[index]).strip()
        if new_word not in assigned_words_list:
            break
    assigned_words_dict[date] = new_word

    with open('assigned_words.json', 'w') as f:
        json.dump(assigned_words_dict, f)


def get_words_list():
    with open('words.txt', 'r') as f:
        words = f.readlines()
    return words


def get_todays_date() -> str:
    return datetime.now().isoformat().split('T')[0]

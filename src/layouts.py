import dash_bootstrap_components as dbc
from dash import html


def grid_layout():
    return html.Div([
        word_layout(),
        word_layout(),
        word_layout(),
        word_layout(),
        word_layout(),
        word_layout()
    ],
        className='grid'
    )


def word_layout():
    return dbc.Row(
        [
            dbc.Col([dbc.Card([dbc.CardBody([' '])], className='letter-card')], className='letter-column'),
            dbc.Col([dbc.Card([dbc.CardBody([' '])], className='letter-card')], className='letter-column'),
            dbc.Col([dbc.Card([dbc.CardBody([' '])], className='letter-card')], className='letter-column'),
            dbc.Col([dbc.Card([dbc.CardBody([' '])], className='letter-card')], className='letter-column'),
            dbc.Col([dbc.Card([dbc.CardBody([' '])], className='letter-card')], className='letter-column')
        ],
        className='word-row'
    )


def keyboard_layout():
    return html.Div(
        [
            dbc.Row(
                [
                    html.Button('Q', className='keyboard-button'),
                    html.Button('W', className='keyboard-button'),
                    html.Button('E', className='keyboard-button'),
                    html.Button('R', className='keyboard-button'),
                    html.Button('T', className='keyboard-button'),
                    html.Button('Y', className='keyboard-button'),
                    html.Button('U', className='keyboard-button'),
                    html.Button('I', className='keyboard-button'),
                    html.Button('O', className='keyboard-button'),
                    html.Button('P', className='keyboard-button')
                ],
                className='keyboard-row'
            ),
            dbc.Row(
                [
                    html.Div(className='spacer-half'),
                    html.Button('A', className='keyboard-button'),
                    html.Button('S', className='keyboard-button'),
                    html.Button('D', className='keyboard-button'),
                    html.Button('F', className='keyboard-button'),
                    html.Button('G', className='keyboard-button'),
                    html.Button('H', className='keyboard-button'),
                    html.Button('J', className='keyboard-button'),
                    html.Button('K', className='keyboard-button'),
                    html.Button('L', className='keyboard-button'),
                    html.Div(className='spacer-half')
                ],
                className='keyboard-row'
            ),
            dbc.Row(
                [
                    html.Button('Enter', className='keyboard-button one-and-half'),
                    html.Button('Z', className='keyboard-button'),
                    html.Button('X', className='keyboard-button'),
                    html.Button('C', className='keyboard-button'),
                    html.Button('V', className='keyboard-button'),
                    html.Button('B', className='keyboard-button'),
                    html.Button('N', className='keyboard-button'),
                    html.Button('M', className='keyboard-button'),
                    html.Button('',
                                className='bi bi-backspace keyboard-button one-and-half',
                                style={'font-size': '28px'}),
                ],
                className='keyboard-row'
            )
        ],
        className='keyboard'
    )

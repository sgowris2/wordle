import dash_bootstrap_components as dbc
from dash import html, callback_context
from dash import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from app import app
import json


def keyboard_layout():
    return html.Div(
        [
            dbc.Row(
                [
                    html.Button('Q', id={'type': 'keybutton', 'index': 'Q'}, className='keyboard-button'),
                    html.Button('W', id={'type': 'keybutton', 'index': 'W'}, className='keyboard-button'),
                    html.Button('E', id={'type': 'keybutton', 'index': 'E'}, className='keyboard-button'),
                    html.Button('R', id={'type': 'keybutton', 'index': 'R'}, className='keyboard-button'),
                    html.Button('T', id={'type': 'keybutton', 'index': 'T'}, className='keyboard-button'),
                    html.Button('Y', id={'type': 'keybutton', 'index': 'Y'}, className='keyboard-button'),
                    html.Button('U', id={'type': 'keybutton', 'index': 'U'}, className='keyboard-button'),
                    html.Button('I', id={'type': 'keybutton', 'index': 'I'}, className='keyboard-button'),
                    html.Button('O', id={'type': 'keybutton', 'index': 'O'}, className='keyboard-button'),
                    html.Button('P', id={'type': 'keybutton', 'index': 'P'}, className='keyboard-button')
                ],
                className='keyboard-row'
            ),
            dbc.Row(
                [
                    html.Div(className='spacer-half'),
                    html.Button('A', id={'type': 'keybutton', 'index': 'A'}, className='keyboard-button'),
                    html.Button('S', id={'type': 'keybutton', 'index': 'S'}, className='keyboard-button'),
                    html.Button('D', id={'type': 'keybutton', 'index': 'D'}, className='keyboard-button'),
                    html.Button('F', id={'type': 'keybutton', 'index': 'F'}, className='keyboard-button'),
                    html.Button('G', id={'type': 'keybutton', 'index': 'G'}, className='keyboard-button'),
                    html.Button('H', id={'type': 'keybutton', 'index': 'H'}, className='keyboard-button'),
                    html.Button('J', id={'type': 'keybutton', 'index': 'J'}, className='keyboard-button'),
                    html.Button('K', id={'type': 'keybutton', 'index': 'K'}, className='keyboard-button'),
                    html.Button('L', id={'type': 'keybutton', 'index': 'L'}, className='keyboard-button'),
                    html.Div(className='spacer-half')
                ],
                className='keyboard-row'
            ),
            dbc.Row(
                [
                    html.Button('Enter', id={'type': 'keybutton', 'index': 'enter'}, className='keyboard-button one-and-half'),
                    html.Button('Z', id={'type': 'keybutton', 'index': 'Z'}, className='keyboard-button'),
                    html.Button('X', id={'type': 'keybutton', 'index': 'X'}, className='keyboard-button'),
                    html.Button('C', id={'type': 'keybutton', 'index': 'C'}, className='keyboard-button'),
                    html.Button('V', id={'type': 'keybutton', 'index': 'V'}, className='keyboard-button'),
                    html.Button('B', id={'type': 'keybutton', 'index': 'B'}, className='keyboard-button'),
                    html.Button('N', id={'type': 'keybutton', 'index': 'N'}, className='keyboard-button'),
                    html.Button('M', id={'type': 'keybutton', 'index': 'M'}, className='keyboard-button'),
                    html.Button('',
                                id={'type': 'keybutton', 'index': 'backspace'},
                                className='bi bi-backspace keyboard-button one-and-half',
                                style={'font-size': '28px'}),
                ],
                className='keyboard-row'
            )
        ],
        className='keyboard'
    )


@app.callback(
    Output('action-store', 'data'),
    [Input({'type': 'keybutton', 'index': ALL}, 'n_clicks')],
)
def key_pressed(n_clicks_list):
    if callback_context.triggered is not None:
        value = callback_context.triggered[0]['value']
        if value is not None:
            property_json_str = callback_context.triggered[0]['prop_id'].split('.')[0]
            if len(property_json_str) > 0:
                triggered_key = json.loads(property_json_str)['index']
                return triggered_key
    raise PreventUpdate()

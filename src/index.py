import dash
from dash import html

from app import app
from keyboard import keyboard_layout
from word_grid import grid_layout, message_box_layout


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname'),
               dash.dependencies.Input('url', 'search')])
def display_page(pathname, search):
    return html.Div([grid_layout(), message_box_layout(), keyboard_layout()])


def _get_query_params(params_str):
    params_list = params_str.split('&')
    params = dict()
    for param in params_list:
        key_value_list = param.split('=')
        if len(key_value_list) >= 2:
            params[key_value_list[0].replace('?', '')] = key_value_list[1]
    return params


if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False)

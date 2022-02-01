import dash
from dash import dcc
from dash import html

from app import app
from layouts import grid_layout, keyboard_layout

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(
        children=[
            html.H1('WORDLE', className='display-6 wordle-title'),
            html.Hr(className='title-sep')
        ],
        className='page-header'),
    html.Div(id='page-content', children=[], className='page-content'),
])


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


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=True)

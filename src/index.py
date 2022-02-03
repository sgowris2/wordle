from app import app


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

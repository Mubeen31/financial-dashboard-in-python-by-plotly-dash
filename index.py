import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data").resolve()

data = pd.read_csv(DATA_PATH.joinpath('financial_data.csv'))
print(data.dtypes)

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
meta_tags = [{"name": "viewport", "content": "width=device-width"}]
external_stylesheets = [meta_tags, font_awesome]

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src = app.get_asset_url('statistics.png'),
                     style = {'height': '30px'},
                     className = 'title_image'
                     ),
            html.H6('Financial Dashboard',
                    style = {'color': '#D35940'},
                    className = 'title'
                    ),
        ], className = 'logo_title'),

        html.Div([
            html.P('Select Month',
                   style = {'color': '#D35940'},
                   className = 'drop_down_list_title'
                   ),
            dcc.Dropdown(id = 'select_month',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Mar',
                         placeholder = 'Select Month',
                         options = [{'label': c, 'value': c}
                                    for c in data['months'].unique()],
                         className = 'drop_down_list'),
        ], className = 'title_drop_down_list'),
    ], className = 'title_and_drop_down_list'),

html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.P('Accounts Receivable',
                           className = 'format_text')
                ], className = 'accounts_receivable1'),
                html.Div([
                    html.Div(id = 'accounts_receivable_value',
                             className = 'numeric_value')
                ], className = 'accounts_receivable2')
            ], className = 'accounts_receivable_column'),
            html.Div([
                html.Div([
                    html.P('Accounts Payable',
                           className = 'format_text')
                ], className = 'accounts_payable1'),
                html.Div([

                ], className = 'accounts_payable2')
            ], className = 'accounts_payable_column'),
        ], className = 'receivable_payable_column'),

        html.Div([
            html.Div([
                html.Div([
                    html.P('Income',
                           className = 'format_text')
                ], className = 'income1'),
                html.Div([

                ], className = 'income2')
            ], className = 'income_column'),
            html.Div([
                html.Div([
                    html.P('Expenses',
                           className = 'format_text')
                ], className = 'expenses1'),
                html.Div([

                ], className = 'expenses2')
            ], className = 'expenses_column'),
        ], className = 'income_expenses_column'),
    ], className = 'first_row'),
    html.Div([
        html.Div([
            html.Div([
            ], className = 'first_left_circle'),
            html.Div([
            ], className = 'second_left_circle'),
        ], className = 'first_second_left_column'),
    ], className = 'left_circle_row'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                ], className = 'first_right_circle'),
                html.Div([
                ], className = 'second_right_circle'),
            ], className = 'first_second_right_column'),
        ], className = 'right_circle_row'),

        html.Div([
            html.Div([
                html.Div([
                    html.P('Income Statement',
                           className = 'format_text')
                ], className = 'income_statement'),

                html.Div([

                ], className = 'income_statement_multiple_values'),
            ], className = 'income_statement_column1'),
            html.Div([

            ], className = 'net_profit'),
        ], className = 'net_profit1'),
    ], className = 'income_statement_row')
    ], className = 'f_row')
])


@app.callback(Output('accounts_receivable_value', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        accounts_receivable = filter_month['accounts receivable'].iloc[0]

        return [
            html.P('${0:,.0f}'.format(accounts_receivable),
                   ),
        ]


if __name__ == "__main__":
    app.run_server(debug = True)
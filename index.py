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

data['pct_accounts_receivable'] = (data['accounts receivable'].pct_change()) * 100
data['pct_accounts_receivable'] = data['pct_accounts_receivable'].fillna(0)

data['pct_accounts_payable'] = (data['accounts payable'].pct_change()) * 100
data['pct_accounts_payable'] = data['pct_accounts_payable'].fillna(0)

data['pct_income'] = (data['income'].pct_change()) * 100
data['pct_income'] = data['pct_income'].fillna(0)

data['expenses'] = data['cost of goods sold'] + data['total operating expenses']
data['pct_expenses'] = (data['expenses'].pct_change()) * 100
data['pct_expenses'] = data['pct_expenses'].fillna(0)

data['gross profit'] = data['income'] - data['cost of goods sold']

data['operating profit (EBIT)'] = data['gross profit'] - data['total operating expenses']

data['net profit'] = data['operating profit (EBIT)'] - data['Taxes']

data['net profit margin %'] = (data['net profit'] / data['income']) * 100

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
                    html.Div(id = 'accounts_payable_value',
                             className = 'numeric_value')
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
                    html.Div(id = 'income_value',
                             className = 'numeric_value')
                ], className = 'income2')
            ], className = 'income_column'),
            html.Div([
                html.Div([
                    html.P('Expenses',
                           className = 'format_text')
                ], className = 'expenses1'),
                html.Div([
                    html.Div(id = 'expenses_value',
                             className = 'numeric_value')
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
        pct_accounts_receivable = filter_month['pct_accounts_receivable'].iloc[0]

        if pct_accounts_receivable > 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(accounts_receivable),
                           ),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(pct_accounts_receivable),
                                   className = 'indicator1'),
                            html.Div([
                                html.I(className = "fas fa-caret-up",
                                       style = {"font-size": "25px",
                                                'color': '#00B050'},
                                       ),
                            ], className = 'value_indicator'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]
        elif pct_accounts_receivable < 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(accounts_receivable),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_accounts_receivable),
                                   className = 'indicator2'),
                            html.Div([
                                html.I(className = "fas fa-caret-down",
                                       style = {"font-size": "25px",
                                                'color': '#FF3399'},
                                       ),
                            ], className = 'value_indicator'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]
        elif pct_accounts_receivable == 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(accounts_receivable),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_accounts_receivable),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]


@app.callback(Output('accounts_payable_value', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        accounts_payable = filter_month['accounts payable'].iloc[0]
        pct_accounts_payable = filter_month['pct_accounts_payable'].iloc[0]

        if pct_accounts_payable > 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(accounts_payable),
                           ),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(pct_accounts_payable),
                                   className = 'indicator1'),
                            html.Div([
                                html.I(className = "fas fa-caret-up",
                                       style = {"font-size": "25px",
                                                'color': '#00B050'},
                                       ),
                            ], className = 'value_indicator'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]
        elif pct_accounts_payable < 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(accounts_payable),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_accounts_payable),
                                   className = 'indicator2'),
                            html.Div([
                                html.I(className = "fas fa-caret-down",
                                       style = {"font-size": "25px",
                                                'color': '#FF3399'},
                                       ),
                            ], className = 'value_indicator'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]
        elif pct_accounts_payable == 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(accounts_payable),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_accounts_payable),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]


@app.callback(Output('income_value', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        income = filter_month['income'].iloc[0]
        pct_income = filter_month['pct_income'].iloc[0]

        if pct_income > 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(income),
                           ),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(pct_income),
                                   className = 'indicator1'),
                            html.Div([
                                html.I(className = "fas fa-caret-up",
                                       style = {"font-size": "25px",
                                                'color': '#00B050'},
                                       ),
                            ], className = 'value_indicator'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]
        elif pct_income < 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(income),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_income),
                                   className = 'indicator2'),
                            html.Div([
                                html.I(className = "fas fa-caret-down",
                                       style = {"font-size": "25px",
                                                'color': '#FF3399'},
                                       ),
                            ], className = 'value_indicator'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]
        elif pct_income == 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(income),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_income),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]


@app.callback(Output('expenses_value', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        expenses = filter_month['expenses'].iloc[0]
        pct_expenses = filter_month['pct_expenses'].iloc[0]

        if pct_expenses > 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(expenses),
                           ),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(pct_expenses),
                                   className = 'indicator1'),
                            html.Div([
                                html.I(className = "fas fa-caret-up",
                                       style = {"font-size": "25px",
                                                'color': '#00B050'},
                                       ),
                            ], className = 'value_indicator'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]
        elif pct_expenses < 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(expenses),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_expenses),
                                   className = 'indicator2'),
                            html.Div([
                                html.I(className = "fas fa-caret-down",
                                       style = {"font-size": "25px",
                                                'color': '#FF3399'},
                                       ),
                            ], className = 'value_indicator'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]
        elif pct_expenses == 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(expenses),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_expenses),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]


if __name__ == "__main__":
    app.run_server(debug = True)
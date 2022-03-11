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
data['pct_gross_profit'] = (data['gross profit'].pct_change()) * 100
data['pct_gross_profit'] = data['pct_gross_profit'].fillna(0)

data['pct_total_operating_expenses'] = (data['total operating expenses'].pct_change()) * 100
data['pct_total_operating_expenses'] = data['pct_total_operating_expenses'].fillna(0)

data['operating profit (EBIT)'] = data['gross profit'] - data['total operating expenses']
data['pct_operating_profit_(EBIT)'] = (data['operating profit (EBIT)'].pct_change()) * 100
data['pct_operating_profit_(EBIT)'] = data['pct_operating_profit_(EBIT)'].fillna(0)

data['pct_taxes'] = (data['Taxes'].pct_change()) * 100
data['pct_taxes'] = data['pct_taxes'].fillna(0)

data['pct_quick_ratio'] = (data['quick ratio'].pct_change()) * 100
data['pct_quick_ratio'] = data['pct_quick_ratio'].fillna(0)

data['pct_current_ratio'] = (data['current ratio'].pct_change()) * 100
data['pct_current_ratio'] = data['pct_current_ratio'].fillna(0)

data['pct_cash_at_eom'] = (data['cash at eom'].pct_change()) * 100
data['pct_cash_at_eom'] = data['pct_cash_at_eom'].fillna(0)

data['net profit'] = data['operating profit (EBIT)'] - data['Taxes']
data['pct_net_profit'] = (data['net profit'].pct_change()) * 100
data['pct_net_profit'] = data['pct_net_profit'].fillna(0)

data['net profit margin %'] = (data['net profit'] / data['income']) * 100
data['pct_net_profit_margin_%'] = (data['net profit margin %'].pct_change()) * 100
data['pct_net_profit_margin_%'] = data['pct_net_profit_margin_%'].fillna(0)

data['income budget %'] = (data['income'] / data['income budget']) * 100
data['pct_income_budget_%'] = (data['income budget %'].pct_change()) * 100
data['pct_income_budget_%'] = data['pct_income_budget_%'].fillna(0)

data['expense budget %'] = (data['expenses'] / data['expense budget']) * 100
data['pct_expense_budget_%'] = (data['expense budget %'].pct_change()) * 100
data['pct_expense_budget_%'] = data['pct_expense_budget_%'].fillna(0)

data['pct_cost_of_goods_sold'] = (data['cost of goods sold'].pct_change()) * 100
data['pct_cost_of_goods_sold'] = data['pct_cost_of_goods_sold'].fillna(0)

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
                    html.Div([
                    ], className = 'first_left_circle'),
                    html.Div([
                        html.Div(id = 'second_left_circle'),
                    ], className = 'second_left_circle'),
                ], className = 'first_second_left_column'),
            ], className = 'left_circle_row'),
            dcc.Graph(id = 'chart1',
                      config = {'displayModeBar': False},
                      className = 'donut_chart_size'),
        ], className = 'text_and_chart'),

        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                    ], className = 'first_right_circle'),
                    html.Div([
                        html.Div(id = 'second_right_circle'),
                    ], className = 'second_right_circle'),
                ], className = 'first_second_right_column'),
            ], className = 'right_circle_row'),
            dcc.Graph(id = 'chart2',
                      config = {'displayModeBar': False},
                      className = 'donut_chart_size'),

            html.Div([
                html.Div([
                    html.Div([
                        html.P('Income Statement',
                               className = 'format_text')
                    ], className = 'income_statement'),

                    html.Div([
                        html.Div([
                            html.Div([
                                html.P('Income',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement1',
                                         className = 'income_statement1'),
                            ], className = 'income_statement_indicator_row1'),
                            html.Div([
                                html.P('Cost of Goods Sold',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement2',
                                         className = 'income_statement1')
                            ], className = 'income_statement_indicator_row2'),
                            html.Hr(className = 'bottom_border'),
                            html.Div([
                                html.P('Gross Profit',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement3',
                                         className = 'income_statement1'),
                            ], className = 'income_statement_indicator_row3'),
                            html.Div([
                                html.P('Total Operating Expenses',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement4',
                                         className = 'income_statement1')
                            ], className = 'income_statement_indicator_row4'),
                            html.Hr(className = 'bottom_border'),
                            html.Div([
                                html.P('Operating Profit (EBIT)',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement5',
                                         className = 'income_statement1'),
                            ], className = 'income_statement_indicator_row5'),
                            html.Div([
                                html.P('Taxes',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement6',
                                         className = 'income_statement1')
                            ], className = 'income_statement_indicator_row6'),
                        ], className = 'in_state_column')
                    ], className = 'income_statement_multiple_values'),
                ], className = 'income_statement_column1'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.P('Net Profit',
                                   className = 'income_statement_title'
                                   ),
                            html.Div(id = 'income_statement7',
                                     className = 'income_statement1')
                        ], className = 'income_statement_indicator_row7'),
                    ], className = 'net_profit_column')
                ], className = 'net_profit'),
            ], className = 'net_profit1'),
        ], className = 'income_statement_row')
    ], className = 'f_row'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.P('Quick Ratio',
                               className = 'format_text')
                    ], className = 'accounts_receivable1'),
                    html.Div([
                        html.Div(id = 'quick_ratio_value',
                                 className = 'numeric_value')
                    ], className = 'accounts_receivable2')
                ], className = 'accounts_receivable_column'),
                html.Div([
                    html.Div([
                        html.P('Current Ratio',
                               className = 'format_text')
                    ], className = 'accounts_payable1'),
                    html.Div([
                        html.Div(id = 'current_ratio_value',
                                 className = 'numeric_value')
                    ], className = 'accounts_payable2')
                ], className = 'accounts_payable_column'),
            ], className = 'receivable_payable_column'),

            html.Div([
                html.Div([
                    html.Div([
                        html.P('Net Profit',
                               className = 'format_text')
                    ], className = 'income1'),
                    html.Div([
                        html.Div(id = 'net_profit_value',
                                 className = 'numeric_value')
                    ], className = 'income2')
                ], className = 'income_column'),
                html.Div([
                    html.Div([
                        html.P('Cash at EOM',
                               className = 'format_text')
                    ], className = 'expenses1'),
                    html.Div([
                        html.Div(id = 'cash_at_eom_value',
                                 className = 'numeric_value')
                    ], className = 'expenses2')
                ], className = 'expenses_column'),
            ], className = 'income_expenses_column'),
        ], className = 'first_row'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                    ], className = 'first_left_circle'),
                    html.Div([
                        html.Div(id = 'third_left_circle'),
                    ], className = 'second_left_circle'),
                ], className = 'first_second_left_column'),
            ], className = 'left_circle_row'),
            dcc.Graph(id = 'chart3',
                      config = {'displayModeBar': False},
                      className = 'donut_chart_size'),
        ], className = 'text_and_chart'),

        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                    ], className = 'first_right_circle'),
                    html.Div([
                        html.Div(id = 'fourth_right_circle'),
                    ], className = 'second_right_circle'),
                ], className = 'first_second_right_column'),
            ], className = 'right_circle_row'),
            dcc.Graph(id = 'chart4',
                      config = {'displayModeBar': False},
                      className = 'donut_chart_size'),

            #     html.Div([
            #         html.Div([
            #             html.Div([
            #                 html.P('Income Statement',
            #                        className = 'format_text')
            #             ], className = 'income_statement'),
            #
            #             html.Div([
            #                 html.Div([
            #                     html.Div([
            #                         html.P('Income',
            #                                className = 'income_statement_title'
            #                                ),
            #                         html.Div(id = 'income_statement1',
            #                                  className = 'income_statement1'),
            #                     ], className = 'income_statement_indicator_row1'),
            #                     html.Div([
            #                         html.P('Cost of Goods Sold',
            #                                className = 'income_statement_title'
            #                                ),
            #                         html.Div(id = 'income_statement2',
            #                                  className = 'income_statement1')
            #                     ], className = 'income_statement_indicator_row2'),
            #                     html.Hr(className = 'bottom_border'),
            #                     html.Div([
            #                         html.P('Gross Profit',
            #                                className = 'income_statement_title'
            #                                ),
            #                         html.Div(id = 'income_statement3',
            #                                  className = 'income_statement1'),
            #                     ], className = 'income_statement_indicator_row3'),
            #                     html.Div([
            #                         html.P('Total Operating Expenses',
            #                                className = 'income_statement_title'
            #                                ),
            #                         html.Div(id = 'income_statement4',
            #                                  className = 'income_statement1')
            #                     ], className = 'income_statement_indicator_row4'),
            #                     html.Hr(className = 'bottom_border'),
            #                     html.Div([
            #                         html.P('Operating Profit (EBIT)',
            #                                className = 'income_statement_title'
            #                                ),
            #                         html.Div(id = 'income_statement5',
            #                                  className = 'income_statement1'),
            #                     ], className = 'income_statement_indicator_row5'),
            #                     html.Div([
            #                         html.P('Taxes',
            #                                className = 'income_statement_title'
            #                                ),
            #                         html.Div(id = 'income_statement6',
            #                                  className = 'income_statement1')
            #                     ], className = 'income_statement_indicator_row6'),
            #                 ], className = 'in_state_column')
            #             ], className = 'income_statement_multiple_values'),
            #         ], className = 'income_statement_column1'),
            #         html.Div([
            #             html.Div([
            #                 html.Div([
            #                     html.P('Net Profit',
            #                            className = 'income_statement_title'
            #                            ),
            #                     html.Div(id = 'income_statement7',
            #                              className = 'income_statement1')
            #                 ], className = 'income_statement_indicator_row7'),
            #             ], className = 'net_profit_column')
            #         ], className = 'net_profit'),
            #     ], className = 'net_profit1'),
        ], className = 'income_statement_row')
    ], className = 'f_row'),
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


@app.callback(Output('second_left_circle', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        net_profit_margin_percentage = filter_month['net profit margin %'].iloc[0]
        pct_net_profit_margin_percentage = filter_month['pct_net_profit_margin_%'].iloc[0]

        if pct_net_profit_margin_percentage > 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Net Profit',
                               className = 'donut_chart_title'
                               ),
                        html.P('Margin %',
                               className = 'donut_chart_title1'
                               ),
                        html.P('{0:,.1f}%'.format(net_profit_margin_percentage),
                               className = 'net_profit_margin_percentage'),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(pct_net_profit_margin_percentage),
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
                ], className = 'inside_donut_chart_column'),
            ]

        if pct_net_profit_margin_percentage < 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Net Profit',
                               className = 'donut_chart_title'
                               ),
                        html.P('Margin %',
                               className = 'donut_chart_title1'
                               ),
                        html.P('{0:,.1f}%'.format(net_profit_margin_percentage),
                               className = 'net_profit_margin_percentage'),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_net_profit_margin_percentage),
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
                ], className = 'inside_donut_chart_column'),
            ]

        if pct_net_profit_margin_percentage == 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Net Profit',
                               className = 'donut_chart_title'
                               ),
                        html.P('Margin %',
                               className = 'donut_chart_title1'
                               ),
                        html.P('{0:,.1f}%'.format(net_profit_margin_percentage),
                               className = 'net_profit_margin_percentage'),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_net_profit_margin_percentage),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'inside_donut_chart_column'),
            ]


@app.callback(Output('chart1', 'figure'),
              [Input('select_month', 'value')])
def update_graph(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        net_profit_margin_percentage = filter_month['net profit margin %'].iloc[0]
        remaining_percentage_profit = 100 - (filter_month['net profit margin %'].iloc[0])
        colors = ['#B258D3', '#82FFFF']

    return {
        'data': [go.Pie(labels = ['', ''],
                        values = [net_profit_margin_percentage, remaining_percentage_profit],
                        marker = dict(colors = colors,
                                      # line=dict(color='#DEB340', width=2)
                                      ),
                        hoverinfo = 'skip',
                        textinfo = 'text',
                        hole = .7,
                        rotation = 90
                        )],

        'layout': go.Layout(
            plot_bgcolor = 'rgba(0,0,0,0)',
            paper_bgcolor = 'rgba(0,0,0,0)',
            margin = dict(t = 35, b = 0, r = 0, l = 0),
            showlegend = False,
            title = {'text': '',
                     'y': 0.95,
                     'x': 0.5,
                     'xanchor': 'center',
                     'yanchor': 'top'},
            titlefont = {'color': 'white',
                         'size': 15},
        ),

    }


@app.callback(Output('second_right_circle', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        income_budget_percentage = filter_month['income budget %'].iloc[0]
        pct_income_budget_percentage = filter_month['pct_income_budget_%'].iloc[0]

        if pct_income_budget_percentage > 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Income Budget %',
                               className = 'donut_chart_title'
                               ),
                        html.P('{0:,.1f}%'.format(income_budget_percentage),
                               className = 'net_profit_margin_percentage1'),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(pct_income_budget_percentage),
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
                ], className = 'inside_donut_chart_column'),
            ]

        if pct_income_budget_percentage < 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Income Budget %',
                               className = 'donut_chart_title'
                               ),
                        html.P('{0:,.1f}%'.format(income_budget_percentage),
                               className = 'net_profit_margin_percentage1'),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_income_budget_percentage),
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
                ], className = 'inside_donut_chart_column'),
            ]

        if pct_income_budget_percentage == 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Income Budget %',
                               className = 'donut_chart_title'
                               ),
                        html.P('{0:,.1f}%'.format(income_budget_percentage),
                               className = 'net_profit_margin_percentage1'),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_income_budget_percentage),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'inside_donut_chart_column'),
            ]


@app.callback(Output('chart2', 'figure'),
              [Input('select_month', 'value')])
def update_graph(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        income_budget_percentage = filter_month['income budget %'].iloc[0]
        remaining_income_budget_percentage = 100 - (filter_month['income budget %'].iloc[0])
        colors = ['#63A0CC', '#82FFFF']

    return {
        'data': [go.Pie(labels = ['', ''],
                        values = [income_budget_percentage, remaining_income_budget_percentage],
                        marker = dict(colors = colors,
                                      # line=dict(color='#DEB340', width=2)
                                      ),
                        hoverinfo = 'skip',
                        textinfo = 'text',
                        hole = .7,
                        rotation = 360
                        )],

        'layout': go.Layout(
            plot_bgcolor = 'rgba(0,0,0,0)',
            paper_bgcolor = 'rgba(0,0,0,0)',
            autosize = True,
            margin = dict(t = 35, b = 0, r = 0, l = 0),
            showlegend = False,
            title = {'text': '',
                     'y': 0.95,
                     'x': 0.5,
                     'xanchor': 'center',
                     'yanchor': 'top'},
            titlefont = {'color': 'white',
                         'size': 15},
        ),

    }


@app.callback(Output('income_statement1', 'children'),
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
                       className = 'monthly_value'),
                html.Div([
                    html.P('+{0:,.1f}%'.format(pct_income),
                           className = 'indicator1'),
                    html.Div([
                        html.I(className = "fas fa-caret-up",
                               style = {"font-size": "25px",
                                        'color': '#00B050'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]
    elif pct_income < 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(income),
                       className = 'monthly_value'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_income),
                           className = 'indicator2'),
                    html.Div([
                        html.I(className = "fas fa-caret-down",
                               style = {"font-size": "25px",
                                        'color': '#FF3399'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]

    elif pct_income == 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(income),
                       className = 'monthly_value'),

                html.Div([
                    html.P('{0:,.1f}%'.format(pct_income),
                           className = 'indicator2'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]


@app.callback(Output('income_statement2', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        cost_of_goods_sold = filter_month['cost of goods sold'].iloc[0]
        pct_cost_of_goods_sold = filter_month['pct_cost_of_goods_sold'].iloc[0]

    if pct_cost_of_goods_sold > 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(cost_of_goods_sold),
                       className = 'monthly_value'),
                html.Div([
                    html.P('+{0:,.1f}%'.format(pct_cost_of_goods_sold),
                           className = 'indicator1'),
                    html.Div([
                        html.I(className = "fas fa-caret-up",
                               style = {"font-size": "25px",
                                        'color': '#00B050'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]
    elif pct_cost_of_goods_sold < 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(cost_of_goods_sold),
                       className = 'monthly_value'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_cost_of_goods_sold),
                           className = 'indicator2'),
                    html.Div([
                        html.I(className = "fas fa-caret-down",
                               style = {"font-size": "25px",
                                        'color': '#FF3399'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]

    elif pct_cost_of_goods_sold == 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(cost_of_goods_sold),
                       className = 'monthly_value'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_cost_of_goods_sold),
                           className = 'indicator2'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]


@app.callback(Output('income_statement3', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        gross_profit = filter_month['gross profit'].iloc[0]
        pct_gross_profit = filter_month['pct_gross_profit'].iloc[0]

    if pct_gross_profit > 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(gross_profit),
                       className = 'monthly_value'),
                html.Div([
                    html.P('+{0:,.1f}%'.format(pct_gross_profit),
                           className = 'indicator1'),
                    html.Div([
                        html.I(className = "fas fa-caret-up",
                               style = {"font-size": "25px",
                                        'color': '#00B050'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]
    elif pct_gross_profit < 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(gross_profit),
                       className = 'monthly_value'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_gross_profit),
                           className = 'indicator2'),
                    html.Div([
                        html.I(className = "fas fa-caret-down",
                               style = {"font-size": "25px",
                                        'color': '#FF3399'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]

    elif pct_gross_profit == 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(gross_profit),
                       className = 'monthly_value'),

                html.Div([
                    html.P('{0:,.1f}%'.format(pct_gross_profit),
                           className = 'indicator2'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]


@app.callback(Output('income_statement4', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        total_operating_expenses = filter_month['total operating expenses'].iloc[0]
        pct_total_operating_expenses = filter_month['pct_total_operating_expenses'].iloc[0]

    if pct_total_operating_expenses > 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(total_operating_expenses),
                       className = 'monthly_value'),
                html.Div([
                    html.P('+{0:,.1f}%'.format(pct_total_operating_expenses),
                           className = 'indicator1'),
                    html.Div([
                        html.I(className = "fas fa-caret-up",
                               style = {"font-size": "25px",
                                        'color': '#00B050'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]
    elif pct_total_operating_expenses < 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(total_operating_expenses),
                       className = 'monthly_value'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_total_operating_expenses),
                           className = 'indicator2'),
                    html.Div([
                        html.I(className = "fas fa-caret-down",
                               style = {"font-size": "25px",
                                        'color': '#FF3399'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]

    elif pct_total_operating_expenses == 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(total_operating_expenses),
                       className = 'monthly_value'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_total_operating_expenses),
                           className = 'indicator2'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]


@app.callback(Output('income_statement5', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        operating_profit_EBIT = filter_month['operating profit (EBIT)'].iloc[0]
        pct_operating_profit_EBIT = filter_month['pct_operating_profit_(EBIT)'].iloc[0]

    if operating_profit_EBIT < 0 and pct_operating_profit_EBIT < 0:
        return [
            html.Div([
                html.P('(${0:,.0f})'.format(abs(operating_profit_EBIT)),
                       className = 'monthly_value1'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_operating_profit_EBIT),
                           className = 'indicator2'),
                    html.Div([
                        html.I(className = "fas fa-caret-down",
                               style = {"font-size": "25px",
                                        'color': '#FF3399'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]
    if operating_profit_EBIT < 0 and pct_operating_profit_EBIT > 0:
        return [
            html.Div([
                html.P('(${0:,.0f})'.format(abs(operating_profit_EBIT)),
                       className = 'monthly_value1'),
                html.Div([
                    html.P('+{0:,.1f}%'.format(pct_operating_profit_EBIT),
                           className = 'indicator1'),
                    html.Div([
                        html.I(className = "fas fa-caret-up",
                               style = {"font-size": "25px",
                                        'color': '#00B050'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]
    if pct_operating_profit_EBIT > 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(operating_profit_EBIT),
                       className = 'monthly_value'),
                html.Div([
                    html.P('+{0:,.1f}%'.format(pct_operating_profit_EBIT),
                           className = 'indicator1'),
                    html.Div([
                        html.I(className = "fas fa-caret-up",
                               style = {"font-size": "25px",
                                        'color': '#00B050'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]
    elif pct_operating_profit_EBIT < 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(operating_profit_EBIT),
                       className = 'monthly_value'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_operating_profit_EBIT),
                           className = 'indicator2'),
                    html.Div([
                        html.I(className = "fas fa-caret-down",
                               style = {"font-size": "25px",
                                        'color': '#FF3399'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]

    elif pct_operating_profit_EBIT == 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(operating_profit_EBIT),
                       className = 'monthly_value'),

                html.Div([
                    html.P('{0:,.1f}%'.format(pct_operating_profit_EBIT),
                           className = 'indicator2'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]


@app.callback(Output('income_statement6', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        taxes = filter_month['Taxes'].iloc[0]
        pct_taxes = filter_month['pct_taxes'].iloc[0]

    if pct_taxes > 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(taxes),
                       className = 'monthly_value'),
                html.Div([
                    html.P('+{0:,.1f}%'.format(pct_taxes),
                           className = 'indicator1'),
                    html.Div([
                        html.I(className = "fas fa-caret-up",
                               style = {"font-size": "25px",
                                        'color': '#00B050'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]
    elif pct_taxes < 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(taxes),
                       className = 'monthly_value'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_taxes),
                           className = 'indicator2'),
                    html.Div([
                        html.I(className = "fas fa-caret-down",
                               style = {"font-size": "25px",
                                        'color': '#FF3399'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]

    elif pct_taxes == 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(taxes),
                       className = 'monthly_value'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_taxes),
                           className = 'indicator2'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]


@app.callback(Output('income_statement7', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        net_profit = filter_month['net profit'].iloc[0]
        pct_net_profit = filter_month['pct_net_profit'].iloc[0]

    if net_profit < 0 and pct_net_profit < 0:
        return [
            html.Div([
                html.P('(${0:,.0f})'.format(abs(net_profit)),
                       className = 'monthly_value1'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_net_profit),
                           className = 'indicator2'),
                    html.Div([
                        html.I(className = "fas fa-caret-down",
                               style = {"font-size": "25px",
                                        'color': '#FF3399'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]
    if net_profit < 0 and pct_net_profit > 0:
        return [
            html.Div([
                html.P('(${0:,.0f})'.format(abs(net_profit)),
                       className = 'monthly_value1'),
                html.Div([
                    html.P('+{0:,.1f}%'.format(pct_net_profit),
                           className = 'indicator1'),
                    html.Div([
                        html.I(className = "fas fa-caret-down",
                               style = {"font-size": "25px",
                                        'color': '#00B050'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]
    if pct_net_profit > 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(net_profit),
                       className = 'monthly_value'),
                html.Div([
                    html.P('+{0:,.1f}%'.format(pct_net_profit),
                           className = 'indicator1'),
                    html.Div([
                        html.I(className = "fas fa-caret-up",
                               style = {"font-size": "25px",
                                        'color': '#00B050'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]
    elif pct_net_profit < 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(net_profit),
                       className = 'monthly_value'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_net_profit),
                           className = 'indicator2'),
                    html.Div([
                        html.I(className = "fas fa-caret-down",
                               style = {"font-size": "25px",
                                        'color': '#FF3399'},
                               ),
                    ], className = 'value_indicator'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]

    elif pct_net_profit == 0:
        return [
            html.Div([
                html.P('${0:,.0f}'.format(net_profit),
                       className = 'monthly_value'),
                html.Div([
                    html.P('{0:,.1f}%'.format(pct_net_profit),
                           className = 'indicator2'),
                ], className = 'value_indicator_row1'),
            ], className = 'income_statement_monthly_row'),
        ]


@app.callback(Output('quick_ratio_value', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        quick_ratio = filter_month['quick ratio'].iloc[0]
        pct_quick_ratio = filter_month['pct_quick_ratio'].iloc[0]

        if pct_quick_ratio > 0:
            return [
                html.Div([
                    html.P('{0:,.2f}'.format(quick_ratio),
                           ),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(pct_quick_ratio),
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
        elif pct_quick_ratio < 0:
            return [
                html.Div([
                    html.P('{0:,.2f}'.format(quick_ratio),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_quick_ratio),
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
        elif pct_quick_ratio == 0:
            return [
                html.Div([
                    html.P('{0:,.2f}'.format(quick_ratio),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_quick_ratio),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]


@app.callback(Output('current_ratio_value', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        current_ratio = filter_month['current ratio'].iloc[0]
        pct_current_ratio = filter_month['pct_current_ratio'].iloc[0]

        if pct_current_ratio > 0:
            return [
                html.Div([
                    html.P('{0:,.2f}'.format(current_ratio),
                           ),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(pct_current_ratio),
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
        elif pct_current_ratio < 0:
            return [
                html.Div([
                    html.P('{0:,.2f}'.format(current_ratio),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_current_ratio),
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
        elif pct_current_ratio == 0:
            return [
                html.Div([
                    html.P('{0:,.2f}'.format(current_ratio),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_current_ratio),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]


@app.callback(Output('net_profit_value', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        net_profit = filter_month['net profit'].iloc[0]
        pct_net_profit = filter_month['pct_net_profit'].iloc[0]

        if pct_net_profit > 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(net_profit),
                           ),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(pct_net_profit),
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
        elif pct_net_profit < 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(net_profit),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_net_profit),
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
        elif pct_net_profit == 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(net_profit),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_net_profit),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]


@app.callback(Output('cash_at_eom_value', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        cash_at_eom = filter_month['cash at eom'].iloc[0]
        pct_cash_at_eom = filter_month['pct_cash_at_eom'].iloc[0]

        if pct_cash_at_eom > 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(cash_at_eom),
                           ),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(pct_cash_at_eom),
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
        elif pct_cash_at_eom < 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(cash_at_eom),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_cash_at_eom),
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
        elif pct_cash_at_eom == 0:
            return [
                html.Div([
                    html.P('${0:,.0f}'.format(cash_at_eom),
                           ),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_cash_at_eom),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'indicator_column'),
            ]


@app.callback(Output('third_left_circle', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        net_profit_margin_percentage = filter_month['net profit margin %'].iloc[0]
        pct_net_profit_margin_percentage = filter_month['pct_net_profit_margin_%'].iloc[0]
        net_profit_margin_percentage_target = float(10.0)
        net_profit_margin_vs_target_margin = net_profit_margin_percentage - net_profit_margin_percentage_target

        if net_profit_margin_vs_target_margin > 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Net Profit Margin',
                               className = 'donut_chart_title'
                               ),
                        html.P('% vs Target',
                               className = 'donut_chart_title1'
                               ),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(net_profit_margin_vs_target_margin),
                                   className = 'indicator1'),
                            html.Div([
                                html.I(className = "fas fa-caret-up",
                                       style = {"font-size": "25px",
                                                'color': '#00B050'},
                                       ),
                            ], className = 'value_indicator'),
                        ], className = 'value_indicator_row'),
                        html.P('Target: 10.0%',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'inside_donut_chart_column'),
            ]

        if net_profit_margin_vs_target_margin < 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Net Profit Margin',
                               className = 'donut_chart_title'
                               ),
                        html.P('% vs Target',
                               className = 'donut_chart_title1'
                               ),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(net_profit_margin_vs_target_margin),
                                   className = 'indicator2'),
                            html.Div([
                                html.I(className = "fas fa-caret-down",
                                       style = {"font-size": "25px",
                                                'color': '#FF3399'},
                                       ),
                            ], className = 'value_indicator'),
                        ], className = 'value_indicator_row'),
                        html.P('Target: 10.0%',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'inside_donut_chart_column'),
            ]

        if net_profit_margin_vs_target_margin == 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Net Profit Margin',
                               className = 'donut_chart_title'
                               ),
                        html.P('% vs Target',
                               className = 'donut_chart_title1'
                               ),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(net_profit_margin_vs_target_margin),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('Target: 10.0%',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'inside_donut_chart_column'),
            ]


@app.callback(Output('chart3', 'figure'),
              [Input('select_month', 'value')])
def update_graph(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        net_profit_margin_percentage = filter_month['net profit margin %'].iloc[0]
        pct_net_profit_margin_percentage = filter_month['pct_net_profit_margin_%'].iloc[0]
        net_profit_margin_percentage_target = float(10.0)
        net_profit_margin_vs_target_margin = net_profit_margin_percentage - net_profit_margin_percentage_target
        remaining_net_profit_margin_vs_target_margin = 100 - (net_profit_margin_vs_target_margin)
        colors = ['#D35940', '#82FFFF']

    return {
        'data': [go.Pie(labels = ['', ''],
                        values = [net_profit_margin_vs_target_margin, remaining_net_profit_margin_vs_target_margin],
                        marker = dict(colors = colors,
                                      # line=dict(color='#DEB340', width=2)
                                      ),
                        hoverinfo = 'skip',
                        textinfo = 'text',
                        hole = .7,
                        rotation = 90
                        )],

        'layout': go.Layout(
            plot_bgcolor = 'rgba(0,0,0,0)',
            paper_bgcolor = 'rgba(0,0,0,0)',
            margin = dict(t = 35, b = 0, r = 0, l = 0),
            showlegend = False,
            title = {'text': '',
                     'y': 0.95,
                     'x': 0.5,
                     'xanchor': 'center',
                     'yanchor': 'top'},
            titlefont = {'color': 'white',
                         'size': 15},
        ),

    }


@app.callback(Output('fourth_right_circle', 'children'),
              [Input('select_month', 'value')])
def update_text(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        expense_budget_percentage = filter_month['expense budget %'].iloc[0]
        pct_expense_budget_percentage = filter_month['pct_expense_budget_%'].iloc[0]

        if pct_expense_budget_percentage > 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Expense Budget %',
                               className = 'donut_chart_title'
                               ),
                        html.P('{0:,.1f}%'.format(expense_budget_percentage),
                               className = 'net_profit_margin_percentage2'),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('+{0:,.1f}%'.format(pct_expense_budget_percentage),
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
                ], className = 'inside_donut_chart_column'),
            ]

        if pct_expense_budget_percentage < 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Expense Budget %',
                               className = 'donut_chart_title'
                               ),
                        html.P('{0:,.1f}%'.format(expense_budget_percentage),
                               className = 'net_profit_margin_percentage2'),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_expense_budget_percentage),
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
                ], className = 'inside_donut_chart_column'),
            ]

        if pct_expense_budget_percentage == 0:
            return [
                html.Div([
                    html.Div([
                        html.P('Expense Budget %',
                               className = 'donut_chart_title'
                               ),
                        html.P('{0:,.1f}%'.format(expense_budget_percentage),
                               className = 'net_profit_margin_percentage2'),
                    ], className = 'title_and_percentage'),
                    html.Div([
                        html.Div([
                            html.P('{0:,.1f}%'.format(pct_expense_budget_percentage),
                                   className = 'indicator2'),
                        ], className = 'value_indicator_row'),
                        html.P('vs previous month',
                               className = 'vs_previous_month')
                    ], className = 'vs_p_m_column')
                ], className = 'inside_donut_chart_column'),
            ]


@app.callback(Output('chart4', 'figure'),
              [Input('select_month', 'value')])
def update_graph(select_month):
    if select_month is None:
        raise PreventUpdate
    else:
        filter_month = data[data['months'] == select_month]
        expense_budget_percentage = filter_month['expense budget %'].iloc[0]
        remaining_expense_budget_percentage = 100 - (filter_month['expense budget %'].iloc[0])
        colors = ['#8AC4A7', '#82FFFF']

    return {
        'data': [go.Pie(labels = ['', ''],
                        values = [expense_budget_percentage, remaining_expense_budget_percentage],
                        marker = dict(colors = colors,
                                      # line=dict(color='#DEB340', width=2)
                                      ),
                        hoverinfo = 'skip',
                        textinfo = 'text',
                        hole = .7,
                        rotation = 360
                        )],

        'layout': go.Layout(
            plot_bgcolor = 'rgba(0,0,0,0)',
            paper_bgcolor = 'rgba(0,0,0,0)',
            autosize = True,
            margin = dict(t = 35, b = 0, r = 0, l = 0),
            showlegend = False,
            title = {'text': '',
                     'y': 0.95,
                     'x': 0.5,
                     'xanchor': 'center',
                     'yanchor': 'top'},
            titlefont = {'color': 'white',
                         'size': 15},
        ),

    }


if __name__ == "__main__":
    app.run_server(debug = True)

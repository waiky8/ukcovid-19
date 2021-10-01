import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
from dash_table.Format import Format, Scheme
import plotly.graph_objects as go
import pandas as pd

# import bs4 as bs
# import urllib.request

'''
===========
SET-UP DASH
===========
'''

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO],
                meta_tags=[
                    {'name': 'viewport',
                     'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'
                     }
                ]
                )
server = app.server
app.title = 'UK Covid-19 Local'

'''
==================================================
READ DATA FROM GOVUK URL & POSTCODE FROM CSV FILES
==================================================
'''

file = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=msoa&metric=newCasesBySpecimenDateRollingSum&metric=newCasesBySpecimenDateRollingRate&metric=newCasesBySpecimenDateChange&metric=newCasesBySpecimenDateChangePercentage&metric=newCasesBySpecimenDateDirection&format=csv'

df = pd.read_csv(file)

'''
======================
PARAMETERS & VARIABLES
======================
'''
date_max = df['date'].max()

topn = 5  # Number of items to show as 'top x'
chart_h = 320  # height of charts
datatable_rows = 10  # rows per page of datatable
fontsize = 12

textcol = 'dimgrey'
bgcol_1 = 'white'
bgcol_2 = 'whitesmoke'

'''
===================
DASH LAYOUT SECTION
===================
'''

app.layout = html.Div(
    [
        html.Div(
            [
                html.H3('UK Covid-19'),
            ],
            style={'text-align': 'center', 'font-weight': 'bold'}
        ),

        html.Br(),

        html.Div(
            [
                html.Div(
                    [
                        html.Br(),

                        dcc.Dropdown(
                            id='date_drop',
                            options=[{'label': i, 'value': i} for i in sorted(df['date'].unique())],
                            multi=False,
                            placeholder='Select Date',
                            value=date_max,
                            style={'font-size': fontsize, 'color': 'black', 'background-color': bgcol_1}
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            id='msoa_drop',
                                            options=[{'label': i, 'value': i} for i in sorted(df['areaName'].unique())],
                                            multi=True,
                                            placeholder='Local Area',
                                            style={'font-size': fontsize, 'color': 'black', 'background-color': bgcol_1}
                                        ),
                                    ], xs=6, sm=6, md=6, lg=6, xl=6
                                ),

                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            id='ltla_drop',
                                            options=[{'label': i, 'value': i} for i in sorted(df['LtlaName'].unique())],
                                            multi=True,
                                            placeholder='Local Authority',
                                            style={'font-size': fontsize, 'color': 'black', 'background-color': bgcol_1}
                                        ),
                                    ], xs=6, sm=6, md=6, lg=6, xl=6
                                ),
                            ]
                        ),

                        html.Br(),

                        # dbc.Row(
                        #     [
                        #         dbc.Col(
                        #             [
                        #                 dcc.Input(
                        #                     id='postcode_inp',
                        #                     # className='col-4',
                        #                     placeholder='Post Code',
                        #                     style={'font-size': fontsize, 'color': 'black', 'background-color': bgcol_1}
                        #                 ),
                        #             ], xs=4, sm=4, md=4, lg=4, xl=4
                        #         ),
                        #
                        #         dbc.Col(
                        #             [
                        #                 html.P(id='message', className='col-8'),
                        #             ], xs=8, sm=8, md=8, lg=8, xl=8
                        #         ),
                        #     ]
                        # ),
                        #
                        # html.Br()
                    ], style={'background': bgcol_2, 'padding': '0px 10px 0px 10px'}
                )
            ], style={'padding': '0px 20px 0px 20px'}
        ),

        html.Br(),

        html.Div(
            [
                dcc.Loading(
                    dash_table.DataTable(
                        id='datatable',

                        columns=[
                            {
                                'id': 'areaName',
                                'name': 'Local Area',
                                'type': 'text'
                            },
                            {
                                'id': 'newCasesBySpecimenDateRollingSum',
                                'name': 'New Cases',
                                'type': 'numeric',
                                'format': Format(
                                    precision=0,
                                    group=',',
                                    scheme=Scheme.fixed,
                                    symbol=''
                                )
                            },
                            {
                                'id': 'newCasesBySpecimenDateDirection',
                                'name': 'Change',
                                'type': 'text'
                            },
                            {
                                'id': 'LtlaName',
                                'name': 'Local Authority',
                                'type': 'text'
                            },
                        ],

                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'width': '100px',
                            'maxWidth': '100px',
                            'minWidth': '100px',
                        },

                        style_cell_conditional=[
                            {
                                'if': {
                                    'column_id': 'areaName'
                                },
                                'textAlign': 'left'
                            },
                            {
                                'if': {
                                    'column_id': 'LtlaName'
                                },
                                'textAlign': 'left'
                            },
                            {
                                'if': {
                                    'column_id': 'newCasesBySpecimenDateDirection'
                                },
                                'textAlign': 'center'
                            },
                        ],

                        style_table={'overflowX': 'auto'},

                        style_cell={
                            'fontSize': 12,
                            'padding': '0px 5px 0px 5px'
                        },

                        page_size=datatable_rows,
                    )
                )
            ], style={'padding': '0px 20px 0px 20px'}
        ),

        html.Br(), html.Br(),

        html.Div(
            dcc.Loading(
                dcc.Graph(
                    id='chart1',
                    figure={},
                    config={'displayModeBar': False}
                )
            ), style={'padding': '0px 20px 0px 20px'}
        ),

        html.Br(),

        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.P(
                                    ['Data Source: ',
                                     html.A('GovUK', href='https://coronavirus.data.gov.uk/details/download',
                                            target='_blank')
                                     ], className='font-italic'
                                ),
                            ]
                        ),

                        dbc.Col(
                            [
                                html.P(
                                    ['Code: ',
                                     html.A('Github', href='https://github.com/waiky8/ukcovid-19',
                                            target='_blank')
                                     ], className='font-italic text-right'
                                ),
                            ],
                        ),
                    ], style={'padding': '0px 20px 0px 20px'}
                )
            ]
        )
    ]
)

'''
======================
CALLBACK FOR DATATABLE
======================
'''


@app.callback(
    Output('datatable', 'data'),
    [
        Input('date_drop', 'value'),
        Input('ltla_drop', 'value'),
        Input('msoa_drop', 'value')
    ]
)
def return_datatable(selected_date, selected_ltla, selected_area):
    df1 = df.copy()
    df1 = df1[df1['date'].isin([selected_date])]

    if selected_area is None or selected_area == []:
        if selected_ltla is None or selected_ltla == []:
            pass
        else:
            df1 = df1[df1['LtlaName'].isin(selected_ltla)]
    else:
        df1 = df1[df1['areaName'].isin(selected_area)]

    df1.loc[(df1.newCasesBySpecimenDateDirection == 'UP'), 'newCasesBySpecimenDateDirection'] = '↑'
    df1.loc[(df1.newCasesBySpecimenDateDirection == 'DOWN'), 'newCasesBySpecimenDateDirection'] = '↓'
    df1.loc[(df1.newCasesBySpecimenDateDirection == 'SAME'), 'newCasesBySpecimenDateDirection'] = '-'  # '↔'

    df1 = df1.sort_values(by=['newCasesBySpecimenDateRollingSum'], ascending=False)
    df1['Row'] = df1.reset_index().index
    df1['Row'] += 1

    if df1.empty:
        df1['LtlaName'] = ['Not Available']
        df1['areaName'] = ['Not Available']
        df1['newCasesBySpecimenDateRollingSum'] = ['Not Available']

    return df1.to_dict('records')


'''
==================
CALLBACK FOR CHART
==================
'''


@app.callback(
    Output('chart1', 'figure'),
    [
        Input('ltla_drop', 'value'),
        Input('msoa_drop', 'value')
    ]
)
def return_chart(selected_ltla, selected_area):
    if selected_area is None or selected_area == []:
        loc_area_list = ['Bents Green & Millhouses']
        df1 = df[df['areaName'].isin(loc_area_list)]
        chart_title = 'Cases for Bents Green & Millhouses'
    else:
        df1 = df[df['areaName'].isin(selected_area)]
        loc_area_list = df1['areaName'].unique()
        if len(selected_area) == 1:
            chart_title = 'Cases for ' + str(selected_area[0])
        else:
            chart_title = 'Cases for Selected Areas'

    fig1 = go.Figure()
    fig1.update_layout(
        title=dict(
            text=chart_title,
            font=dict(
                size=12,
                color=textcol
            )
        ),

        font=dict(
            size=fontsize,
            color=textcol
        ),

        plot_bgcolor=bgcol_2,
        height=chart_h,
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis={
            'title': '',
            'tickangle': 0,
            'showgrid': False,
            'fixedrange': True
        },
        yaxis={
            'title': '',
            'showgrid': False,
            'zeroline': False,
            'fixedrange': True
        },
        hovermode='x',
        legend=dict(
            yanchor="top",
            y=1.01,
            xanchor="left",
            x=0.01
        )
    )

    for la in loc_area_list:
        dfx = df1.copy()[df1['areaName'] == la]
        dfx['newCasesBySpecimenDateRollingSum'].fillna(0, inplace=True)  # solve problem of gap in chart if blank value
        fig1.add_trace(
            go.Scatter(
                x=dfx['date'],
                y=dfx['newCasesBySpecimenDateRollingSum'],
                mode='lines',
                name=la,
                # text=dfx['areaName'],
                customdata=dfx['newCasesBySpecimenDateRollingSum'],
                hovertemplate='<br><b>%{customdata}</b>'  # '<br><b>%{text}</b>: %{customdata}'
            )
        )

    return fig1


'''
=================================
CALLBACK FOR POSTCODE/MSOA LOOKUP
=================================
'''

# @app.callback(
#     Output('message', 'children'),
#     [
#         Input('postcode_inp', 'n_submit'),
#         Input('postcode_inp', 'n_blur')
#     ],
#     State('postcode_inp', 'value')
# )
# def return_datatable(ns, nb, selected_postcode):
#     message = ''
#
#     if selected_postcode is None or selected_postcode == '':
#         pass
#     else:
#         neighbourhood = get_data(selected_postcode.upper())
#         if neighbourhood == '':
#             message = 'Please enter valid full postcode'
#         else:
#             message = neighbourhood
#
#     return message


'''
=================================
MAP POSTCODE TO LOCAL AREA (MSOA)
=================================
'''

# def get_data(pcode):
#     area = ''
#
#     url = ('https://www.doogal.co.uk/ShowMap.php?postcode=' + pcode).replace(' ', '%20')
#
#     try:
#         source = urllib.request.urlopen(url)
#         soup = bs.BeautifulSoup(source, 'lxml')
#         tables = soup.find_all('table')
#
#         for tb in tables:
#             table_rows = tb.find_all('tr')
#
#             for tr in table_rows:
#                 thd = tr.find_all(['th', 'td'])
#                 row = [i.text for i in thd]
#                 if row[0] == 'Middle layer super output area':
#                     area = row[1]
#                     break
#
#     except urllib.request.HTTPError as err:
#         print('HTTP Error: (postcode ', pcode, ')', err.code)
#
#     return area


if __name__ == '__main__':
    app.run_server(debug=True)

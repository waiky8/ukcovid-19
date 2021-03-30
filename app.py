import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_daq as daq
import pandas as pd
import numpy as np
import datetime
from configparser import ConfigParser

'''
===========
SET-UP DASH
===========
'''

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO],
                meta_tags=[
                    {"name": "viewport",
                     "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,"
                     }
                ]
                )
server = app.server
app.title = "UK Covid-19"

config = ConfigParser()
config.read("config.ini")
mapbox_access_token = config["mapbox"]["secret_token"]

'''
================
READ EXCEL FILES
================
'''

# df = pd.read_excel("covid_data.xlsx")
# df_tot = pd.read_excel("covid_totals.xlsx")

df = pd.read_excel("https://github.com/waiky8/ukcovid-19/blob/main/covid_data.xlsx?raw=true")
df_tot = pd.read_excel("https://github.com/waiky8/ukcovid-19/blob/main/covid_totals.xlsx?raw=true")

'''
======================
PARAMETERS & VARIABLES
======================
'''

date_min = "2020-08-12"  # data available from this date
date_max = df["date"].max()

marker_calc_size = 50  # used to (dynamically) calculate marker size on map
topn = 5
chart_h = 320
datatable_rows = 10
fontsize = 15

textcol = "dimgrey"
bgcol_1 = "white"
bgcol_2 = "whitesmoke"
col_1 = "teal"
col_2 = "firebrick"
col_3 = "lightseagreen"
col_4 = "indianred"

'''
===================
DASH LAYOUT SECTION
===================
'''

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("UK Covid-19"),
                html.H3("(by Local Authority - Daily)")
            ],
            style={"text-align": "center", "font-weight": "bold"}
        ),

        html.Br(),

        html.P(
            html.A("Local Area View - Weekly", href="https://ukcovid-19a.herokuapp.com/", target="_blank"),
            style={"padding": "0px 0px 0px 50px"}
        ),

        html.Br(),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.P("Select Date:"),

                                dcc.DatePickerSingle(
                                    id="date_picker",
                                    clearable=True,
                                    with_portal=True,
                                    date=date_max,
                                    display_format="MMM D, YYYY",
                                    day_size=50,
                                    initial_visible_month=date_max,
                                    min_date_allowed=date_min,
                                    max_date_allowed=date_max
                                ),

                                html.Br(), html.Br(),

                                dcc.Dropdown(
                                    id="locauth_drop",
                                    options=[{"label": i, "value": i} for i in sorted(df["areaName"].unique())],
                                    multi=True,
                                    placeholder="Local Authority (Mutli-Select)",
                                    style={"font-size": fontsize, "color": "black", "background-color": bgcol_1}
                                )
                            ], style={"padding": "0px 10px 0px 10px"}
                        ),

                        html.Br(),

                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.P("Cumulative")
                                            ], className="col-3"

                                        ),

                                        dbc.Col(
                                            [
                                                daq.BooleanSwitch(
                                                    id='data_type',
                                                    on=True
                                                )
                                            ], className="col-3"
                                        ),

                                        dbc.Col(
                                            [
                                                html.P("Daily")
                                            ], className="col-3"

                                        ),
                                    ]
                                )
                            ], style={"padding": "0px 10px 0px 10px"}
                        ),

                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.P("Deaths")
                                            ], className="col-3"

                                        ),

                                        dbc.Col(
                                            [
                                                daq.BooleanSwitch(
                                                    id='cases_deaths_switch',
                                                    on=True
                                                )
                                            ], className="col-3"
                                        ),

                                        dbc.Col(
                                            [
                                                html.P("Cases")
                                            ], className="col-3"
                                        )
                                    ]
                                )
                            ], style={"padding": "0px 10px 0px 10px"}
                        ),
                    ], style={"background": bgcol_2}
                ),
            ], style={"padding": "0px 30px 0px 30px"}
        ),

        html.Br(), html.Br(),

        html.Div(
            [
                html.Div(
                    [
                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            html.H4("New Cases", className="card-title"),
                                            html.H3(
                                                id="new_cases",
                                                className="card-value",
                                                style={"font-weight": "bold"}
                                            )
                                        ],
                                        style={
                                            "color": bgcol_1,
                                            "background": col_1,
                                            "text-align": "center"
                                        }
                                    )
                                ),

                                dbc.Col(
                                    dbc.Card(
                                        [
                                            html.H4("New Deaths", className="card-title"),
                                            html.H3(
                                                id="new_deaths",
                                                className="card-value",
                                                style={"font-weight": "bold"}
                                            )
                                        ],
                                        style={
                                            "color": bgcol_1,
                                            "background": col_2,
                                            "text-align": "center"
                                        }
                                    )
                                )
                            ], style={"padding": "0px 10px 0px 10px"}
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            html.H4("Total Cases", className="card-title"),
                                            html.H3(
                                                id="total_cases",
                                                className="card-value",
                                                style={"font-weight": "bold"}
                                            )
                                        ],
                                        style={
                                            "color": bgcol_1,
                                            "background": col_3,
                                            "text-align": "center"
                                        }
                                    )
                                ),

                                dbc.Col(
                                    dbc.Card(
                                        [
                                            html.H4("Total Deaths", className="card-title"),
                                            html.H3(
                                                id="total_deaths",
                                                className="card-value",
                                                style={"font-weight": "bold"}
                                            )
                                        ],
                                        style={
                                            "color": bgcol_1,
                                            "background": col_4,
                                            "text-align": "center"
                                        }
                                    )
                                )
                            ], style={"padding": "0px 10px 0px 10px"}
                        ),

                        html.Br()
                    ], style={"background": bgcol_2}
                )
            ], style={"padding": "0px 30px 0px 30px"}
        ),

        html.Br(), html.Br(),

        html.Div(
            dcc.Loading(
                dcc.Graph(
                    id="covid_map",
                    figure={},
                    config={"displayModeBar": False}
                )
            ), style={"padding": "0px 20px 0px 20px"}
        ),

        html.Br(), html.Br(),

        html.Div(
            [
                dcc.Loading(
                    dcc.Graph(
                        id="chart1",
                        figure={},
                        config={"displayModeBar": False}
                    ), className="col-6"
                )
            ], style={"padding": "0px 20px 0px 20px"}
        ),

        html.Br(), html.Br(),

        html.Div(
            html.P("*Defaults to 'Sheffield' if no local authority selected"),
            style={"font-style": "italic", "padding": "0px 20px 0px 20px"}
        ),

        html.Div(
            dcc.Loading(
                dcc.Graph(
                    id="chart3",
                    figure={},
                    config={"displayModeBar": False}
                )
            ), style={"padding": "0px 20px 0px 20px"}
        ),

        html.Br(), html.Br(),

        html.Div(
            dcc.Loading(
                dcc.Graph(
                    id="chart4",
                    figure={},
                    config={"displayModeBar": False}
                )
            ), style={"padding": "0px 20px 0px 20px"}
        ),

        html.Br(), html.Br(), html.Br(),

        html.Div(
            html.P(
                ["Data Source: ",
                 html.A("GovUK", href="https://coronavirus.data.gov.uk/details/download", target="_blank")
                 ]
            ),
            style={"padding": "0px 0px 0px 50px"}
        ),

        html.Div(
            html.P(
                ["Code: ",
                 html.A("Github", href="https://github.com/waiky8/ukcovid-19", target="_blank")
                 ]
            ),
            style={"padding": "0px 0px 0px 50px"}
        ),

        # dummy DIV to trigger totals_timeline callback
        html.Div(
            id="dummy",
            children=[],
            style={"display": "none"}
        )
    ]
)

'''
================
CALLBACK FOR MAP
================
'''


@app.callback(
    Output("covid_map", "figure"),  # Output("datatable", "data"),
    [
        Input("date_picker", "date"),
        Input("locauth_drop", "value"),
        Input("data_type", "on"),
        Input("cases_deaths_switch", "on")
    ]
)
def return_datatable(selected_date, selected_auth, selected_data, selected_cases):
    # print(str(datetime.datetime.now()), "[1] start update_map...")

    df1 = df[df["date"].isin([selected_date])]

    if selected_data:
        if selected_cases:
            display = "newCasesByPublishDate"
            marker_col = col_1
        else:
            display = "newDeaths28DaysByPublishDate"
            marker_col = col_2
    else:
        if selected_cases:
            display = "cumCasesByPublishDate"
            marker_col = col_3
        else:
            display = "cumDeaths28DaysByPublishDate"
            marker_col = col_4

    if selected_auth is None or selected_auth == []:
        pass
    else:
        df1 = df1[df1["areaName"].isin(selected_auth)]

    df1 = df1.sort_values(by=[display], ascending=False)
    df1["Row"] = df1.reset_index().index
    df1["Row"] += 1

    lat_mean = pd.to_numeric(df1["Latitude"]).mean()
    lon_mean = pd.to_numeric(df1["Longitude"]).mean()

    df1.loc[(pd.isna(df1["newDeaths28DaysByPublishDate"])), "newDeaths28DaysByPublishDate"] = 0
    df1.loc[(pd.isna(df1["cumDeaths28DaysByPublishDate"])), "cumDeaths28DaysByPublishDate"] = 0

    fig = go.Figure(
        go.Scattermapbox(
            lat=df1["Latitude"],
            lon=df1["Longitude"],
            mode="text+markers",
            marker={"size": df1[display] * marker_calc_size / df1[display].max(),
                    "color": marker_col,
                    },
            name="",
            text=df1["areaName"],
            textposition='top center',
            customdata=np.stack(
                (
                    df1["date"],
                    df1["newCasesByPublishDate"],
                    df1["newDeaths28DaysByPublishDate"],
                    df1["cumCasesByPublishDate"],
                    df1["cumDeaths28DaysByPublishDate"]
                ),
                axis=-1
            ),
            hovertemplate="<br><b>Date</b>: %{customdata[0]}" + \
                          "<br><b>Local Authority</b>: %{text}" + \
                          "<br><b>New Cases</b>: %{customdata[1]:,}" + \
                          "<br><b>New Deaths</b>: %{customdata[2]:,}" + \
                          "<br><b>Cumulative Cases</b>: %{customdata[3]:,}" + \
                          "<br><b>Cumulative Deaths</b>: %{customdata[4]:,}"
        )
    )

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=lat_mean,
                lon=lon_mean
            ),
            pitch=0,
            zoom=5,
            style="light"  # satellite, outdoors, streets, dark
        ),
        hoverlabel=dict(
            bgcolor=bgcol_1,
            font_size=12,
            font_family="Rockwell"
        ),
        margin=dict(t=0, b=0, l=0, r=0)
    )

    # print(str(datetime.datetime.now()), "[1] finish update_map...")

    return fig  # df1.to_dict("records")


'''
=======================
CALLBACK FOR BAR CHARTS
=======================
'''


@app.callback(
    Output("chart1", "figure"),
    [
        Input("date_picker", "date"),
        Input("locauth_drop", "value"),
        Input("data_type", "on"),
        Input("cases_deaths_switch", "on")
    ]
)
def return_bar_charts(selected_date, selected_auth, selected_data, selected_cases):
    # print(str(datetime.datetime.now()), "[2] start update_graph...")
    if selected_data:
        if selected_cases:
            display = "newCasesByPublishDate"
            title = "New Cases"
            bar_col = col_1
        else:
            display = "newDeaths28DaysByPublishDate"
            title = "New Deaths"
            bar_col = col_2
    else:
        if selected_cases:
            display = "cumCasesByPublishDate"
            title = " Total Cases"
            bar_col = col_3
        else:
            display = "cumDeaths28DaysByPublishDate"
            title = "Total Deaths"
            bar_col = col_4

    df1 = df[df["date"].isin([selected_date])]

    if selected_auth is None or selected_auth == []:
        pass
    else:
        df1 = df1[df1["areaName"].isin(selected_auth)]

    d = datetime.datetime.strptime(selected_date, "%Y-%m-%d")

    data_fig = df1.sort_values(by=display, ascending=False)[:topn]

    fig = go.Figure(
        go.Bar(
            orientation="h",
            x=data_fig[display],
            y=data_fig["areaName"],
            texttemplate="%{y} - %{x:,}",
            textposition="inside",
            insidetextanchor="start"
        )
    )

    fig.update_layout(
        title="<b>" + title + ": " + d.strftime("%b %d, %Y") + "</b>",
        title_font_color=textcol,
        font_color=textcol,
        font_size=fontsize,
        showlegend=False,
        xaxis={
            "categoryorder": "total descending",
            "title": "",
            "tickangle": 0,
            "visible": False,
            "showgrid": False,
            "fixedrange": True
        },
        yaxis={
            "title": "",
            "autorange": "reversed",
            "visible": False,
            "showgrid": False,
            "zeroline": False,
            "fixedrange": True
        },
        height=chart_h,
        margin=dict(l=0, r=0, t=50, b=0),
        plot_bgcolor=bgcol_2
    )

    fig.update_traces(
        marker_color=bar_col,
        hoverinfo="skip"
    )

    # print(str(datetime.datetime.now()), "[2] finish update_graph...")
    return fig


'''
==================================
CALLBACK FOR LOCAL AUTHORITY CHART
==================================
'''


@app.callback(
    Output("chart3", "figure"),
    Input("locauth_drop", "value")
)
def return_loc_auth_chart(selected_auth):
    # print(str(datetime.datetime.now()), "[3] start update_graph2...")
    if selected_auth is None or selected_auth == []:
        locauth_list = ["Sheffield"]
        df1 = df[df["areaName"].isin(locauth_list)]
    else:
        df1 = df[df["areaName"].isin(selected_auth)]
        locauth_list = df1["areaName"].unique()

    fig3 = go.Figure()
    fig3.update_layout(
        title="<b>Local Authority Cases</b>",
        title_font_color=textcol,
        font_color=textcol,
        font_size=fontsize,
        plot_bgcolor=bgcol_2,
        height=chart_h,
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis={
            "title": "",
            "tickangle": 0,
            "showgrid": False,
            "fixedrange": True
        },
        yaxis={
            "title": "",
            "showgrid": False,
            "zeroline": False,
            "fixedrange": True
        },
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        hovermode="x"
    )

    for la in locauth_list:
        dfx = df1[df1["areaName"] == la]
        fig3.add_trace(
            go.Scatter(
                x=dfx["date"],
                y=dfx["newCasesByPublishDate"],
                mode="lines",
                name="",
                text=dfx["areaName"],
                showlegend=False,
                customdata=dfx["newCasesByPublishDate"],
                hovertemplate="<br><b>%{text}</b>: %{customdata}"
            )
        )

    # print(str(datetime.datetime.now()), "[3] finish update_graph2...")
    return fig3


'''
=========================
CALLBACK FOR TOTALS CHART
=========================
'''


@app.callback(
    Output("chart4", "figure"),
    Input("dummy", "children")
)
def return_tot_chart(none):
    date_list = df["date"].unique()
    # print(str(datetime.datetime.now()), "[4] start totals_timeline...")

    fig5 = go.Figure()
    fig5.update_layout(
        title="<b>UK Daily Cases</b>",
        title_font_color=textcol,
        font_color=textcol,
        font_size=fontsize,
        plot_bgcolor=bgcol_2,
        height=chart_h,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False,
        xaxis={
            "title": "",
            "tickangle": 0,
            "showgrid": False,
            "fixedrange": True
        },
        yaxis={
            "title": "",
            "showgrid": False,
            "zeroline": False,
            "fixedrange": True
        },
        hovermode="x"
    )

    tot_cases = []
    for dt in date_list:
        dfx = df_tot[df_tot["date"] == dt]
        tc = dfx["newCasesByPublishDate"].sum()
        tot_cases.append(tc)

    fig5.add_trace(
        go.Scatter(
            x=date_list,
            y=tot_cases,
            fill="tonexty",
            mode="none",
            name="Cases",
            showlegend=False,
            hovertemplate=None
        )
    )

    # print(str(datetime.datetime.now()), "[4] finish totals_timeline...")
    return fig5


'''
==========================
CALLBACK FOR SUMMARY BOXES
==========================
'''


@app.callback(
    [
        Output("new_cases", "children"),
        Output("new_deaths", "children"),
        Output("total_cases", "children"),
        Output("total_deaths", "children")
    ],
    Input("date_picker", "date")
)
def return_summary(selected_date):
    # print(str(datetime.datetime.now()), "[5] start update_summary...")
    df1 = df_tot[df_tot["date"] == selected_date]

    new_cases = format(int(df1["newCasesByPublishDate"]), ",d")
    new_deaths = format(int(df1["newDeaths28DaysByPublishDate"]), ",d")
    total_cases = format(int(df1["cumCasesByPublishDate"]), ",d")
    total_deaths = format(int(df1["cumDeaths28DaysByPublishDate"]), ",d")

    # print(str(datetime.datetime.now()), "[5] finish update_summary...")
    return new_cases, new_deaths, total_cases, total_deaths


if __name__ == "__main__":
    app.run_server(debug=True)

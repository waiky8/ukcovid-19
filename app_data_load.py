import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from openpyxl import load_workbook
import urllib.request
import datetime

################################################################################
#  Data source from GovUK                                                      #
################################################################################
url_ltla = "https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=cumCasesByPublishDate&metric=newCasesByPublishDate&metric=newDeaths28DaysByPublishDate&metric=cumDeaths28DaysByPublishDate&format=csv"
url_uk = "https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=cumCasesByPublishDate&metric=newCasesByPublishDate&metric=newDeaths28DaysByPublishDate&metric=cumDeaths28DaysByPublishDate&format=csv"

################################################################################
#  Set up Dash application                                                     #
################################################################################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO],
                meta_tags=[{"name": "viewport",
                            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,"
                            }
                           ]
                )
server = app.server
app.title = "UK Covid-19"

################################################################################
#  Read input files and load lists and variables                               #
################################################################################

covid_daily_file = "covid_data.xlsx"
covid_totals_file = "covid_totals.xlsx"

df_daily = pd.read_excel(covid_daily_file)
df_totals = pd.read_excel(covid_totals_file)

date_min = "2020-08-12"  # data available from this date
date_max = df_daily["date"].max()

date_list_daily = [str(d) for d in df_daily["date"].unique()]
date_list_totals = [str(d) for d in df_totals["date"].unique()]

################################################################################
#  Define layout of Dash screen                                                #
################################################################################

app.layout = html.Div(
    [
        dbc.Row(dbc.Col(html.H1("UK Covid-19"), style={"text-align": "center", "font-weight": "bold"})),

        dbc.Row(dbc.Col(html.H3("(Data Load)"), style={"text-align": "center", "font-weight": "bold"})),

        html.Br(),

        dbc.Col(
            [
                html.P("Select Date"),

                html.Div(
                    dcc.DatePickerSingle(
                        id="date_picker",
                        clearable=True,
                        with_portal=True,
                        date=date_max,
                        display_format="MMM D, YYYY",
                        day_size=50,
                        initial_visible_month=date_max,
                        min_date_allowed=date_min,
                        # max_date_allowed=date_max
                    )
                )
            ], style={"padding": "0px 20px 0px 20px"}
        ),

        html.Br(), html.Br(), html.Br(),

        html.Div(
            [
                html.Br(),

                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Loading(
                                dbc.Card(
                                    [
                                        html.H5("Covid Data", className="card-title"),
                                        html.H4(
                                            html.Div(id="message1",
                                                     className="card-value",
                                                     style={"font-weight": "bold"}
                                                     )
                                        )
                                    ],
                                    style={"color": "white",
                                           "background": "teal",
                                           "text-align": "center"
                                           }
                                )
                            ),
                        ),

                        dbc.Col(
                            dcc.Loading(
                                dbc.Card(
                                    [
                                        html.H5("Covid Totals", className="card-title"),
                                        html.H4(
                                            html.Div(id="message2",
                                                     className="card-value",
                                                     style={"font-weight": "bold"}
                                                     )
                                        )
                                    ],
                                    style={"color": "white",
                                           "background": "midnightblue",
                                           "text-align": "center"
                                           }
                                )
                            )
                        )
                    ], style={"padding": "0px 30px 0px 30px"}
                ),
                html.Br(),
            ], style={"background": "ghostwhite", "border-style": "groove"}
        ),
    ], style={"padding": "0px 30px 0px 30px"}
)


################################################################################
#  Callback to display messages                                                #
################################################################################

@app.callback(
    [Output("message1", "children"),
     Output("message2", "children")
     ],
    Input("date_picker", "date")
)
def update_data(selected_date):
    message1 = message2 = ""

    d = datetime.datetime.strptime(selected_date, "%Y-%m-%d")

    ################################################################################
    #  Daily data                                                                  #
    ################################################################################
    if selected_date in date_list_daily:
        message1 = "[" + d.strftime("%b %d, %Y") + "] Already Uploaded 👍"

    else:
        url = url_ltla + "&release=" + selected_date  # Attempt to read data for selected date

        try:
            print("Processing daily data...")
            print(str(datetime.datetime.now()), "step 1 of 3: read ", url)
            df_load = pd.read_csv(url)
            print(str(datetime.datetime.now()), " step 2 of 3: extract data for ", d.strftime("%b %d, %Y"))
            df_load = df_load[df_load["date"] == selected_date]

            print(str(datetime.datetime.now()), "step 3 of 3: write to covid file...")
            writer = pd.ExcelWriter(covid_daily_file)
            writer.book = load_workbook(covid_daily_file)
            writer.sheets = {ws.title: ws for ws in writer.book.worksheets}

            for sheetname in writer.sheets:
                df_load.to_excel(writer,
                                 sheet_name=sheetname,
                                 index=False,
                                 header=False,
                                 startrow=writer.sheets[sheetname].max_row)
                writer.save()
                date_list_daily.append(selected_date)

            message1 = "[" + d.strftime("%b %d, %Y") + "] Upload Complete ✔️"

        except urllib.request.HTTPError as e:
            message1 = "[" + d.strftime("%b %d, %Y") + "] Not Available ❌"

        except IOError as e:
            message1 = "[" + d.strftime("%b %d, %Y") + "] " + str(e)

    ################################################################################
    #  Totals data                                                                 #
    ################################################################################
    if selected_date in date_list_totals:
        message2 = "[" + d.strftime("%b %d, %Y") + "] Already Uploaded 👍"

    else:

        url = url_uk + "&release=" + selected_date  # Attempt to read data for selected date

        try:
            print("Processing totals data...")
            print(str(datetime.datetime.now()), "step 1 of 3: read ", url)
            df_load = pd.read_csv(url)
            print(str(datetime.datetime.now()), " step 2 of 3: extract data for ", d.strftime("%b %d, %Y"))
            df_load = df_load[df_load["date"] == selected_date]

            print(str(datetime.datetime.now()), "step 3 of 3: write to covid file...")
            writer = pd.ExcelWriter(covid_totals_file)
            writer.book = load_workbook(covid_totals_file)
            writer.sheets = {ws.title: ws for ws in writer.book.worksheets}

            for sheetname in writer.sheets:
                df_load.to_excel(writer,
                                 sheet_name=sheetname,
                                 index=False,
                                 header=False,
                                 startrow=writer.sheets[sheetname].max_row)
                writer.save()
                date_list_totals.append(selected_date)

            message2 = "[" + d.strftime("%b %d, %Y") + "] Upload Complete ✔️"

        except urllib.request.HTTPError as e:
            message2 = "[" + d.strftime("%b %d, %Y") + "] Not Available ❌"

        except IOError as e:
            message2 = "[" + d.strftime("%b %d, %Y") + "] " + str(e)

    print(str(datetime.datetime.now()), message1)
    print(str(datetime.datetime.now()), message2)

    return message1, message2


if __name__ == "__main__":
    app.run_server(debug=True)

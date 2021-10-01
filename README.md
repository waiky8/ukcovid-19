# UK Covid-19 Dashboard
There are plenty of (UK) covid dashboards available but this one can show comparisons at local authority level. It is built using **Dash**, written in **Python** and sources data from GovUK site https://coronavirus.data.gov.uk/details/download.<br><br>

**Mapbox** is used to show a map of cases/deaths for each local authority with markers and hover text. Leveraged **Doogal** to obtain longitude and latitude of local authorities to enable correct placement on the map.<br><br>

The application is uploaded to **Heroku**. Check it out at https://ukcovid-19.herokuapp.com/<br>
Note, there is an second application that shows cases by local area - https://ukcovid-19-local.herokuapp.com/<br>

# Features:
- Interactive dashboard 
- Summary of cases/deaths
- Map including marker that can show the covid cases and deaths for each local authority (marker size to aid in visual scale)
- Bar charts showing cases/deaths for daily or cumulative figures
- Data Table showing cases and movement of change<br><br>

# Description of code/files:
 - **app.py** - main application code that show data for local authority
 - **app_local.py** - main application code that show data for local area
 - **app_data_load.py** - code to retrieve latest data from GovUK
 - **covid_data.xlsx** - covid daily data at local authority level
 - **covid_totals.xlsx** - covid totals data<br><br>

# Sample screenshots:
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshot1.png)
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshot2.png)

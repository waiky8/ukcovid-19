# UK Covid-19 Dashboard
There are plenty of (UK) covid dashboards available but this one can show comparisons at local authority level. It is built using **Dash**, written in **Python** and sources data from GovUK site https://coronavirus.data.gov.uk/details/download.<br><br>

**Mapbox** is used to show cases/deaths for each local authority with markers and hover text.<br><br>

The application is uploaded to **Heroku**. Check it out at https://ukcovid-19.herokuapp.com/<br>

# Features:
- Summary of cases/deaths
- Map with markers showing the covid cases and deaths for each local authority with varying size to depict the scale of numbers
- Bar charts showing cases/deaths for daily or cumulative figures

(reduced data to last 28 days to speed up callback refresh)<br><br>

# Input options:
- Select date
- Select local authorities
- Option to view number of cases or deaths
- Option to view daily data or cumulative data<br><br>

# Description of code/files:
 - **app.py** - main application code that show data for local authority
 - **app2.py** - main application code that show data for local area
 - **app_data_load.py** - code to retrieve latest data from GovUK
 - **covid_data.xlsx** - covid daily data at local authority level
 - **covid_totals.xlsx** - covid totals data<br><br>

# Sample screenshots:
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshot1.png)
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshot2.png)
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshot3.png)
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshot4.png)
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshot5.png)

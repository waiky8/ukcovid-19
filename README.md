# UK Covid-19 Dashboard
There are plenty of (UK) covid dashboards available but not many that show comparisons at local authority level. So I decided to build one using **Dash**, written in **Python** and sourcing the data from GovUK site https://coronavirus.data.gov.uk/details/download.<br><br>

**Dash** comes with many wonderful features (graphs, datatable, date picker, checkboxes, radio buttons etc.) that have been incorporated into the application.<br><br>

**Mapbox** is used to show cases/deaths for each local authority with markers and hover text.<br><br>

Data is refreshed and uploaded daily (semi-automated).<br><br>
The application is uploaded to **Heroku**. Check it out at https://ukcovid-19.herokuapp.com/<br><br>

# Features:
- Summary of cases/deaths
- Map with markers showing the covid cases and deaths for each local authority with varying size to depict the scale of numbers
- Bar charts showing cases/deaths for daily or cumulative figures
- Graphical timeline of cases for selected local authorities
- Graphical timeline of daily cases<br>

(reduced data to last 28 days to speed up callback refresh)<br><br>

# Input options:
- Select date
- View daily data or cumulative data
- View number of cases or deaths
- Select local authorities<br><br>

# Description of code/files:
 - **app.py** - main application code
 - **app_data_load.py** - code to retrieve latest data from GovUK
 - **covid_data.xlsx** - covid daily data at local authority level
 - **covid_totals.xlsx** - covid totals data<br><br>

# Sample screenshots:
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshot1.png)
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshot2.png)
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshot3.png)

# UK Covid-19 Dashboard
There are plenty of covid dashboards (uk) available but not many that show comparisons at local authority level.
I went for **Plotly Dash** as it was the simplest (& therefore best) to implement - the fact that there are a number of wonderful features (graphs, datatable, date picker) out of the box is a huge plus. Data is stored in **Excel** and is sourced from https://coronavirus.data.gov.uk/details/download.<br><br>
Included is a built in feature (under ADMIN tab) to upload new data. Unfortunatrely, due to a 30s processing time limit imposed by **heroku** (where the app is hosted), data refresh needs to be done locally (after 4pm UK when the data is published) and then pushed to heroku. A password lock on the admin tab has been implemented to ensure data integrity.<br><br>
Check it out at https://ukcovid-19.herokuapp.com/<br><br>
Sample.<br><br>
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshots/Screenshot_20210209-173221_Chrome.jpg)
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshots/Screenshot_20210209-173322_Chrome.jpg)
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshots/Screenshot_20210209-173337_Chrome.jpg)
![alt text](https://github.com/waiky8/ukcovid-19/blob/main/screenshots/Screenshot_20210209-173414_Chrome.jpg)

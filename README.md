## Gross Domestic Income (PIB) App for Mexico
What was last period's PIB (last official figure) and how good was it historically and compared with different government periods?  
This is the question this Dashboard aims to answer.

Using constant prices and controlling for seasonality, we can directly compare economy's general output (as measured by the gross domestic product) quarterly and build the histogram of economic growth.

### Framework
The app is going to be using the dash framework for dynamic dashboards which uses React, Flask and Python as the backend.

It uses [INEGI](https://www.inegi.org.mx/) api for querying official public figures. 

The app is deployed [here](https://mexico-pib.herokuapp.com)

### How to run the app
In python3:  
```
pip3 install -r requirements.txt
python3 app.py
```



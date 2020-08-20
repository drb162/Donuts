# Donuts
Part 1:

The Answers and scripts used to answer the first part of the case can be found in the GA Answers.pdf and analytics.sql respectively. 



Part 2 - Python script implementation:

A CryptoCurrencies class was created in the crypto.py file to interact with the mentioned API. The following functions were implemented inside the class:

get_timeseries_daily: returns daily data in pandas fromat from the API based on they cryptocurrency symbol and market. 

get_processed_timeseries_daily: returns daily closing value, 3 day rollinga average and 7 day rolling average in pandas fromat, based on they cryptocurrency symbol and market specified.

plot_timeseries: triggers a pyplot object depicting the given data. 

Python script will print the Bitcoin value in USD for the last 10 days and plot the last 1000 when run from the command line.


A docker image of the application can also be pulled from the dockerhub repository: drb162/donuts

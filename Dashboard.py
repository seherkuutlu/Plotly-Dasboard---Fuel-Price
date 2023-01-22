# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 21:47:37 2023

@author: Seher
"""

from dash import Dash, dcc, html
import plotly.express as px
from base64 import b64encode
import io
import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
from flask import Flask
import dash_lazy_load
import dash
import dash_html_components as html

import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np 
import sidetable
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
from IPython.display import display, HTML
import plotly.express as px
from keras import optimizers
from keras.layers import Dense, LSTM, RepeatVector, TimeDistributed, Flatten
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from datetime import datetime
import warnings
warnings.simplefilter('ignore')


data = pd.read_csv("weekly_fuel_prices_all_data_from_2005_to_20221102.csv",delimiter=";")
## object to datetime
data["SURVEY_DATE"] = data["SURVEY_DATE"].apply(pd.to_datetime, format="%Y-%m-%d")
data["Year"] = data["SURVEY_DATE"].dt.year
data["Month"] =  data["SURVEY_DATE"].dt.month
data["Day"] =  data["SURVEY_DATE"].dt.day_name()
data["Dummy"] = 1


daily_fuil = []
buffer = io.StringIO()

for i in data["PRODUCT_NAME"].unique():
    dataFilterPlot = data.loc[data["PRODUCT_NAME"] == i].reset_index(drop=True)
    daily_fuil.append(go.Scatter(x=dataFilterPlot['SURVEY_DATE'], y=dataFilterPlot['PRICE'],name=(f"{i}")))
    layout = go.Layout(title='Daily Fuil Price', xaxis=dict(title='Date'), yaxis=dict(title='Price'))
    
    fig = go.Figure(data=daily_fuil, layout=layout)
    #iplot(fig) 
    fig.write_html(buffer)
    
    fig.update_layout(
    updatemenus=[
        dict(
            #   active=0,
            buttons=list([
                dict(label="Default",
                     method="update",
                     args=[{"visible": [True, True, True, True, True, True]}],
                ),
                dict(label="Euro-Super 95",
                     method="update",
                     args=[{"visible": [True, False, False, False, False, False]}],
                ),
                dict(label="Automotive gas oil",
                     method="update",
                     args=[{"visible": [False, True, False, False, False, False]}],
                ),
                dict(label="Heating gas oil",
                     method="update",
                     args=[{"visible": [False, False, True, False, False, False]}],
                ),
                dict(label="LPG",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, False]}],
                ),
                dict(label="Residual fuel oil",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, False]}],
                ),
                dict(label="Heavy fuel oil",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, True]}],
                ),
            ]),
        )
])
    
    fig2 = px.box(data, x="Year", y="PRICE", color='PRODUCT_NAME',
             notched=True)
    fig2.write_html(buffer)
    
    fig2.update_layout(
    updatemenus=[
        dict(
            #   active=0,
            buttons=list([
                dict(label="Default",
                     method="update",
                     args=[{"visible": [True, True, True, True, True, True]}],
                ),
                dict(label="Euro-Super 95",
                     method="update",
                     args=[{"visible": [True, False, False, False, False, False]}],
                ),
                dict(label="Automotive gas oil",
                     method="update",
                     args=[{"visible": [False, True, False, False, False, False]}],
                ),
                dict(label="Heating gas oil",
                     method="update",
                     args=[{"visible": [False, False, True, False, False, False]}],
                ),
                dict(label="LPG",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, False]}],
                ),
                dict(label="Residual fuel oil",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, False]}],
                ),
                dict(label="Heavy fuel oil",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, True]}],
                ),
            ]),
        )
])
    
    fig3 = px.pie(data, values="Dummy", names="PRODUCT_NAME",
             color_discrete_sequence=px.colors.sequential.RdBu,
             opacity=0.7, hole=0.5)
    fig3.write_html(buffer)
    
    fig4 = px.box(data, x="PRODUCT_NAME", y="PRICE")
    fig4.write_html(buffer)
    
    html_bytes = buffer.getvalue().encode()
    encoded = b64encode(html_bytes).decode()

    app = JupyterDash(__name__) 
    app.layout = html.Div(children=[
        html.Div([
        html.H1(children='Line Plot'),

        html.Div(children='''
            Price distribution of fuel types according to years
        '''),

        dcc.Graph(
            id='graph1',
            figure=fig
        ),
        html.A(
        html.Button("Download as HTML"), 
        id="download",
        href="data:text/html;base64," + encoded,
        download="plotly_graph.html")    
    ]),
        
        html.Div([
        html.H1(children='Box Plot'),

        html.Div(children='''
            Examination of fuel types in terms of outliers
        '''),

        dcc.Graph(
            id='graph4',
            figure=fig4
        ),  
    ]),  
        
        html.Div([
        html.H1(children='Box Plot'),

        html.Div(children='''
            Examination of fuel types in terms of outliers on a yearly basis
        '''),

        dcc.Graph(
            id='graph2',
            figure=fig2
        ),  
    ]),
        
        html.Div([
        html.H1(children='Distribution of fuel types'),

        html.Div(children='''
            Equal data is available for all 6 fuel types.
        '''),

        dcc.Graph(
            id='graph3',
            figure=fig3
        ),  
    ]),  
        
        
])

if __name__ == '__main__':
    app.run_server(debug=True, mode="inline",port=8051)   
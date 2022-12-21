# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 04:23:11 2020

@author: A.FAISAL
"""
import os
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
#from flask import send_file
#from dash.exceptions import PreventUpdate
#from dash.dependencies import Input, Output

#server = Flask(__name__)
#download_dir = '/data'

app = dash.Dash(__name__)  
server = app.server
#USERNAME_PASSWORD_PAIRS = [['bigdata','bigdata']]
#auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)


city_df = pd.read_csv('data/city_df.csv')
state_df = pd.read_csv('data/state_df.csv')


px.set_mapbox_access_token("pk.eyJ1IjoiYXNpZmFsZmFpc2FsIiwiYSI6ImNrNGh5ajdjbzFmNWkzbHFld2NjZXprc3gifQ.shmAdMv1HDnZXZ6INjrshA")


fig_city = px.scatter_mapbox(city_df, lat="Lat", lon="Lon", color="City", size='Frequency', hover_data=['Links','Published Date'],
                  color_discrete_sequence=px.colors.qualitative.Prism, size_max=25, zoom=6)
fig_city.update_layout(margin=dict(l=0,r=0,b=0,t=40,pad=0),
                       title={'text': "Media Reports by City", 'x':0.5,'xanchor': 'center','yanchor': 'top'})


fig_state = px.scatter_mapbox(state_df, lat="Lat", lon="Lon", color="State", size='Frequency',
                  color_discrete_sequence=px.colors.qualitative.Set2, size_max=30, zoom=6)
fig_state.update_layout(margin=dict(l=0,r=0,b=0,t=40,pad=0),
                       title={'text': "Media Reports by State", 'x':0.5,'xanchor': 'center','yanchor': 'top'})


app.layout = html.Div([
    
    ## Header Section
    html.Div([
        
        html.Div([
            #html.Img(
            #    src=app.get_asset_url("cimmyt-logo.png"),
            #    id='cimmyt-logo',
            #    style={'height':'50px','width':'auto','margin':'auto'}
            #    )
            ],style={'display':'inline-block','width':'15%','margin-left':'5%','margin-top':'0%'}),
        
        
        html.Div([
            html.H4("ARRCC Media Reports Location Viewer", 
                    style={'margin-bottom':"0px",'margin-top':'0%'}),
            #html.P("This tool is designed to monitor incoming ODK data.", style={'margin-top':"0px"}),
            ],id = 'title', style={'display':'inline-block','width':'60%','textAlign':'center'}),
        
        ], id='header',className='pretty_container'),
    
    html.Div([
        html.Div([
            dcc.Graph(id='fig-map-city', figure=fig_city)
            ],className='pretty_container twelve columns'),
        ],className='row flex-display'),
    
   
    
    html.Div([
        html.Div([
            dcc.Graph(id='fig-map-state', figure=fig_state)
            ],className='pretty_container twelve columns'),
        ],className='row flex-display'),
    
    html.A(
        html.Button(
            #id='circos-download-button',
            #className='control-download',
            children="Download Data"
        ),
        href=os.path.join('assets', 'sample_data', 'data.zip'),
        download="media_reports.zip",
        ),
        
    html.Span("Developed by: Asif Al Faisal | CIMMYT",className='row flex-display')
    
    ],id="main-container",style={'display':'flex','flex-direction':'column'})

if __name__ == '__main__':
    app.run_server()

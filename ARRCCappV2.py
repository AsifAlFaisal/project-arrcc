# -*- coding: utf-8 -*-
"""
Created on Wed May 27 15:20:05 2020

@author: A.FAISAL
"""


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
import json
#from flask import send_file
#from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output

#server = Flask(__name__)
#download_dir = '/data'

app = dash.Dash(__name__)  
server = app.server
#USERNAME_PASSWORD_PAIRS = [['bigdata','bigdata']]
#auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)


dist_df = pd.read_csv('data/dist_df.csv')
#dist_df['Published Date'] = dist_df['Published Date'].apply(lambda x: datetime.datetime.strptime(x, "%d-%m-%y").date())
df = pd.DataFrame(dist_df['District'].value_counts())
df = df.reset_index()
df.columns = ['district','frequency']
dist_dict = dict(zip(dist_df['District'].unique(), dist_df['ID'].unique()))

for dd in df['district']:
    df.loc[df['district']==dd, 'ID'] = dist_dict.get(dd)

df['ID'] = df['ID'].round(0).astype(int)


with open('data/ind (1).json','r') as file:
    indiaJson = json.load(file)
    

for i, idx in enumerate(indiaJson['features']):
    indiaJson['features'][i]['id'] = i



fig = px.choropleth_mapbox(df, geojson=indiaJson, color="frequency", range_color=(0, df['frequency'].max()),
                           locations="ID", featureidkey="id",
                           labels={'district':'District'}, hover_data=['district'],
                           color_continuous_scale="Reds",
                           center={"lat": 29.837091, "lon": 76.040828},
                           mapbox_style="carto-positron", zoom=6)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


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
            dcc.Graph(id='fig-plot', figure=fig)
            ],className='pretty_container seven columns'),
        
        html.Div([
            dcc.Graph(id='fig-plot-bar')
            ],className='pretty_container five columns')

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






@app.callback(Output('fig-plot-bar', 'figure'),
              [Input('fig-plot','clickData')])
def hover_update(clickData):
    value = str(clickData['points'][0]['customdata'][0])
    temp_df = dist_df[dist_df['District']==value]
    #temp_df = dist_df.query("District=='{}'".format(value))
    temp_df2 = temp_df.groupby(['Published Date']).count().reset_index()
    temp_df2['District'] = temp_df['District'].unique()[0]
    temp_df2.columns = ['Published Date', 'District', 'Frequency', 'Lon', 'Lat', 'State','ID']
    temp_df2 = temp_df2[['Published Date','District','Frequency']]
    #temp_df2['week']=temp_df2['Published Date'].apply(lambda x: pd.to_datetime(x).week)
    
    fig2 = px.bar(temp_df2, x='Published Date', y='Frequency',
                  title='Incident Report Frequency by Published Date')
    fig2.update_xaxes(type='category')
    
    return fig2

if __name__ == '__main__':
    app.run_server(debug=False)

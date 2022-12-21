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


df = pd.read_csv('data/NEWS REPORTS.csv')
#dist_df['Published Date'] = dist_df['Published Date'].apply(lambda x: datetime.datetime.strptime(x, "%d-%m-%y").date())
#df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%y")
#df['WeekNumber'] = df['Date'].apply(lambda x: x.strftime("%V"))
temp = df['District'].value_counts().reset_index()
temp = dict(zip(temp['index'],temp['District']))
for dist in df['District']:
    df.loc[df['District']==dist, 'Count'] = temp.get(dist)


px.set_mapbox_access_token("pk.eyJ1IjoiYXNpZmFsZmFpc2FsIiwiYSI6ImNrNGh5ajdjbzFmNWkzbHFld2NjZXprc3gifQ.shmAdMv1HDnZXZ6INjrshA")


fig = px.scatter_mapbox(df, lat="Lat", lon="Lon", color="Count", size='Count',
                        hover_data=['ID','Link','Date','Country','State','District','Keyword'],
                        color_continuous_scale=px.colors.sequential.Reds, color_continuous_midpoint=0.1, 
                        size_max=20, zoom=4)
fig.update_layout(margin=dict(l=0,r=0,b=0,t=40,pad=0),
                  coloraxis_showscale=False,
                  title={'text': "Media Reports by District", 'x':0.5,'xanchor': 'center','yanchor': 'top'})





fig_anim = px.scatter_mapbox(df, lat="Lat", lon="Lon", color="Count", size='Count',
                             animation_frame='WeekNumber',
                             hover_data=['ID','Date','Country','State','District'],
                             color_continuous_scale=px.colors.sequential.Reds, color_continuous_midpoint=0.1, 
                             size_max=20, zoom=3)
fig_anim.update_layout(margin=dict(l=0,r=0,b=0,t=40,pad=0),
                       coloraxis_showscale=False,
                       updatemenus=[{'pad': {'b': 5, 't': 25}}],
                       sliders=[{'pad': {'b': 5, 't': 5}}],
                       title={'text': "Media Report Stream by Week", 'x':0.5,'xanchor': 'center','yanchor': 'top'})





country = []
state = []
week = []
count = []

for ct in df['Country'].unique():
    for st in df.loc[df['Country']==ct,'State'].unique():
        for wk in df.loc[(df['Country']==ct) & (df['State']==st),'WeekNumber'].unique():
            country.append(ct)
            state.append(st)
            week.append(wk)
            count.append(len(df.loc[(df['Country']==ct) & (df['State']==st) & (df['WeekNumber']==wk),'District'].unique()))
            #print(ct, st, wk, df.loc[(df['Country']==ct) & (df['State']==st) & (df['WeekNumber']==wk),'District'].unique())

freq_df = pd.DataFrame({'Country':country, 'State':state, 'Week':week, 'Frequency':count})



fig_bar = px.bar(freq_df, x='Week', y='Frequency', facet_col='State', facet_row='Country', color='Frequency',
                 color_continuous_scale=px.colors.sequential.Burg)


fig_bar.update_layout(coloraxis_showscale=False, title={'text':'Number of Reported Districts in Each State by Week', 'x':0.5})
#fig.update_xaxes(matches=None)
#fig.update_yaxes(matches=None)


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
            ],className='pretty_container ten columns'),
        
        
        html.Div([
            html.Img(
                src=app.get_asset_url("info-logo.svg"),
                style={'height':'30px','display':'inline-block','width':'40%'}),
            
            
            html.H6("Keyword",style={'display':'inline-block','width':'40%'}),
            
            html.Div(id='hover-data'),
            
            html.Div([
                html.A("News Source Link", id="url", href='/', target="_blank")
                ]),
            
            #html.Pre(id='hover-data')
            ],className='pretty_container three columns'),

        ],className='row flex-display'),
    
    html.Div([
        
        html.Div([
            dcc.Graph(id='fig-plot-bar', figure=fig_bar)
            ],className='pretty_container seven columns'),
        
        
        html.Div([
            dcc.Graph(id='fig-plot-anim', figure=fig_anim)
            ],className='pretty_container five columns'),

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




@app.callback(Output('hover-data', 'children'),
              [Input('fig-plot','clickData')])
def hover_update(clickData):
    
    #kw = str(clickData['points'][0]['customdata'][6].replace("+",", "))
    kw = clickData['points'][0]['customdata'][6].split('+')
    #kw.append("\\nLink: "+clickData['points'][0]['customdata'][1])
    
    return json.dumps(kw, indent=0)



@app.callback(Output('url', 'href'),
              [Input('fig-plot','clickData')])
def hover_link(clickData):
    
    ln= str(clickData['points'][0]['customdata'][1])
    
    return ln

if __name__ == '__main__':
    app.run_server(debug=False)

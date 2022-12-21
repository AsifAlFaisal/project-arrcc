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
from dash.dependencies import Input, Output, State
#import dash_auth
from dash.exceptions import PreventUpdate
#server = Flask(__name__)
#download_dir = '/data'

app = dash.Dash(__name__)  
server = app.server
#USERNAME_PASSWORD_PAIRS = [['bigdata','bigdata']]
#auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)





df = pd.read_csv('data/NEWS REPORTS.csv')
#weeks = pd.read_csv('data/weeks_2020.csv')
#weeks['Joint'] = weeks['Start'].astype(str) + " -- " + weeks['End'].astype(str)
#week_dict = dict(zip(weeks['week'], weeks['Joint']))
#df['WeekName'] = [week_dict[wk] for wk in df['WeekNumber']]

df['Year'] = pd.to_datetime(df['Date']).dt.year
df['WeekName'] = df['Year'].astype(str) + "_wk_" + df['WeekNumber'].astype(str)

#dist_df['Published Date'] = dist_df['Published Date'].apply(lambda x: datetime.datetime.strptime(x, "%d-%m-%y").date())
#df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%y")
#df['WeekNumber'] = df['Date'].apply(lambda x: x.strftime("%V"))

temp = df.groupby(by=['Year','District']).agg({'ID':'count'}).reset_index()
temp = dict(zip(temp["Year"].astype(str) +":" + temp["District"], temp['ID']))
df['YrDist'] = df["Year"].astype(str) +":" + df["District"]
for dist in df['YrDist']:
    df.loc[df['YrDist']==dist, 'Count'] = temp.get(dist)

px.set_mapbox_access_token("pk.eyJ1IjoiYXNpZmFsZmFpc2FsIiwiYSI6ImNrNGh5ajdjbzFmNWkzbHFld2NjZXprc3gifQ.shmAdMv1HDnZXZ6INjrshA")





yr20 = df.loc[df['Year'] == 2020,:]
yr21 = df.loc[df['Year'] == 2021,:]
yr22 = df.loc[df['Year'] == 2022,:]

yr20 = yr20.drop_duplicates(subset='District')
yr20 = yr20.groupby(by=['State','WeekName']).agg({'Country':'first','ID':'first','Year':'first','District':'count'}).reset_index().sort_values('ID').reset_index(drop=True)
yr21 = yr21.drop_duplicates(subset='District')
yr21 = yr21.groupby(by=['State','WeekName']).agg({'Country':'first','ID':'first','Year':'first','District':'count'}).reset_index().sort_values('ID').reset_index(drop=True)
yr22 = yr22.drop_duplicates(subset='District')
yr22 = yr22.groupby(by=['State','WeekName']).agg({'Country':'first','ID':'first','Year':'first','District':'count'}).reset_index().sort_values('ID').reset_index(drop=True)

for st in yr20['State'].unique():
    tmp_df = yr20[yr20['State'] == st]
    yr20.loc[yr20['State'] == st, 'Frequency'] = tmp_df['District'].cumsum().to_list()
    
for st in yr21['State'].unique():
    tmp_df = yr21[yr21['State'] == st]
    yr21.loc[yr21['State'] == st, 'Frequency'] = tmp_df['District'].cumsum().to_list()
for st in yr22['State'].unique():
    tmp_df = yr22[yr22['State'] == st]
    yr22.loc[yr22['State'] == st, 'Frequency'] = tmp_df['District'].cumsum().to_list()


rust_options = ['All','Yellow Rust', 'Leaf Rust', 'Stem Rust', 'Leaf, Stem, Stripe Rust', 'Leaf, Yellow Rust', 'Not Specified']
year_options = [yr for yr in df['Year'].unique()]

country_options = [ct for ct in df['Country'].unique()]

## IWWBR Newsletter Viz here #######

iiwbr_df = pd.read_csv('data/iiiwbr_newsletters.csv')
iiwbr_df['Year'] = pd.to_datetime(iiwbr_df['Date']).dt.year
newsletter_options = list(set(iiwbr_df['Source']))


##########

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
            html.Div([
                dcc.Dropdown(
                        id='year-picker',
                        options = [{'label':str(yr), 'value':yr} for yr in year_options],
                        placeholder="Select year",
                        className='dcc_control'
                        ),
           
                ],style={'display':'inline-block','width':'50%','textAlign':'center'}),
            html.Div([
                dcc.Dropdown(
                        id='type-picker1',
                        options = [{'label':tp, 'value':tp.lower()} for tp in rust_options],
                        placeholder="Select Disease",
                        className='dcc_control'
                        ),
           
                ],style={'display':'inline-block','width':'50%','textAlign':'center'}),
            
            html.Div([
                html.Button('Press Here!',id='submit-button')
                ]),
            
             dcc.Graph(id='fig-plot')
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
            dcc.Graph(id='fig-plot-anim')
            ],className='pretty_container six columns'),
        
        html.Div([
            
            dcc.Dropdown(
                        id='country-picker',
                        options = [{'label':ct, 'value':ct} for ct in country_options],
                        value = 'India',
                        className='dcc_control'
                        ),
            dcc.Graph(id='fig-plot-bar')
            ],className='pretty_container six columns'),
        

        ],className='row flex-display'),
    
    html.Div([html.H4("Extracted Information from Various Newsletter", style={'margin-bottom':"0px",'margin-top':'0%'})], 
             style={'display':'inline-block','textAlign':'center'},className='pretty_container'),
    
    html.Div([
                dcc.Dropdown(
                        id='newsletter-picker',
                        options = [{'label':nl, 'value':nl} for nl in newsletter_options],
                        value = newsletter_options[0],
                        className='dcc_control'
                        ),
           
                ],style={'display':'inline-block','width':'50%','textAlign':'center'}),
    
    html.Div([
        
        html.Div([
            #IIWBR Viz here
            dcc.Graph(id='fig-parallel'),
            dcc.Graph(id='fig-rep-gs')
            ],className='pretty_container six columns'),
        html.Div([
            #IIWBR Viz here
            
            dcc.Graph(id='fig-rep-dis'),
            dcc.Graph(id='fig-rep-var'),
            ],className='pretty_container six columns'),
        
        
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
        
    html.Span("Developed by: Asif Al Faisal | CIMMYT",className='row flex-display'),
    html.Span("Last updated: 24 February, 2022",className='row flex-display')
    
    ],id="main-container",style={'display':'flex','flex-direction':'column'})


@app.callback([Output('fig-plot', 'figure'),
               Output('fig-plot-anim', 'figure')],
              [Input('submit-button','n_clicks')],
              [State('type-picker1','value'), 
               State('year-picker','value')])
def update_maps(n_clicks,type_rust, year):
    if n_clicks is None:
        raise PreventUpdate
    else:
        
        if type_rust == 'all':
            new_df = df.copy()
            new_df = new_df.loc[(new_df['Year']==year),]
        else:
            new_df = df.loc[(df['Type'] == type_rust) & (df['Year']==year),:].reset_index(drop=True)     
        
        fig = px.scatter_mapbox(new_df, lat="Lat", lon="Lon", color="Count", size='Count', hover_data=['ID','Link','Date','Country','State','District','Keyword'],
                            color_continuous_scale=px.colors.sequential.Reds, color_continuous_midpoint=0.1, size_max=20, zoom=3)
        
        fig.update_layout(margin=dict(l=0,r=0,b=0,t=40,pad=0), coloraxis_showscale=False, 
                          title={'text': "Media Reports by District", 'x':0.5,'xanchor': 'center','yanchor': 'top'})
        
        
        fig_anim = px.scatter_mapbox(new_df, lat="Lat", lon="Lon", color="Count", size='Count', animation_frame='WeekName', hover_data=['ID','Date','Country','State','District'],
                                 color_continuous_scale=px.colors.sequential.Reds, color_continuous_midpoint=0.1, size_max=20, zoom=3)
        fig_anim.update_layout(margin=dict(l=0,r=0,b=0,t=40,pad=0), coloraxis_showscale=False,
                               updatemenus=[{'pad': {'b': 5, 't': 25}}],
                               sliders=[{'pad': {'b': 5, 't': 5}}],
                               title={'text': "Media Report Stream by Week", 'x':0.5,'xanchor': 'center','yanchor': 'top'})
            
        return fig, fig_anim
    

    
    
@app.callback(Output('fig-plot-bar', 'figure'),
              [Input('country-picker','value'),
               Input('year-picker','value')])
def update_bar(country, year):
    if year==2020:
        country_df = yr20.loc[yr20['Country'] == country,:].reset_index(drop=True)
    elif year==2021:
        country_df = yr21.loc[yr21['Country'] == country,:].reset_index(drop=True)
    elif year==2022:
        country_df = yr22.loc[yr22['Country'] == country,:].reset_index(drop=True)
    
    fig_bar = px.scatter(country_df, x='WeekName', y='Frequency', facet_col='State', facet_col_wrap=3, hover_data=['Year','WeekName','Frequency'], 
                         color='District', color_continuous_scale=px.colors.sequential.Burg)
    

    fig_bar.update_layout(coloraxis_showscale=False, title={'text':'Number of Reported Districts in Each State by Week', 'x':0.5})
    fig_bar.update_xaxes(matches=None)
    fig_bar.update_traces(mode='lines+markers')
    return fig_bar


@app.callback(
    [Output('fig-parallel','figure'),
     Output('fig-rep-gs','figure'),
     Output('fig-rep-dis','figure'),
     Output('fig-rep-var','figure')],
    [Input('newsletter-picker','value')]
    )
def newsletter_viz(nl_edition):
    
    iiwbr_df2 = iiwbr_df[iiwbr_df['Source'] == nl_edition]
    fig_iiwbr = px.parallel_categories(iiwbr_df2, color = 'Disease UID', dimensions=['Disease','District','Reported Variety'], 
                                   height=900, color_continuous_scale=px.colors.sequential.thermal, color_continuous_midpoint=4)
    fig_iiwbr.update_layout(coloraxis_showscale=False, title={'text': "Extracted Information from IIWBR Newsletter", 'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    # anothe way of representation
    fig_iiwbr2 = px.sunburst(iiwbr_df2[iiwbr_df2['Reported Variety'] != "No Info"], path=['Disease','District'], 
                             color='Disease', color_discrete_sequence=px.colors.qualitative.D3, height=400)
    fig_iiwbr2.update_layout(coloraxis_showscale=False, title={'text': "Affected Districts by Disease", 'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    
    
    # anothe way of representation
    fig_iiwbr3 = px.sunburst(iiwbr_df2[iiwbr_df2['Reported Variety'] != "No Info"], path=['Disease','Reported Variety'], 
                             color='Disease', color_discrete_sequence=px.colors.qualitative.D3, height=400)
    fig_iiwbr3.update_layout(coloraxis_showscale=False, title={'text': "Affected Varieties by Disease", 'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    # Total Reported Diseases Frequency
    rep_dis = iiwbr_df2.groupby(["Date","State","District"], sort=False, as_index=False)["Disease"].first()
    rep_dis = rep_dis.groupby(["Disease"], sort=False, as_index=False)["Date"].count()
    rep_dis.columns = ["Disease","Frequency"]
    rep_dis = rep_dis.sort_values("Frequency").reset_index(drop=True)
    fig_rep_dis = px.bar(rep_dis, x='Frequency', y='Disease', color_discrete_sequence=px.colors.sequential.RdBu, orientation='h', text='Frequency', height=400)
    fig_rep_dis.update_layout(coloraxis_showscale=False, title={'text': "Reported Disease Frequency", 'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    # Total reported variety frequency
    rep_var = iiwbr_df2['Reported Variety'].value_counts().reset_index()
    rep_var.columns = ["Reported Variety","Count"]
    fig_rep_var = px.bar(rep_var, y='Count', x="Reported Variety", color_discrete_sequence=px.colors.sequential.RdBu, text='Count', height=400)
    fig_rep_var.update_layout(coloraxis_showscale=False, title={'text': "Reported Affected Variety Frequency", 'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    # Total reported stages frequency
    rep_gs = iiwbr_df2.groupby(["Date","State","District"], sort=False, as_index=False)["Reported Growth Stage"].first()
    rep_gs = rep_gs.groupby(["Reported Growth Stage"], sort=False, as_index=False)["Date"].count()
    rep_gs.columns = ["Reported Growth Stage","Frequency"]
    rep_gs = rep_gs[rep_gs["Reported Growth Stage"] != "No Info"]
    rep_gs = rep_gs.sort_values("Frequency").reset_index(drop=True)
    
    fig_rep_gs = px.bar_polar(rep_gs, r='Frequency', theta='Reported Growth Stage', color='Frequency', color_continuous_scale=px.colors.sequential.GnBu, color_continuous_midpoint=1,
                              height=300)
    fig_rep_gs.update_layout(polar = dict(radialaxis = dict(dtick = 1)))
    fig_rep_gs.update_layout(coloraxis_showscale=False, title={'text': "Reported Growth Stage Frequency", 'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    return fig_iiwbr2, fig_iiwbr3, fig_rep_dis, fig_rep_var




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

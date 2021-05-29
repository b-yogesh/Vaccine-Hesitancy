import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
master_df = pd.read_csv('Data/master.csv')

stats_df = master_df.groupby('SVI Category', as_index = False).median()

vulnerability_order = ["Very High Vulnerability","High Vulnerability", "Moderate Vulnerability", "Low Vulnerability","Very Low Vulnerability"]
vulnerability_colours = ["orange","blue","yellow","red","green"]

hesitant_vs_SVI = go.Bar(x=stats_df["SVI Category"], y=stats_df["Estimated hesitant"], marker_color=vulnerability_colours)

fig1 = go.Figure(hesitant_vs_SVI)

fig2_data = master_df.copy()
fig2_data = fig2_data.groupby('State', as_index = False).sum()
fig2 = px.scatter(fig2_data, x= "Estimated hesitant" , y = "deaths", color = "State")

fig1.update_layout(xaxis={'categoryorder':'array', 'categoryarray':vulnerability_order},title={
        'text': "Hesitancy by Social Vulnerability Category",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

fig2.update_layout(xaxis={'categoryorder':'array', 'categoryarray':vulnerability_order},title={
        'text': "Number of COVID-19 Cases vs. Estimated Vaccine Acceptance",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

app.layout = html.Div(children=[
    html.H1(children='Vaccine Hesitancy - Team 5'),
    dcc.Graph(
        id='hesitant_vs_SVI',
        figure=fig1,
    ),
      dcc.Graph(
        id='scatter',
        figure=fig2,
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

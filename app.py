import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Load your new CSV data
data = pd.read_csv('Data/UdupiCrimeData.csv', encoding='utf-8')

# Define time of day labels
time_of_day_mapping = {
    0: "Midnight",
    1: "Early Morning",
    2: "Morning",
    3: "Afternoon",
    4: "Evening",
}

# Define month labels
month_labels = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}

app = dash.Dash(__name__)

options_crime_type = [{'label': 'Select All: Crime Type', 'value': 'Select All: Crime Type'}] + [{'label': crime_type, 'value': crime_type} for crime_type in data['Crime Type English'].unique()]
options_location = [{'label': 'Select All: Location', 'value': 'Select All: Location'}] + [{'label': location, 'value': location} for location in data['Location English'].unique()]
options_year = [{'label': 'Select All: Year', 'value': 'Select All: Year'}] + [{'label': year, 'value': year} for year in data['Year'].unique()]
options_month = [{'label': month_labels[month], 'value': month} for month in range(1, 13)] + [{'label': 'Select All: Month', 'value': 'Select All: Month'}]
options_time_of_day = [{'label': f'Select All: Time of Day', 'value': 'Select All: Time of Day'}] + [{'label': time_of_day, 'value': time_of_day} for time_of_day in time_of_day_mapping.values()]

# Define color scale for months
month_color_scale = px.colors.qualitative.Set1

# Define color scale for crime types
crime_color_scale = px.colors.qualitative.Set2

# Define color scale for time of day
time_color_scale = px.colors.qualitative.Pastel1

# Styling for the app
app.layout = html.Div([
    html.Div([
        html.H1("Crime Report Dashboard", style={'text-align': 'center'}),
        html.Hr(),
    ]),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crime-type-dropdown',
                options=options_crime_type,
                value='Select All: Crime Type',
                multi=True,
                clearable=True,
                placeholder='Select Crime Type(s)'
            ),
            dcc.Dropdown(
                id='location-dropdown',
                options=options_location,
                value='Select All: Location',
                multi=True,
                clearable=True,
                placeholder='Select Location(s)'
            ),
        ]),

        html.Div([
            dcc.Dropdown(
                id='year-dropdown',
                options=options_year,
                value='Select All: Year',
                multi=True,
                clearable=True,
                placeholder='Select Year(s)'
            ),
            dcc.Dropdown(
                id='month-dropdown',
                options=options_month,
                value='Select All: Month',
                multi=True,
                clearable=True,
                placeholder='Select Month(s)'
            ),
        ]),

        html.Div([
            dcc.Dropdown(
                id='time-of-day-dropdown',
                options=options_time_of_day,
                value='Select All: Time of Day',
                multi=True,
                clearable=True,
                placeholder='Select Time of Day(s)'
            ),
        ]),
    ], style={'background-color': 'lightgray', 'padding': '10px'}),

    dcc.Graph(id='crime-type-plot', config={'displayModeBar': False}),

    html.Div([
        html.H2("Insights and Analysis", style={'text-align': 'center'}),
        html.P("This dashboard provides insights into crime data, including distribution by crime type, location, time of day, and more."),
        html.P("Use the filters above to explore the data based on your criteria."),
        html.P("Insight 1: Crime Type Distribution - The chart displays the distribution of crime types."),
        html.P("Insight 2: Location Distribution - The chart shows where the crimes are concentrated."),
        html.P("Insight 3: Yearly Trends - The graph highlights yearly crime trends."),
        html.P("Insight 4: Monthly Patterns - Observe the monthly patterns of crimes."),
    ], style={'background-color': 'lightgray', 'padding': '20px'}),
])

# Callback function
@app.callback(
    Output('crime-type-plot', 'figure'),
    Input('crime-type-dropdown', 'value'),
    Input('location-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('month-dropdown', 'value'),
    Input('time-of-day-dropdown', 'value')
)
def update_plot(selected_crime_type, selected_location, selected_year, selected_month, selected_time_of_day):
    filtered_data = data

    if 'Select All: Crime Type' not in selected_crime_type:
        filtered_data = filtered_data[filtered_data['Crime Type English'].isin(selected_crime_type)]

    if 'Select All: Location' not in selected_location:
        filtered_data = filtered_data[filtered_data['Location English'].isin(selected_location)]

    if 'Select All: Year' not in selected_year:
        filtered_data = filtered_data[filtered_data['Year'].isin(selected_year)]
    
    if 'Select All: Month' not in selected_month:
        filtered_data = filtered_data[filtered_data['Month'].isin(selected_month)]

    if 'Select All: Time of Day' not in selected_time_of_day:
        selected_time_of_day = [key for key, value in time_of_day_mapping.items() if value in selected_time_of_day]
        filtered_data = filtered_data[filtered_data['Time of Day'].isin(selected_time_of_day)]

    if len(selected_year) == 1:
        # Plot for specific year, crime type, month, and time of day
        filtered_counts = filtered_data.groupby(['Month', 'Crime Type English']).size().reset_index(name='Count')
        fig = px.bar(
            filtered_counts,
            x='Month',
            y='Count',
            title=f'Crime Counts by Month and Crime Type for {selected_crime_type[0]} in {selected_year[0]} during {selected_time_of_day[0]}',
            color='Crime Type English',  
            color_discrete_sequence=crime_color_scale,
        )
    else:
        # Plot for all years, crime types, months, and time of day
        filtered_counts = filtered_data.groupby(['Month', 'Crime Type English']).size().reset_index(name='Count')
        fig = px.bar(
            filtered_counts,
            x='Month',
            y='Count',
            title='Crime Counts by Month and Crime Type',
            color='Crime Type English',  
            color_discrete_sequence=crime_color_scale,
        )

    fig.update_xaxes(title_text='Month', showgrid=False)
    fig.update_yaxes(title_text='Crime Count', showgrid=False)
    fig.update_layout(plot_bgcolor='white', margin=dict(l=20, r=20, t=50, b=20))

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

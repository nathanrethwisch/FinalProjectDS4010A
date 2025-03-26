import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
import dash_leaflet as dl
app = dash.Dash(external_stylesheets=[dbc.themes.SIMPLEX])

theme = {

}

app.layout = html.Div([
    # Top Navigation Bar
    html.Div([
        html.H2("Wildfire"),
        # Add navigation links or components here
    ], style={'width': '100%', 'display': 'block', 'backgroundColor': '#f8f9fa', 'padding': '10px', 'textAlign': 'center'}
    ),

    # Main Content Area with Sidebars
    html.Div([
        # Left Sidebar
        html.Div([
            html.H3("Data"),
            # Add components for the left sidebar here
        ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'backgroundColor': '#e9ecef', 'padding': '10px'}
        ),

        # Central Content Area
        html.Div([
            html.H3("Map"),
            # Add main content components and plots here
            dl.Map([
                dl.TileLayer()
            ], center=[40,-95], zoom=4, style={'height': '50vh'}, id="map"),
            html.Button("Recenter", id="btn")

        ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}
        ),

        # Right Sidebar
        html.Div([
            html.H3("Model"),
            # Add components for the right sidebar here
        ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'backgroundColor': '#e9ecef', 'padding': '10px'}
        ),
    ], style={'width': '100%', 'display': 'block'}),
    html.Div([
        html.H3('Bottom Panel')
    ])
])


@app.callback(Output("map", "viewport"), Input("btn", "n_clicks"), prevent_initial_call=True)
def recenter(_):
    return dict(center=[40,-95], zoom=4, transition="flyTo")





if __name__ == "__main__":
    app.run(debug=True, dev_tools_hot_reload=True)

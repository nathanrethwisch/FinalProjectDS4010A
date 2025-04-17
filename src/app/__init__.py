import dash_leaflet as dl
import geopandas as gpd
import matplotlib.colors as mcolors
from dash import html
from dash_leaflet import Polygon, BaseLayer

from .utils import *





def generate_polys(gdf: gpd.GeoDataFrame, field: str) -> list[Polygon]:
    """
    return a list of polys to be passed into a layergroup
    """
    cmap = get_colormap_choice(field)

    # Defines a nonlinear scale to adjust the color bar
    def nonlinear_scale(x):
        return x ** 0.5  
    
    # We don't want to use this scale for temperature because they are normally distributed - while these other values are right-skewed
    nonlinear_fields = [
        "Normalized Predicted Fire Probability", 
        "Normalized Precipitation (3-Day Average)", 
        "Normalized Snowfall (3-Day Average)",
        "Normalized Daily Average Wind (3-Day Average)"
    ]

    polygons: [dl.Polygon] = []
    for _, row in gdf.iterrows():
        polygon = row["geometry"]
        coordinates = [[lat, lon] for lat, lon in polygon.exterior.coords]
        value = row[field]  # Field value for the polygon

        # Apply nonlinear transformation only to selected fields 
        if field in nonlinear_fields:
            transformed_value = nonlinear_scale(value)
        else:
            transformed_value = value  

        # Get color based on the (possibly nonlinear) transformed value
        color = mcolors.to_hex(cmap(transformed_value))  

        polygons.append(
            dl.Polygon(positions=coordinates, color=color, fillColor=color, fillOpacity=0.6,
                       weight=1,)
        )
    return polygons




def generate_layers(gdf: gpd.GeoDataFrame, date_str: str) -> list[dl.BaseLayer]:
        overlays: list[dl.BaseLayer] = []
        for i, field in enumerate(field_identifiers):
            
            #Takes off the word normalized for display
            display_name = field.replace("Normalized ", "")
            polys = generate_polys(gdf, field)
    
            poly_layer = dl.FeatureGroup(
                polys,
                interactive=True,
                id=f"group-{field}-{date_str}"
            )
    
            overlay = dl.BaseLayer(
                poly_layer,
                name=display_name,  # Use display name without "Normalized"
                id=f"overlay-{field}-{date_str}",
                checked=(i == 0)  # Only the first field is selected by default
            )
    
            overlays.append(overlay)
    
        return overlays






def generate_colorbar(field, n_ticks):
    
    # Remove "Normalized" part of the field name for the colorbar
    display_name = field.replace("Normalized ", "")
    
    cmap = get_colormap_choice(field)
    min_val, max_val = get_field_range(field)

    # Nonlinear scale (same as for colorbar)
    def nonlinear_scale(x):
        return x ** 0.5  # You can adjust this function (e.g., to loglike_scale if needed)

    # Don't scale for temperature fields
    nonlinear_fields = [
        "Normalized Predicted Fire Probability", 
        "Normalized Precipitation (3-Day Average)", 
        "Normalized Snowfall (3-Day Average)",
        "Normalized Daily Average Wind (3-Day Average)"
    ]

    n_grad_steps = 24
    steps = []
    
    # Apply the nonlinear transformation back to the selected fields with 24 steps
    for i in range(n_grad_steps):
        value = i / (n_grad_steps - 1)
        if field in nonlinear_fields:
            transformed_value = nonlinear_scale(value)
        else:
            transformed_value = value  
        # Get color based on the transformed value
        steps.append(cmap(transformed_value))
        
    hex_colors = [mcolors.to_hex(c) for c in steps]
    gradient = f'linear-gradient(to right, {", ".join(hex_colors)})'

    # The gradient bar styling
    gradient_style = {
        'height': '20px',
        'width': '100%',
        'background': gradient,
        'border': '1px solid #ccc',
        'borderRadius': '4px',
        'position': 'relative'
    }

    # Tick marks and labels
    tick_elements = []
    for i, val in enumerate(np.linspace(min_val, max_val, n_ticks)):
        left_percent = (i / (n_ticks - 1)) * 100

        tick_mark_style = {
            'position': 'absolute',
            'top': '0px',
            'left': f'{left_percent}%',
            'width': '1px',
            'height': '8px',
            'background': 'black',
            'transform': 'translateX(-50%)'
        }

        tick_label_style = {
            'position': 'absolute',
            'top': '12px',
            'left': f'{left_percent}%',
            'transform': 'translateX(-50%)',
            'fontSize': '12px',
            'textAlign': 'center'
        }

        tick_elements.append(html.Div([], style=tick_mark_style))
        tick_elements.append(html.Div(format_field_values(val, field), style=tick_label_style))

    ticks_container_style = {
        'position': 'relative',
        'width': '100%',
        'height': '40px'
    }

    ticks_container = html.Div(tick_elements, style=ticks_container_style)

    # Final colorbar
    return html.Div([
        html.Div(style=gradient_style),
        ticks_container
    ])


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

    polygons: [dl.Polygon] = []
    for _, row in gdf.iterrows():
        polygon = row["geometry"]
        coordinates = [[lat, lon] for lat, lon in polygon.exterior.coords]
        value = row[field]  # Now the field value is normalized (0 to 1)
        color = mcolors.to_hex(cmap(value))  # Apply colormap
        
        polygons.append(
            dl.Polygon(positions=coordinates, color=color, fillColor=color, fillOpacity=0.6,
                       weight=1,)
        )
    return polygons


def generate_layers(gdf: gpd.GeoDataFrame, date_str: str) -> list[dl.BaseLayer]:
    overlays: list[dl.BaseLayer] = []
    for i, field in enumerate(field_identifiers):
        gdf_copy = gdf.copy()
        gdf_copy = normalize_to_field_range(gdf_copy, field)
        polys = generate_polys(gdf_copy, field)

        poly_layer = dl.FeatureGroup(
            polys,
            interactive=True,
            id=f"group-{field}-{date_str}"
        )

        overlay = dl.BaseLayer(
            poly_layer,
            name=field,
            id=f"overlay-{field}-{date_str}",
            checked=(i == 0)  # Only the first field is selected by default
        )

        overlays.append(overlay)

    return overlays




def generate_colorbar(field, n_ticks):
    cmap = get_colormap_choice(field)
    min_val, max_val = get_field_range(field)

    # Build a linear gradient with discrete steps
    n_grad_steps = 24
    steps = [cmap(i / (n_grad_steps - 1)) for i in range(n_grad_steps)]
    hex_colors = [mcolors.to_hex(c) for c in steps]
    gradient = f'linear-gradient(to right, {", ".join(hex_colors)})'

    # The gradient bar with relative positioning
    gradient_style = {
        'height': '20px',
        'width': '100%',
        'background': gradient,
        'border': '1px solid #ccc',
        'borderRadius': '4px',
        'position': 'relative'
    }

    # Container for tick marks and labels (absolute positioning relative to its own container)
    tick_elements = []
    for i, val in enumerate(np.linspace(min_val, max_val, n_ticks)):
        # Compute left position as a percentage along the bar.
        left_percent = (i / (n_ticks - 1)) * 100
        # Tick mark: a short vertical line on the colorbar.
        tick_mark_style = {
            'position': 'absolute',
            'top': '0px',
            'left': f'{left_percent}%',
            'width': '1px',
            'height': '8px',
            'background': 'black',
            'transform': 'translateX(-50%)'
        }
        # Tick label: positioned below the colorbar.
        tick_label_style = {
            'position': 'absolute',
            'top': '12px',
            'left': f'{left_percent}%',
            'transform': 'translateX(-50%)',
            'fontSize': '12px',
            'textAlign': 'center'
        }
        tick_elements.append(html.Div([], style=tick_mark_style))

        # noinspection PyTypeChecker
        # type: ignore[assignment]
        tick_elements.append(html.Div(format_field_values(val, field), style=tick_label_style))

    ticks_container_style = {
        'position': 'relative',
        'width': '100%',
        'height': '40px'
    }

    ticks_container = html.Div(tick_elements, style=ticks_container_style)

    # Assemble the colorbar with ticks below the gradient bar.
    return html.Div([
        html.Div(style=gradient_style),
        ticks_container
    ])

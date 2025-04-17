import matplotlib as mpl
import numpy as np

field_identifiers: [str] = ['Normalized Predicted Fire Probability', 'Normalized Precipitation (3-Day Average)', 'Normalized Temperature Maximum (3-Day Average)', 'Normalized Temperature Minimum (3-Day Average)', 'Normalized Snowfall (3-Day Average)', 'Normalized Average Elevation', 'Normalized Daily Average Wind (3-Day Average)']

_field_colormaps = {
    "Normalized Predicted Fire Probability": mpl.cm.get_cmap("RdYlGn_r"),  # green = low, red = high
    "Normalized Precipitation (3-Day Average)": mpl.cm.get_cmap("Blues"),  # blue scale for precipitation
    "Normalized Temperature Maximum (3-Day Average)": mpl.cm.get_cmap("turbo"),  # hot for max temp
    "Normalized Temperature Minimum (3-Day Average)": mpl.cm.get_cmap("turbo"),  # cool for min temp
    "Normalized Snowfall (3-Day Average)": mpl.cm.get_cmap("PuBuGn"),  # purple-blue-green for snow
    "Normalized Average Elevation": mpl.cm.get_cmap("Greens"),
    'Normalized Daily Average Wind (3-Day Average)': mpl.cm.get_cmap("YlOrRd"),
}

_field_ranges = {
    "Normalized Predicted Fire Probability": (0.0, 1.0),
    "Normalized Precipitation (3-Day Average)": (0, 1230),  # 40 mm
    "Normalized Temperature Maximum (3-Day Average)": (-400, 830),  # -25°C to 50°C
    "Normalized Temperature Minimum (3-Day Average)": (-400, 830),  # -25°C to 50°C
    "Normalized Snowfall (3-Day Average)": (0, 340),  
    "Normalized Average Elevation": (-74, 2855),
    "Normalized Daily Average Wind (3-Day Average)": (0, 90),
}

_field_formatter_funcs = {
    "Normalized Predicted Fire Probability": lambda s: f"{s:.0%}",
    "Normalized Precipitation (3-Day Average)": lambda s: f"{s / 10:.0f}mm",
    "Normalized Temperature Maximum (3-Day Average)": lambda s: f"{s * 0.18 + 32:.0f}°F",
    "Normalized Temperature Minimum (3-Day Average)": lambda s: f"{s * 0.18 + 32:.0f}°F",
    "Normalized Snowfall (3-Day Average)": lambda s: f"{s / 10:.0f}mm",
    "Normalized Average Elevation": lambda s: f"{(s * 3.28084):,.0f} ft",    
    "Normalized Daily Average Wind (3-Day Average)": lambda s: f"{(s * 0.1 * 2.23694):,.1f} mph",
}

# Function to get the display name (without 'Normalized')
def get_display_name(field: str) -> str:
    friendly_names = {
        "Normalized Predicted Fire Probability": "Fire Probability",
        "Normalized Precipitation (3-Day Average)": "Precipitation (3-Day Average)",
        "Normalized Temperature Maximum (3-Day Average)": "Temperature Maximum (3-Day Average)",
        "Normalized Temperature Minimum (3-Day Average)": "Temperature Minimum (3-Day Average)",
        "Normalized Snowfall (3-Day Average)": "Snowfall (3-Day Average)",
        "Normalized Average Elevation": "Average Elevation",
        "Normalized Daily Average Wind (3-Day Average)": "Daily Average Wind",
    }
    return friendly_names.get(field, field)

def get_colormap_choice(field):
    """
    Return a matplotlib colormap object appropriate for the selected weather field.
    """
    if field not in _field_colormaps:
        print("[app.utils._viz_helpers.py.get_field_range()] Field not found in predefined field colormaps")
        return mpl.cm.get_cmap("viridis")
    return _field_colormaps.get(field)

def get_field_range(field: str) -> tuple[float, float]:
    """
    Return predefined vmin and vmax for each field.
    These values are in the units of the raw dataset.
    """
    if field not in _field_ranges:
        print("[app.utils._viz_helpers.py.get_field_range()] Field not found in predefined field ranges")
        return 0, 1
    return _field_ranges.get(field)

def format_field_values(x: float, field: str) -> str:
    if field not in _field_formatter_funcs:
        print("[app.utils._viz_helpers.py.get_field_range()] Field not found in predefined field formatters")
        return str(x)
    fn = _field_formatter_funcs.get(field)
    return fn(x)





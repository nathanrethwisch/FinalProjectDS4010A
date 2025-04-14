import matplotlib as mpl
import numpy as np

field_identifiers = ['Normalized Fire Probability', 'Precipitation (3-Day Average)', 'Temperature Maximum (3-Day Average)', 'Temperature Minimum (3-Day Average)', 'Snowfall (3-Day Average)']#, 'Average Elevation', 'Daily Average Wind (3-Day Avereage)']

_field_colormaps = {
    "Normalized Fire Probability": mpl.cm.get_cmap("RdYlGn_r"),  # green = low, red = high
    "Precipitation (3-Day Average)": mpl.cm.get_cmap("Blues"),  # blue scale for precipitation
    "Temperature Maximum (3-Day Average)": mpl.cm.get_cmap("turbo"),  # hot for max temp
    "Temperature Minimum (3-Day Average)": mpl.cm.get_cmap("turbo"),  # cool for min temp
    "Snowfall (3-Day Average)": mpl.cm.get_cmap("PuBuGn"),  # purple-blue-green for snow
}
_field_ranges = {
    "Normalized Fire Probability": (0.0, 1.0),
    "Precipitation (3-Day Average)": (0, 400),  # 40 mm
    "Temperature Maximum (3-Day Average)": (-240, 560),  # -25°C to 50°C
    "Temperature Minimum (3-Day Average)": (-240, 560),  # -25°C to 50°C
    "Snowfall (3-Day Average)": (0, 200),  # 20 mm
}
_field_formatter_funcs = {
    "Normalized Fire Probability": lambda s: f"{s:.0%}",
    "Precipitation (3-Day Average)": lambda s: f"{s / 10:.0f}mm",
    # "Temperature Maximum (3-Day Average)": lambda s: f"{s / 10:.0f}°C",
    "Temperature Maximum (3-Day Average)": lambda s: f"{s * 0.18 + 32:.0f}°F",
    # "Temperature Minimum (3-Day Average)": lambda s: f"{s / 10:.0f}°C",
    "Temperature Minimum (3-Day Average)": lambda s: f"{s * 0.18 + 32:.0f}°F",
    "Snowfall (3-Day Average)": lambda s: f"{s / 10:.0f}mm",

}


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


def normalize_to_field_range(gdf, field):
    vmin, vmax = get_field_range(field)
    gdf[field] = (gdf[field] - vmin) / (vmax - vmin)
    gdf[field] = np.clip(gdf[field], 0, 1)
    return gdf


# normalize_to_climate_range replaces this
def normalize(gdf, field):
    """
    Assign Colors to values
    """
    min_val = gdf[field].min()
    max_val = gdf[field].max()
    gdf[field] = (gdf[field] - min_val) / (max_val - min_val)
    # mean_shift = 0.5 - gdf[field].mean()
    # gdf[field] += mean_shift
    gdf[field] = np.clip(gdf[field], 0, 1)
    return gdf

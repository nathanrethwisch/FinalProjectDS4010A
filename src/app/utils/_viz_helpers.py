import matplotlib as mpl
import numpy as np

field_identifiers = ['normalized_probabilities', 'prcp_avg', 'tmax_avg', 'tmin_avg', 'snow_avg']

_field_colormaps = {
    "normalized_probabilities": mpl.cm.get_cmap("RdYlGn_r"),  # green = low, red = high
    "prcp_avg": mpl.cm.get_cmap("Blues"),  # blue scale for precipitation
    "tmax_avg": mpl.cm.get_cmap("turbo"),  # hot for max temp
    "tmin_avg": mpl.cm.get_cmap("turbo"),  # cool for min temp
    "snow_avg": mpl.cm.get_cmap("PuBuGn"),  # purple-blue-green for snow
}
_field_ranges = {
    "normalized_probabilities": (0.0, 1.0),
    "prcp_avg": (0, 400),  # 40 mm
    "tmax_avg": (-240, 560),  # -25°C to 50°C
    "tmin_avg": (-240, 560),  # -25°C to 50°C
    "snow_avg": (0, 200),  # 20 mm
}
_field_formatter_funcs = {
    "normalized_probabilities": lambda s: f"{s:.0%}",
    "prcp_avg": lambda s: f"{s / 10:.0f}mm",
    # "tmax_avg": lambda s: f"{s / 10:.0f}°C",
    "tmax_avg": lambda s: f"{s * 0.18 + 32:.0f}°F",
    # "tmin_avg": lambda s: f"{s / 10:.0f}°C",
    "tmin_avg": lambda s: f"{s * 0.18 + 32:.0f}°F",
    "snow_avg": lambda s: f"{s / 10:.0f}mm",

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

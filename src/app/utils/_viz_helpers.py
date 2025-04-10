import matplotlib as mpl
import numpy as np

field_colormaps = {
    'normalized_probabilities': mpl.cm.get_cmap("RdYlGn_r"),  # green = low, red = high
    'prcp_avg': mpl.cm.get_cmap("Blues"),  # blue scale for precipitation
    'tmax_avg': mpl.cm.get_cmap("hot"),  # hot for max temp
    'tmin_avg': mpl.cm.get_cmap("cool"),  # cool for min temp
    'snow_avg': mpl.cm.get_cmap("PuBuGn"),  # purple-blue-green for snow
}
field_ranges = {
    'normalized_probabilities': (0.0, 1.0),
    'prcp_avg': (0, 200),  # 20 mm
    'tmax_avg': (-250, 350),  # -25°C to 35°C
    'tmin_avg': (-250, 350),  # -25°C to 35°C
    'snow_avg': (0, 200),  # 20 mm
}


def get_colormap_choice(field):
    """
    Return a matplotlib colormap object appropriate for the selected weather field.
    """
    return field_colormaps.get(field, mpl.cm.get_cmap("viridis"))  # fallback to viridis


def get_field_range(field):
    """
    Return predefined vmin and vmax for each field.
    These values are in the units of the raw dataset.
    """
    return field_ranges.get(field, (0, 1))  # fallback


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

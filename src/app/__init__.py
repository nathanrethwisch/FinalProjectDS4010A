from datetime import date

from dash import dcc

field_selection = dcc.RadioItems(
    id='field-checklist',
    options=[
        {'label': 'Precipitation', 'value': 'prcp'},
        {'label': 'Max Temperature', 'value': 'tmax'},
        {'label': 'Min Temperature', 'value': 'tmin'},
        {'label': 'Snowfall', 'value': 'snow'},
        {'label': 'Wind', 'value': 'snwd'}
    ],
    value=None
)

date_picker = dcc.DatePickerSingle(
    id='date-picker',
    min_date_allowed=date(2000, 1, 1),
    max_date_allowed=date(2025, 2, 28),
    initial_visible_month=date(2020, 1, 1),
    date=date(2020, 1, 1),
)

def get_layer(selected_field, date):
    pass

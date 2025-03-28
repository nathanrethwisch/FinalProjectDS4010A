from datetime import date

from dash import dcc

field_selection = dcc.Checklist(
    id='field-checklist',
    options=[
        {'label': 'Precipitation', 'value': 'precipitation'},
        {'label': 'Max Temperature', 'value': 'max_temp'},
        {'label': 'Min Temperature', 'value': 'min_temp'}
    ],
    value=[]
)

date_picker = dcc.DatePickerSingle(
    id='date-picker',
    min_date_allowed=date(2000, 1, 1),
    max_date_allowed=date(2025, 2, 28),
    initial_visible_month=date(2020, 1, 1),
    date=date(2020, 1, 1),
)

import pandas as pd
import plotly.express as px
from datetime import datetime

# Load your fire data
# fire = pd.read_parquet("path_to_your/Fire_Occurence.parquet")

# Prepare the weekly fire count data
fire["DISCOVERYDATE"] = pd.to_datetime(fire["DISCOVERYDATE"])  # convert to datetime
fire["week"] = fire["DISCOVERYDATE"].dt.to_period("W").apply(lambda r: r.start_time)  # floor to week

fires_week = fire.groupby("week").size().reset_index(name="fire_count")

# Create the plotly line chart
fig = px.line(
    fires_week,
    x="week",
    y="fire_count",
    title="Weekly Fire Count",
    labels={"week": "Week", "fire_count": "Number of Fires"}
)

# Style the plot
fig.update_traces(
    mode="lines+markers",
    line=dict(color="firebrick", width=2),
    marker=dict(size=4),
    name="Fires per Week"
)

fig.update_layout(
    xaxis=dict(
        title="Week",
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all", label="All")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    ),
    yaxis=dict(title="Number of Fires"),
    hovermode="x unified"
)

# View the plot (in Jupyter/Notebook) or export
fig.show()

# To save as an HTML file:
fig.write_html("fire_timeseries.html", include_plotlyjs="cdn")

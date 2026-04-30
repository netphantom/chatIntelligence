import pandas as pd
import streamlit as st
from plotly import express as px

from view.charts.ChartStrategy import ChartStrategy


class PeriodicityHeatmapStrategy(ChartStrategy):
    @property
    def title(self) -> str:
        return "Circadian and Weekly Rhythm Analysis"

    def render(self, df: pd.DataFrame) -> None:
        # Prepare data for heatmap: Day of week vs Hour of day
        heatmap_data = df.copy()
        heatmap_data["hour"] = heatmap_data.index.hour
        heatmap_data["day_of_week"] = heatmap_data.index.day_name()

        # Correct ordering of days
        days_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        pivot = (
            heatmap_data.groupby(["day_of_week", "hour"]).size().unstack(fill_value=0)
        )
        pivot = pivot.reindex(days_order)

        fig = px.imshow(
            pivot,
            labels=dict(x="Hour of Day", y="Day of Week", color="Messages"),
            title="Temporal Distribution of Messages",
            color_continuous_scale="Viridis",
        )

        st.plotly_chart(fig, width="stretch")

        st.info("This chart highlights the communication 'golden hours'.")

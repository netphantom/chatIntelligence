import pandas as pd
import streamlit as st
from plotly import express as px

from view.charts.ChartStrategy import ChartStrategy


class ResponseTimeStrategy(ChartStrategy):
    @property
    def title(self) -> str:
        return "Average Response Time Over Time"

    def render(self, df: pd.DataFrame) -> None:
        df_sorted = df.sort_index()
        df_sorted["prev_sender"] = df_sorted["sender"].shift(1)
        # Calculate time diff in minutes
        df_sorted["time_diff_min"] = (
            df_sorted.index.to_series().diff().dt.total_seconds() / 60.0
        )

        # Keep only rows where sender changed (a response happened)
        responses = df_sorted[df_sorted["sender"] != df_sorted["prev_sender"]].dropna(
            subset=["prev_sender"]
        )

        # Remove massive outliers (e.g., someone responding after 3 months doesn't reflect standard response time)
        responses = responses[responses["time_diff_min"] < 60 * 24]  # Cap at 24 hours

        weekly_response = (
            responses.groupby("sender")
            .resample("W")["time_diff_min"]
            .mean()
            .reset_index()
        )
        fig = px.line(
            weekly_response,
            x="date",
            y="time_diff_min",
            color="sender",
            labels={"time_diff_min": "Avg Response Time (Minutes)", "date": "Week"},
        )
        st.plotly_chart(fig, width="stretch")

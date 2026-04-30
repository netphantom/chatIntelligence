import pandas as pd
import streamlit as st
from plotly import express as px

from view.charts.ChartStrategy import ChartStrategy


class FilterableTimelineStrategy(ChartStrategy):
    @property
    def title(self) -> str:
        return "Daily Messages Timeline (Filterable)"

    def render(self, df: pd.DataFrame) -> None:
        years = df.index.year.unique().tolist()
        selected_year = st.selectbox(
            "Select Year", [None] + years, index=0, key="timeline_year"
        )

        filtered_df = df.copy()
        if selected_year:
            filtered_df = filtered_df[filtered_df.index.year == selected_year]
            months = filtered_df.index.month.unique().tolist()
            selected_month = st.selectbox(
                "Select Month", [None] + months, index=0, key="timeline_month"
            )
            if selected_month:
                filtered_df = filtered_df[filtered_df.index.month == selected_month]

        daily_df = (
            filtered_df.groupby("sender").resample("D").size().reset_index(name="count")
        )
        fig = px.line(daily_df, x="date", y="count", color="sender")
        st.plotly_chart(fig, width="stretch")

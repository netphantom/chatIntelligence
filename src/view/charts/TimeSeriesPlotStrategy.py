import pandas as pd
import streamlit as st
from plotly import express as px

from view.charts.ChartStrategy import ChartStrategy


class TimeSeriesPlotStrategy(ChartStrategy):
    def __init__(self, freq: str, title: str):
        self.freq = freq
        self._title = title

    @property
    def title(self) -> str:
        return self._title

    def render(self, df: pd.DataFrame) -> None:
        resampled = (
            df.groupby("sender").resample(self.freq).size().reset_index(name="count")
        )
        fig = px.line(
            resampled,
            x="date",
            y="count",
            color="sender",
            title=self.title,
            markers=True,
        )
        st.plotly_chart(fig, width="stretch")

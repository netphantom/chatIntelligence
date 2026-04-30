import pandas as pd
import streamlit as st
from plotly import express as px

from view.charts.ChartStrategy import ChartStrategy


class MovingAverageStrategy(ChartStrategy):
    @property
    def title(self) -> str:
        return "Moving Average of Daily Messages"

    def render(self, df: pd.DataFrame) -> None:
        window = st.slider("Select Window (Days)", min_value=3, max_value=60, value=14)
        daily_df = (
            df.groupby(["date", "sender"])
            .size()
            .unstack(fill_value=0)
            .resample("D")
            .sum()
        )
        ma_df = daily_df.rolling(window=window).mean().reset_index()

        # Melt for plotly
        ma_df_melted = ma_df.melt(
            id_vars=["date"], var_name="sender", value_name="Moving Average"
        )
        fig = px.line(ma_df_melted, x="date", y="Moving Average", color="sender")
        st.plotly_chart(fig, width="stretch")

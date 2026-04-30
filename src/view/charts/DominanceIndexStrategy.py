import pandas as pd
import streamlit as st
from plotly import express as px

from view.charts.ChartStrategy import ChartStrategy


class DominanceIndexStrategy(ChartStrategy):
    @property
    def title(self) -> str:
        return "Dominance Index (Message Volume Ratio)"

    def render(self, df: pd.DataFrame) -> None:
        daily_df = (
            df.groupby(["date", "sender"])
            .size()
            .unstack(fill_value=0)
            .resample("D")
            .sum()
        )
        window = st.slider(
            "Dominance Calculation Window (Days)",
            min_value=7,
            max_value=90,
            value=30,
            key="dom_window",
        )

        rolling_sum = daily_df.rolling(window=window).sum()
        total_rolling = rolling_sum.sum(axis=1)

        # Calculate percentage of messages per user
        dominance_df = rolling_sum.div(total_rolling, axis=0) * 100
        dominance_df = dominance_df.reset_index().melt(
            id_vars=["date"], var_name="sender", value_name="Dominance (%)"
        )

        fig = px.area(
            dominance_df,
            x="date",
            y="Dominance (%)",
            color="sender",
            groupnorm="percent",
        )
        st.plotly_chart(fig, width="stretch")

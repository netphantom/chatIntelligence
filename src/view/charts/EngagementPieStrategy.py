import pandas as pd
import streamlit as st
from plotly import express as px

from view.charts.ChartStrategy import ChartStrategy


class EngagementPieStrategy(ChartStrategy):
    @property
    def title(self) -> str:
        return "Overall Engagement (Message Volume & Characters)"

    def render(self, df: pd.DataFrame) -> None:
        metrics = (
            df.groupby("sender")
            .agg(msg_count=("sender", "count"), char_count=("text_length", "sum"))
            .reset_index()
        )

        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(
                metrics, values="msg_count", names="sender", title="Total Messages"
            )
            st.plotly_chart(fig1, width="stretch")
        with col2:
            fig2 = px.pie(
                metrics,
                values="char_count",
                names="sender",
                title="Total Characters Written",
            )
            st.plotly_chart(fig2, width="stretch")

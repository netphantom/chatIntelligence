import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from view.charts.ChartStrategy import ChartStrategy


class PeakAnomalyStrategy(ChartStrategy):
    @property
    def title(self) -> str:
        return "Peak and Anomaly Detection (Extraordinary Events)"

    def render(self, df: pd.DataFrame) -> None:
        # Daily aggregation
        daily_counts = df.resample("D").size().reset_index(name="msg_count")

        # Z-Score calculation to identify peaks
        # Formula: $Z = \frac{x - \mu}{\sigma}$
        mean_val = daily_counts["msg_count"].mean()
        std_val = daily_counts["msg_count"].std()

        daily_counts["z_score"] = (daily_counts["msg_count"] - mean_val) / std_val

        # Anomaly threshold (e.g., 2 standard deviations)
        threshold = st.number_input(
            "Anomaly sensitivity threshold (Z-Score)", value=2.0, step=0.5
        )
        peaks = daily_counts[daily_counts["z_score"] > threshold]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=daily_counts["date"],
                y=daily_counts["msg_count"],
                mode="lines",
                name="Daily Volume",
                line=dict(color="lightgrey"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=peaks["date"],
                y=peaks["msg_count"],
                mode="markers",
                name="Detected Peaks",
                marker=dict(color="red", size=10, symbol="star"),
            )
        )

        fig.update_layout(
            title=f"Peak Analysis (Above {threshold} standard deviations)"
        )
        st.plotly_chart(fig, width="stretch")

        if not peaks.empty:
            st.write("Days with anomalous activity:")
            st.dataframe(
                peaks[["date", "msg_count"]].sort_values(
                    by="msg_count", ascending=False
                )
            )

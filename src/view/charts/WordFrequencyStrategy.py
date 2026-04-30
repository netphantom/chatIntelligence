import pandas as pd
import streamlit as st
from plotly import express as px

from view.charts.ChartStrategy import ChartStrategy


class WordFrequencyStrategy(ChartStrategy):
    @property
    def title(self) -> str:
        return "Term Frequency Analysis"

    def render(self, df: pd.DataFrame) -> None:
        search_term = st.text_input("Enter word or phrase to search", key="word_search")

        if search_term:
            # Filter messages containing the term (case insensitive)
            mask = df["text"].str.contains(search_term, case=False, na=False)
            filtered_df = df[mask]

            if not filtered_df.empty:
                # Daily aggregation by sender
                resampled = (
                    filtered_df.groupby("sender")
                    .resample("D")
                    .size()
                    .reset_index(name="occurrences")
                )

                fig = px.line(
                    resampled,
                    x="date",
                    y="occurrences",
                    color="sender",
                    title=f"Frequency of: '{search_term}' over time",
                    markers=True,
                )

                st.plotly_chart(fig, width="stretch")
                st.info(f"Found {len(filtered_df)} occurrences.")
            else:
                st.warning("No matches found.")

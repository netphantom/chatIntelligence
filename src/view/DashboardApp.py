from typing import Dict, List

import streamlit as st

from controller.TelegramParser import TelegramParser
from view.charts.ChartStrategy import ChartStrategy


class DashboardApp:
    def __init__(self, strategy_groups: Dict[str, List[ChartStrategy]]):
        self.strategy_groups = strategy_groups

    # ======================
    # CONFIG
    # ======================
    def _configure(self):
        st.set_page_config(
            page_title="Chat Intelligence",
            page_icon="💬",
            layout="wide",
        )

    # ======================
    # THEME
    # ======================
    def _theme(self):
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #0B0F19;
                color: #E5E7EB;
            }

            .title {
                font-size: 2.3rem;
                font-weight: 800;
                margin-bottom: 0.2rem;
            }

            .subtitle {
                color: #9CA3AF;
                margin-bottom: 1.5rem;
            }

            .section {
                font-size: 1.2rem;
                font-weight: 700;
                margin-top: 2rem;
                margin-bottom: 1rem;
                color: #F3F4F6;
            }

            .card {
                border: 1px solid #1F2937;
                border-radius: 12px;
                padding: 1rem;
                background: #111827;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # ======================
    # STATE HELPERS
    # ======================
    def _go_home(self):
        st.session_state.clear()
        st.session_state["page"] = "home"
        st.rerun()

    def _go_analysis(self):
        st.session_state["page"] = "analysis"
        st.rerun()

    # ======================
    # DATA
    # ======================
    def _load_data(self, uploaded_file):
        if "df" in st.session_state:
            return st.session_state["df"]

        df = TelegramParser.parse(uploaded_file.getvalue())

        if df.empty:
            raise ValueError("Empty dataset")

        st.session_state["df"] = df
        return df

    # ======================
    # LANDING PAGE
    # ======================
    def _landing(self):
        st.markdown(
            '<div class="title">Chat Intelligence</div>', unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">'
            "Turn any chat into structured insights."
            "Discover patterns, timing, behavior and anomalies."
            "</div>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Patterns", "Behavioral")

        with col2:
            st.metric("Timing", "Temporal")

        with col3:
            st.metric("Insights", "Automatic")

        st.markdown("---")

        st.markdown(
            """
            ### What you can discover
            - Interaction dynamics between participants  
            - Response speed and communication rhythm  
            - Hidden periodic patterns  
            - Anomalies and bursts of activity  
            - Language and content distribution  
            """,
        )

        st.markdown("---")

        uploaded_file = st.file_uploader(
            "Drop your chat export (JSON)",
            type=["json"],
        )

        if uploaded_file:
            st.session_state["file"] = uploaded_file
            st.session_state["page"] = "analysis"
            self._go_analysis()

    # ======================
    # ANALYSIS PAGE
    # ======================
    def _analysis(self):
        st.markdown('<div class="title">Analysis</div>', unsafe_allow_html=True)

        if st.button("← Back to Home"):
            self._go_home()
            return

        uploaded_file = st.session_state.get("file")

        if uploaded_file is None:
            st.warning("No dataset found")
            self._go_home()
            return

        # spinner SOLO sul compute reale
        with st.spinner("Analyzing conversation..."):
            df = self._load_data(uploaded_file)

        st.success(f"Loaded {len(df)} messages")

        # ======================
        # STRATEGY GROUPS
        # ======================
        for section, strategies in self.strategy_groups.items():
            st.markdown(f'<div class="section">{section}</div>', unsafe_allow_html=True)

            cols = st.columns(2)

            for i, strategy in enumerate(strategies):
                with cols[i % 2]:
                    with st.container(border=True):
                        strategy.render(df)

            st.divider()

    # ======================
    # RUN
    # ======================
    def run(self):
        self._configure()
        self._theme()

        if "page" not in st.session_state:
            st.session_state["page"] = "home"

        if st.session_state["page"] == "home":
            self._landing()
        else:
            self._analysis()

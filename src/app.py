import logging
import warnings

from view.charts.DominanceIndexStrategy import DominanceIndexStrategy
from view.charts.EngagementPieStrategy import EngagementPieStrategy
from view.charts.FilterableTimelineStrategy import FilterableTimelineStrategy
from view.charts.MovingAverageStrategy import MovingAverageStrategy
from view.charts.PeakAnomalyStrategy import PeakAnomalyStrategy
from view.charts.PeriodicityHeatmapStrategy import PeriodicityHeatmapStrategy
from view.charts.ResponseTimeStrategy import ResponseTimeStrategy
from view.charts.TimeSeriesPlotStrategy import TimeSeriesPlotStrategy
from view.charts.WordFrequencyStrategy import WordFrequencyStrategy
from view.DashboardApp import DashboardApp

logging.getLogger("transformers").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

def build_strategies():
    return {
        "Temporal Patterns": [
            TimeSeriesPlotStrategy(freq="W", title="Weekly Message Exchange"),
            TimeSeriesPlotStrategy(freq="ME", title="Monthly Message Exchange"),
            MovingAverageStrategy(),
            PeriodicityHeatmapStrategy(),
        ],
        "Behavioral Analysis": [
            ResponseTimeStrategy(),
            DominanceIndexStrategy(),
            EngagementPieStrategy(),
        ],
        "Content Analysis": [
            WordFrequencyStrategy(),
            FilterableTimelineStrategy(),
        ],
        "Anomalies": [
            PeakAnomalyStrategy(),
        ],
    }


if __name__ == "__main__":
    strategy_groups = build_strategies()

    app = DashboardApp(strategy_groups=strategy_groups)
    app.run()
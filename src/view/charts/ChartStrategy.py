from abc import ABC, abstractmethod

import pandas as pd


class ChartStrategy(ABC):
    """Abstract base class for all analysis modules (Open-Closed Principle)."""

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @abstractmethod
    def render(self, df: pd.DataFrame) -> None:
        """Processes data and renders the Streamlit component."""
        pass

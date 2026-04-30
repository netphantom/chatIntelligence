FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
LABEL authors="net_phantom"

WORKDIR /home

COPY ../src .
COPY ../pyproject.toml .

RUN uv sync --project pyproject.toml

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.address=0.0.0.0"]
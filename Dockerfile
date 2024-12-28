# ============== dev stage (開発用) ==============
FROM python:3.13.1-slim-bookworm AS dev

# Pythonの出力表示をDocker用に調整
ENV PYTHONUNBUFFERD=1

# Poetryインストールに必要なツールをインストール
RUN apt-get update \
    && apt-get install -y curl build-essential --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Poetryをインストール (バージョンは適宜指定)
ENV POETRY_VERSION=1.8.5
RUN curl -sSL https://install.python-poetry.org | python -
# PoetryをPATHに追加
ENV PATH="/root/.local/bin:$PATH"

# Poetryの仮想環境をコンテナ内に作らず、グローバルインストール的に使う設定例
RUN poetry config virtualenvs.create false

# 作業ディレクトリ
WORKDIR /workspace

# pyproject.toml / poetry.lock をコピーして依存を解決 (dev環境は開発用依存も含む)
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# ソースコードをコピー
COPY . .

# CMD は docker-compose.ymlで指定 (uvicorn --reload など)


# ============== prd stage (本番用) ==============
FROM python:3.13.1-slim-bookworm  AS prd

# 必要なツール
RUN apt-get update && apt-get install -y curl build-essential --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Poetryインストール
ENV POETRY_VERSION=1.8.5
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false

WORKDIR /workspace

# pyproject.toml / poetry.lock をコピーして"本番用"にインストール
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main  # dev依存関係を除外

# devステージでコピー済みのソースコードをまとめて取得
COPY --from=dev /workspace /workspace

# 本番用FastAPIの起動コマンド (Cloud Runなどでポートを8080に)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]



# FROM python:3.13.1-bookworm

# ENV PYTHONUNBUFFERD=1

# WORKDIR /src

# RUN pip install poetry

# COPY pyproject.toml* poetry.lock* ./

# RUN poetry config virtualenvs.in-project true
# RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload", "--app-dir", "./src"]
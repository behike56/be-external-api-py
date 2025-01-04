# ==========================================================
# ============== dev stage (Dev Container) =================
# ==========================================================
FROM python:3.13.1-slim-bookworm AS dev

# Pythonの出力をバッファしない(Dev用)
ENV PYTHONUNBUFFERED=1

# ========== 追加する要素 ==========
# ユーザー/グループ作成 + sudo設定 + ロケール設定
ARG USERNAME=behike56
ARG USER_UID=1056
ARG USER_GID=$USER_UID

RUN apt-get update \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get install -y sudo \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get -y install locales \
    && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 \
    && apt-get -y install curl git less gcc build-essential --no-install-recommends \
    && apt-get -y install libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 環境変数 (日本語ロケールなど)
ENV LANG=ja_JP.UTF-8
ENV LANGUAGE=ja_JP:ja
ENV LC_ALL=ja_JP.UTF-8
ENV TZ=JST-9
ENV TERM=xterm

# pipとPoetryをインストール (VSCodeフォーマッタ/リンタ用など)
RUN pip install --upgrade pip setuptools pipx \
    && pip install poetry

# ========== 以下: 従来のPoetryインストール内容と合流 ==========
# (すでにPoetryをインストール済みだがバージョン固定などあれば上書き可能)
ENV POETRY_VERSION=1.8.5
# もしバージョンの固定インストールをしたい場合は、上で "pip install poetry==$POETRY_VERSION" 等も検討

# Poetryの仮想環境をコンテナ全体で使う設定 (必要に応じて変更)
RUN poetry config virtualenvs.create false

# 作業ディレクトリ
WORKDIR /workspace

# pyproject.toml / poetry.lock を先にコピーして依存を解決 (開発用依存も含む)
COPY pyproject.toml* poetry.lock* ./
RUN poetry install --no-root

# RUN poetry config virtualenvs.in-project true \
#     && if [ -f pyproject.toml ]; then poetry install --no-root; fi
# RUN if [ -f pyproject.toml ]; then poetry install --no-interaction --no-ansi; fi

# ENV PATH="/workspace/.venv/bin:$PATH"

# ソースコードをコピー
COPY . .

# CMDはcompose.yaml側で指定 (例: uvicorn --reload)


# ==========================================================
# ============== prd stage (Cloud Run) =====================
# ==========================================================
FROM python:3.13.1-slim-bookworm AS prd

# 必要なツール
RUN apt-get update \
    && apt-get install -y curl build-essential --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Poetryインストール
ENV POETRY_VERSION=1.8.5
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false

# 作業ディレクトリ
WORKDIR /workspace

# pyproject.toml / poetry.lock をコピーして "本番用" にインストール
COPY pyproject.toml poetry.lock ./
# dev依存関係を除外
RUN poetry install --no-root --only main

# devステージでインストール/コピー済みのソースをまとめて取得
COPY --from=dev /workspace /workspace

# 本番FastAPIの起動コマンド (例: Cloud Runで8080ポート)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

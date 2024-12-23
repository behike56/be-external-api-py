# DevContinerによる開発

## Dockerfileの解説

`.devcontainer/Dockerfile`

``` dockerfile
RUN apt-get update \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get -y install locales \
    && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
```

### 全体像

- この部分では、コンテナ内に「特定のユーザー」を追加し、そのユーザーが `sudo` をパスワード無しで実行できるように設定し、最後に日本語ロケールをインストール・生成しています。
- `&&` でつないでいるのは、途中で何らかのエラーが発生した場合に、その時点でビルドが止まるようにするためです。  

### 各行の処理内容

1. **`apt-get update`**  
   - パッケージリポジトリのインデックス情報を更新します。  
   - 直後に行うパッケージインストールに備え、最新情報を取得するために実行します。

2. **`groupadd --gid $USER_GID $USERNAME`**  
   - `$USER_GID` という GID（グループID）を持つ新しいグループ `$USERNAME` を作成します。  
   - あらかじめ外部で `$USER_GID` という環境変数が設定されている想定です。

3. **`useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME`**  
   - `$USER_UID` という UID（ユーザーID）を持つ新しいユーザー `$USERNAME` を作成します。  
   - `-s /bin/bash` でログインシェルを Bash に設定しています。  
   - `-m` オプションによってユーザーディレクトリ（ホームディレクトリ）を自動的に作成します。

4. **`apt-get install -y sudo`**  
   - `sudo` パッケージをインストールします。  
   - `-y` はインストール途中での確認を自動的に「Yes」とするオプションです。

5. **`echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME`**  
   - `/etc/sudoers.d/` に `$USERNAME` 用の設定ファイルを作成し、そのユーザーが `sudo` コマンドを **パスワードなし** で実行できるようにします。  
   - `ALL=(root) NOPASSWD:ALL` は、root 権限で任意のコマンドをパスワード入力なしで実行できる設定です。

6. **`chmod 0440 /etc/sudoers.d/$USERNAME`**  
   - 先ほど作成したファイルのパーミッションを `0440` に変更し、  
     - 所有者は読み取り可、その他は読み取り不可  
     - 書き込み権限を付与しない  
   - これにより、`sudo` 権限設定ファイルとして正しくセキュアに保護する目的があります。

7. **`apt-get -y install locales`**  
   - ロケール関連のパッケージをインストールします。  
   - 国際化・多言語対応（言語や文字コード、日付フォーマットなど）に必要なファイルを含んでいます。

8. **`localedef -f UTF-8 -i ja_JP ja_JP.UTF-8`**  
   - 日本語 (ja_JP) のロケールを UTF-8 向けに生成します。  
   - これによって、コンテナ内で日本語の文字コード・日付や時間表記などを扱えるようになります。

---

### まとめ

- **ユーザーとグループを作成**し、**パスワードなしの `sudo` 設定**を行う。  
- **日本語 (UTF-8) ロケールを生成**して、コンテナ内で日本語環境を使えるようにする。

このようにすることで、コンテナ内で開発や運用を行う際に、特定ユーザーとして安全に作業できるだけでなく、日本語対応が必要な場面（ログ、標準出力など）にも対応しやすくなります。
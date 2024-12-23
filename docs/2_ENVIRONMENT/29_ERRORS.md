# ERRORS

## 1

``` shell
docker compose build
[+] Building 0.0s (1/1) FINISHED                                           docker:desktop-linux
 => ERROR [demo-app internal] load build definition from Dockerfile                        0.0s
 => => transferring dockerfile: 138B                                                       0.0s
------
 > [demo-app internal] load build definition from Dockerfile:
------
failed to solve: failed to read dockerfile: error from sender: failed to xattr /Volumes/CODE/00_Development/000-proj/be-external-api-py/._be-external-api-py.code-workspace: operation not permitted
```

MacOSが自動的に作成している「._」ファイルがイメージ内に入っていることが原因と思われる。
.gitignoreに含める、または、物理的に削除してからコンテナをビルドすること。

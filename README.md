# NAOYA WEB

ずっと、あれも、これも。

宮崎直哉の11プロジェクトを紹介するレスポンシブなポートフォリオ。吉田ファームは紹介対象外です。

公開先: https://djnaoyaman.github.io/

main / root から既存のGitHub Pages設定で公開。ビルドや依存ライブラリは不要です。

## 収録

- 11サイトの静的紹介、GitHubソースリンク
- 最新版の本人提供のプロフィール文章
- OGP / X summary_large_image、1200 × 630 PNG
- SVG / ICO / PNG favicon、180px Apple Touch Icon、192 / 512pxアイコン
- canonical、robots、sitemap、構造化データ、llms.txt / llms-full.txt
- Xシェア、対応端末の共有機能、HTTPS環境のリンクコピー
- キーボード操作、読み上げラベル、動きを抑える設定、JavaScriptなしの全作品表示

## SEM・運用

UTM付きURLの例:
https://djnaoyaman.github.io/?utm_source=google&utm_medium=cpc&utm_campaign=naoya_web

canonicalと共有URLはパラメータなしの正規URLに統一しています。計測IDは未提供のため、アクセス解析・広告タグ・コンバージョン計測は未接続です。広告配信・課金・Search Console登録は実施していません。導入時は実アカウントのID、目的、コンバージョン、同意要件を決めてください。

llms.txtは補助資料です。検索順位、AIでの引用、SNSプレビューの更新時期は保証しません。SNSのキャッシュは再取得が必要な場合があります。Service Workerとオフライン対応は含みません。

## 更新

index.htmlの作品カード、件数、JSON-LD ItemList、llms.txt / llms-full.txtを同時に更新。OG画像とアイコンは白地と黒文字のデザイン・名称に合わせて更新します。robots.txtの既存制限と他サイトのサイトマップ案内を維持してください。


## 2026-10-26 の改善

静かな白地のデザインと本人の文章を維持し、並列する「か」の誤字2か所を修正。

- 4分野の絞り込み。選択は `?theme=music` などで復元し、ブラウザの戻る・進むに対応。既存のUTMやアンカーも保持。共有するURLは正規のトップページ。
- 件数バッジは実カードから算出。元の通し番号を保ち、表示件数を読み上げる。JavaScriptなしでは操作部を隠し全作品を表示。
- 主要操作の44pxタップ領域、320pxからのレイアウト、本文スキップ、現在セクション表示、コントラスト、セーフエリア、強制配色、動きを抑える設定。
- 印刷では絞り込みを解除して全11作品とURLを掲載。操作部を隠し、作品単位の改ページを抑制。
- コピー失敗時のURL案内、連打防止、同じ通知の再読み上げ、共有キャンセル時の古い通知消去。
- 深いパスでも相対参照が壊れない404ページ。自動転送せずホーム・作品一覧に復帰。検索登録を抑止。GitHub Pagesのホスト共通404としても機能する。
- CSS・JavaScriptを外部ファイルに分離。ページ単位のCSPでインライン実行や外部接続を制限し、referrer方針も明示。別プロジェクトのページには適用されない。
- ビルド・外部ライブラリ・外部フォント・トラッキングの追加なし。

## 検証

`python3 tests/check-content.py` と `node --check site.js` は依存なし。GitHub Actionsでも実行。

`python tests/test-site.py` はPython Playwrightと `/usr/bin/chromium` を使用。ネットワークをモックして絞り込み・履歴・6画面幅・キーボード・印刷・共有の失敗/キャンセル・JavaScript無効・404を検証。任意の `AXE_PATH` にaxe-coreのローカルファイルを渡すとWCAG A/AAとbest-practiceも自動検査。検査エンジンを注入する専用コンテキストのみCSPを無効化し、通常の機能テストではCSPを有効にする。自動検査だけで完全なアクセシビリティ適合を保証するものではない。

作品の追加時は `index.html` のカード・構造化データ・初期件数・分野ボタン、`llms.txt` / `llms-full.txt` とチェックの期待件数を更新する。

# NAOYA WEB

ずっと、あれも、これも。

宮崎直哉の12プロジェクトを紹介するレスポンシブなポートフォリオ。吉田ファームは紹介対象外です。

公開先: https://djnaoyaman.github.io/

main / root から既存のGitHub Pages設定で公開。ビルドや依存ライブラリは不要です。

## 収録

- 12サイトの静的紹介、GitHubソースリンク
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
- 印刷では絞り込みを解除して全12作品とURLを掲載。操作部を隠し、作品単位の改ページを抑制。
- コピー失敗時のURL案内、連打防止、同じ通知の再読み上げ、共有キャンセル時の古い通知消去。
- 深いパスでも相対参照が壊れない404ページ。自動転送せずホーム・作品一覧に復帰。検索登録を抑止。GitHub Pagesのホスト共通404としても機能する。
- CSS・JavaScriptを外部ファイルに分離。ページ単位のCSPでインライン実行や外部接続を制限し、referrer方針も明示。別プロジェクトのページには適用されない。
- ビルド・外部ライブラリ・外部フォント・トラッキングの追加なし。

## 検証

`python3 tests/check-content.py` と `node --check site.js` は依存なし。GitHub Actionsでも実行。

`python tests/test-site.py` はPython Playwrightと `/usr/bin/chromium` を使用。ネットワークをモックして絞り込み・履歴・6画面幅・キーボード・印刷・共有の失敗/キャンセル・JavaScript無効・404を検証。任意の `AXE_PATH` にaxe-coreのローカルファイルを渡すとWCAG A/AAとbest-practiceも自動検査。検査エンジンを注入する専用コンテキストのみCSPを無効化し、通常の機能テストではCSPを有効にする。自動検査だけで完全なアクセシビリティ適合を保証するものではない。

作品の追加時は `index.html` のカード・構造化データ・初期件数・分野ボタン、`llms.txt` / `llms-full.txt` とチェックの期待件数を更新する。

## 2026-10-26 ブランド・端末対応と細部の再点検

- ヘッダーのArial系太字と同じ「N」にアイコンを統一。文字の外接矩形を基準に中央配置し、装飾的な点は入れない。180px Apple Touch Icon、192/512px通常アイコン、192/512px Android maskableアイコン、16/32/48px PNG、16/32/48/64pxを格納したICO、明暗に追従するSVG favicon、単色のSafari固定タブ用SVGを用意。
- Apple Touch Iconは不透明な白地。Androidの図柄は中央80%の安全円に収め、丸型・角丸型で欠けないことを画素から検査。アイコンと共有画像の版番号を参照URLに付け、既存キャッシュとの混在を防ぐ。
- 共有画像は日本語フォントを指定した1200×630px。ブランド、キャッチコピー、分野、URLを同じ意匠で描画。素材のソースは `assets-source/`、再生成は `python tools/render-assets.py`。Noto Sans CJK JP・Playwright・Pillowが必要。
- ホーム画面名を `NAOYA WEB.` に明示。manifestに説明・実際のモバイル/PC画面・3つのショートカットを追加。ブラウザの操作が使える `minimal-ui` を優先し、対応しない環境では `browser` に戻る。単なるポートフォリオをブラウザ操作のない画面に閉じ込めない。
- 404にもアイコン・ホーム画面名・manifest設定を統一。`viewport-fit=cover` と既存セーフエリア指定を接続。明るいページ背景を初回表示前から明示。
- 文字間隔・行間の拡大に備えヘッダーを折り返す。キーボードで作品にフォーカスしたときにも見出しの下線を表示。
- 履歴から復帰したときの共有ボタン状態を復旧。ページ復帰前の非同期結果が新しい共有操作を上書きしないよう、通知とボタン状態をそれぞれ管理。
- ページ本体・CSS・JSの合計は非圧縮で40KB未満。OGPやインストール用スクリーンショットは通常表示では読み込まない。

`python tools/capture-screenshots.py` でmanifest用の実画面を明示的に更新する。通常テストは公開用画像を書き換えない。

`python tests/test-details.py` で画素の中央配置/安全円、CSPによる実行阻止、404応答、共有の非同期競合、文字間隔拡大、追加の画面寸法、強制配色、明暗faviconを検査。アイコンの切り抜きプレビューは `/tmp/naoya-icon-masks.png` に出力。GitHub Actionsは構造検査に加えPlaywrightとaxe-coreによるブラウザ検査も実行する。ブラウザ実行パスは `CHROMIUM_PATH` で指定でき、未指定時はシステムChromiumまたはPlaywrightのChromiumを利用する。

端末ごとの表示はブラウザで検証した。iPhone/Androidの実機やSNSサービス側の画像キャッシュ更新までは自動検証の対象外。

タブ用faviconはNの高さを48/64、ホーム画面用は36/64として光学補正し、16pxでもNの高さを12px確保する。`assets-source/tab-mark.svg` がその描画元。

2026-10-26 アイコンの意匠を修正。独自の幾何学的なNと赤い点を廃し、ヘッダーと同じArial系太字のNを使用。ページのブランド末尾のピリオドは黒に統一し、共有画像の重複するNマークも削除。原型は `tools/build-mark.py` でLiberation Sans BoldのNをアウトライン化し、文字自体の中心を合わせている。

Premium Cuts Listedを音楽分野に追加。全12サイト・音楽4サイトとし、表示順・構造化データ・概要文・印刷用件数・検証の期待値を同期。紹介先は https://djnaoyaman.github.io/premiumcuts/ 。


## 2026-10-26 執筆活動・プロフィールの追加

note（宮崎直哉）のエッセイ4分野、紫波金魚の公開小説3作品の紹介、サウナイキタイ・Instagram・Facebookへの導線を追加。作品の12サイトとは別のセクションで紹介。noteの公開プロフィール・マガジン紹介を参照し、サウナとSNSは本人指定URLへのリンクを掲載。

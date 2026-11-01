# MIYAZAKINAOYA

ずーっと、あれも、これも。

宮崎直哉の15のWORLD（独立したWebサイト）をつなぐポートフォリオ。公開先は https://djnaoyaman.github.io/ 。MIXWELLは作者自身の実践として紹介します。吉田ファームは対象外です。

## 公開面と共通デザイン

- `/`：WORLDS / JOURNAL / ABOUT。15の点が線へつながり、作者の視点を表す軽量SVGアニメーション。
- `/profile.html`：制作姿勢を短く紹介。作品一覧はトップのWORLDSへ集約。旧プロフィールURLと各フラグメントは維持。
- `/404.html`：深い未知のURLにもルート相対参照で対応。noindex、復帰導線つき。
- `maisons.css` は互換性のためファイル名を維持した共通スタイル。名称はWORLDS。`profile.css`、`subpages.css`は配下の読み物レイアウト。
- `#worlds`が新しい入口。`#projects`と`#maisons`の既存リンクも維持。

アイボリー `#f7f6f2`、墨色 `#282823`、淡グレーを基調に統一。15サイト自身の画像・色・名前は変更しません。公式画像の出典とハッシュは `docs/maison-assets.json`。

## ブランド素材

`tools/build-mark.py` がフォントからの自動切り出しではない手設計MINAシンボルを生成。MIYAZAKIのMIとNAOYAのNAを2×2に構成し、通常版と小サイズ版で余白を光学調整しています。

`python tools/render-assets.py` でSVG、16/32/48 PNG、4サイズICO、180 Apple Touch Icon、192/512通常・maskable、Safari pinned、および1200×630のトップ/プロフィール/404共有画像を再生成。PillowとNoto Sans CJK・Liberation Serifを使用します。共有画像の原稿は `tools/render-share-card.py`、制作確認は `assets-source/share-card.html`（noindex）。

アイコンは不透明アイボリー、maskableは中央80%の安全円に収容。SVG faviconは明暗に追従。メタデータとmanifestの版番号は同時更新します。

## 動き・操作

`world-atlas.js` は外部依存なし。15の実サイトへのリンク、キーボードフォーカス、タッチ可能なテキスト一覧、再生ボタン、画面外/非表示時の一時停止、幅変更、履歴復帰に対応。動きを減らす設定とJavaScript無効時は完成図。派手な点滅や無限ループ、本文を隠すイントロはありません。

既存の4分野フィルターはURLの `?theme=` と履歴に対応。共有は正規URL、コピー失敗とキャンセルを処理。旧本文と執筆詳細は開閉欄で保持しています。

## 更新・検証

main/rootの既存GitHub Pages設定で公開。ブラウザの依存ライブラリやビルド工程は不要です。

- `python tests/check-content.py`、`python tests/test-profile.py`
- `node --check site.js`、`node --check world-atlas.js`
- CIの `tests/test-site.py` / `tests/test-details.py` / `tests/test-world-atlas.py` はPlaywright、Chromium、Pillow、axe-coreでアクセシビリティ、幅、履歴、印刷、CSP、共有、アイコン、動作を検査。
- `tools/capture-screenshots.py` は完成図（reduced-motion）の実ブラウザ画面を取得。CIの `identity-screenshots` artifactから最終画像を取り込みます。
- 項目追加時はカード、SVGカタログ、JSON-LD、llms資料、robotsのサイトマップ案内、件数と検査を同期。

## 保全と検証範囲

正規URL、プロフィール原稿・出典、各サイトURL、既存robots制限・sitemap方針、CSPを保持。計測IDがないためGA/広告タグは未導入のまま。新しいトラッキング、外部フォント通信、権限、Service Workerは追加しません。

SNS画像キャッシュ更新やiOS/Android実機のインストール表示は自動検査の対象外です。改修一覧と区別は `docs/identity-inventory.md` を参照。

## MINA brand symbol
The crown-shaped MINA symbol and its point-to-line construction story are documented in [docs/mina-identity.md](docs/mina-identity.md). The public process page is `/mina.html`; all shared site icons derive from the same approved geometry.

## Visible site update date

The footer's **サイト最終更新** is the actual published-source revision date in Japan Standard Time, not a visitor clock, weather observation, article fact-check or author-profile review date. It is visible without JavaScript. Content-specific dates remain separate.

For each site release, run `python3 scripts/site-update-date.py --date YYYY-MM-DD` using the actual release date in JST. Commit `site-update.json` and its listed HTML pages with the change; use `--check-content` before committing. CI also checks Git history and rejects a date differing from the latest published-source change. Tests/docs/CI-only edits and SUBURBIA's independently dated weather cache do not advance this date. This is an explicit release step, not an automatic runtime date. A release crossing midnight JST must refresh its date and checks before publication.

The read-only **Site update date** workflow verifies synchronization and captures visible footers at 390/1280px, including repeat loads and JavaScript-disabled checks, with external browser requests blocked. It adds no runtime request, tracking or deployment permission.

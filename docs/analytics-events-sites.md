# 個人サイト18件の追加イベント整理

2026-11-23（JST）。対象は djnaoyaman.github.io 配下の18サイト。各サイトの既存計測を確認し、実際に不足している操作へ追加・補正する。サイト側実装とGA4管理画面側の登録・受信確認は区別する。

## 追加・補正した10サイト

| サイト | 今回の内容 | 定義書 |
|---|---|---|
| MINA | 作品分類の変更、共有・URLコピーの成功。既存 creator_site_visit を維持 | [定義](analytics-events.md) |
| 1minutes | 展示の開始・完了、共有・URLコピーの成功。再開・取消・未完了を区別 | [定義](https://github.com/djnaoyaman/1minutes/blob/main/docs/analytics-events.md) |
| DESIGN LINEAGE | 記事選択、既定分類の変更、2項目の比較、URLコピー成功。Selected Worksの内容と配置は維持 | [定義](https://github.com/djnaoyaman/design-lineage/blob/main/docs/analytics-events.md) |
| my Chems | 実再生開始・終了、作品選択、共有成功 | [定義](https://github.com/djnaoyaman/chems/blob/main/docs/analytics-events.md) |
| Premium Cuts Listed | 既存共有UIの成功だけを share として計測 | [定義](https://github.com/djnaoyaman/premiumcuts/blob/main/docs/analytics-events.md) |
| CRATE DIGGIN’ | 既存 share に端末共有成功を追加。プレイリストの追加・削除は保存成功時に限定。イベント名は維持 | [定義](https://github.com/djnaoyaman/cratediggin/blob/main/docs/analytics-events.md) |
| IL MASTRO / bookkeeping | 構造化演習と60分模試の開始・完了。既存5問演習は維持 | [定義](https://github.com/djnaoyaman/bookkeeping/blob/main/docs/analytics-events.md) |
| Earth Number | 展示選択、既定分類の変更、展示内の初回操作 | [定義](https://github.com/djnaoyaman/earthnumber/blob/main/docs/analytics-events.md) |
| Before We Eat | 詳細ダイアログ表示、小説紹介の表示。既存の動物図解・連続閲覧判定を補正 | [定義](https://github.com/djnaoyaman/beforeweeat/blob/main/docs/analytics-events.md) |
| 妖怪図鑑 | カテゴリ選択を追加。既存の図鑑遷移に公開項目IDを補足 | [定義](https://github.com/djnaoyaman/youkai/blob/main/docs/analytics-events.md) |

## 既存の主要計測を維持した8サイト

| サイト | 既存で把握できる主な行動 |
|---|---|
| OMOCHI TOUCH | アート・写真・配色の選択、編集操作、PNG生成。書き出し生成とダウンロードクリックは別イベント。入力文字や作品内容は送らない |
| GOOOOOOOOOOD EXPRESSION | 詳細表示、デモ操作、コード・依頼文・色のコピー成功、コレクション、比較、共有、分類 |
| SUBURBIA CLASSICA | 実再生・終了、分類、コピー成功 |
| さかなむし | 開始、回答、時間切れ、完了 |
| ppp | パラメータなしの開始・完了・再開。健康情報の収集範囲は拡大しない |
| くらんぽ | 章別・総合・復習の開始、回答、完了 |
| 三冷交代浴 | 開始、回答、完了・途中終了、研究詳細 |
| 文鳥 | 図鑑・ゲーム・工房の専用イベント。既存GTM/GA4の構成を維持 |

## 共通方針

- 既存のGoogleタグと測定IDを使う。新しいタグ/config/page_viewや、拡張計測の外部リンク・スクロール・PDFダウンロードと同義のイベントを追加しない。
- 追加・補正した送信先は各サイトの測定IDに固定し、既存の停止設定を尊重する。
- 共有キャンセル、コピー失敗、保存失敗、未完了の操作を成功と数えない。端末共有APIの成功は、受信者への配送保証を意味しない。
- 自由入力、検索文字列、作品の内容、学習回答や得点、個人の測定値を追加パラメータへ含めない。
- Before We Eat の bwe_novel_view はGA4側の生成イベントとして扱い、クライアント側から重ねて送らない。既存 bwe_novel_read は維持する。

## 検証と管理画面の状態

実装前後は対象の発火条件、取消・失敗分岐、重複抑止、送信先を局所確認する。リポジトリの既存必須CIは維持する。公開後は代表ファイルの反映確認に限定し、全ページ巡回や大量のテストイベント送信を追加しない。

この作業では、GA4の対象管理画面でアクセス権のエラーが表示されたため、カスタムディメンションの登録、キーイベント指定、実データ受信の確認は行えていない。サイト側の追加・公開を、これら管理画面側の作業まで完了した意味では扱わない。各定義書の管理画面設定は、登録済みと明記していない限り候補・別工程である。

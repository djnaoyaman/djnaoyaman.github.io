# GA4 イベント定義

測定ID `G-PT03XG7KQR`。2026-11-23更新。

| イベント | 発火条件 | パラメータ |
|---|---|---|
| creator_site_visit | 同一ドメインの各プロジェクトへのリンク選択。既存イベントを維持 | target_site |
| select_filter | 利用者が作品分類を実際に変更。初回表示・戻る操作・同じ分類の再選択は除外 | filter_name=project_theme, filter_value |
| share | 共有APIの正常終了、またはリンクのクリップボード書き込み成功 | method=native/copy_link, content_type=website, item_id=mina |

共有の取消・失敗・手動コピー案内では成功イベントを送らない。native は端末の共有APIが正常終了したことを示し、相手の受領を保証しない。独自パラメータに自由入力・メール・共有文章・URLクエリは含めない。新規2イベントのURLは公開トップへ固定する。

Googleタグ・config・page_viewは追加しない。各イベントの送信先はこの測定IDに固定し、ga-disable の設定を尊重する。

サイト側実装とGA4管理画面の登録・受信確認は別工程。イベントは送信により収集される。分類別に見る場合のイベントスコープのカスタムディメンション候補は target_site、filter_name、filter_value。通常の分類選択はキーイベントにしない。

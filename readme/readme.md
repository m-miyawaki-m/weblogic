WebLogic の「設定」と言っても範囲がかなり広いので、まずは **全体像を整理しつつ、よく触る設定ポイント**を一通り解説します。
（バージョンや用途が分かれば、あとで個別チューニング案も出せます）

---

## 1. WebLogic の基本構造と設定の考え方

WebLogic はざっくりいうと：

* **ドメイン（Domain）**

  * WebLogic の「構成単位（プロジェクトの箱）」
  * 1つのドメインの中に、サーバやリソースをまとめて管理
* **管理サーバ（Admin Server）**

  * ドメインを管理する中枢。管理コンソール（ブラウザGUI）や WLST で操作
* **マネージドサーバ（Managed Server）**

  * 実際にアプリがデプロイされて動くサーバ
* **クラスタ（Cluster）**

  * 複数 Managed Server のグループ（負荷分散・冗長化用）

👉 WebLogic の設定は、基本的には
**「ドメイン単位で Admin Server から行う」**
と覚えておくと整理しやすいです。

---

## 2. 主な設定の入り口

### 2-1. 管理コンソール（ブラウザGUI）

* URL 例
  `http://<host>:7001/console` など
* ブラウザ上で：

  * サーバ設定（ポート、ログ、JVM 引数）
  * データソース（JDBC）
  * JMS、セキュリティ、クラスタ etc.
    をポチポチ設定するのが一番メジャーなやり方です。

### 2-2. 設定ファイル（config.xml など）

* ドメイン配下にある `config/config.xml` などに
  サーバやリソース設定が XML で保存されています。
* 管理コンソールで保存 → この XML が書き換わるイメージ。
* 直接編集もできますが、基本は **コンソール経由** が安全。

### 2-3. WLST（WebLogic Scripting Tool）

* Jython ベースの CLI ツール
* スクリプトで：

  * ドメイン作成
  * サーバ追加
  * データソース作成
  * デプロイ
    などを自動化できる
* 本番系や大量ドメインを扱う現場だと、
  **WLST + スクリプトで構成管理** がよくあります。

---

## 3. 代表的な設定項目ごとの解説

### 3-1. サーバ（Admin / Managed）の設定

管理コンソール → **Environment → Servers**

ここで主に設定するのは：

1. **General**

   * Listen Address（待ち受けアドレス）
   * Listen Port（ポート番号）
   * SSL ポートの有無・番号
2. **Server Start**

   * Java オプション（`-Xms`, `-Xmx`, `-XX` 系）
   * クラスパス、起動時の環境変数
3. **Logging**

   * サーバログの出力先・ローテーション条件
4. **Tuning**

   * スレッドプールの設定など（HTTP スレッドなど）

👉 パフォーマンス関連では：

* JVM オプション（ヒープサイズ・GC）
* スレッド数（ワークマネージャ含む）
* コネクションプール（JDBC）

あたりを調整していきます。

---

### 3-2. ドメイン全体の設定

管理コンソール → **Domain Structure → [domain名]**

* **General**

  * ドメイン名、セキュリティ設定の一部
* **Security**

  * セキュリティ・レルム（ユーザ・グループ・ロール）
  * 認証プロバイダ（LDAP 連携など）
* **JTA**

  * トランザクションタイムアウト、リカバリ関連

「アプリ全体に共通」なポリシー系はこの辺で設定します。

---

### 3-3. Data Source（JDBC）の設定

管理コンソール → **Services → Data Sources**

1. **新規作成ウィザード**

   * 名前
   * JNDI 名（アプリから `java:comp/env/jdbc/xxx` などで参照）
   * ドライバ種別（Oracle, MySQL …）
   * DB 接続情報（URL, ユーザ/パスワード）
   * ターゲット（どのサーバ/クラスタで使うか）

2. **詳細設定での主なポイント**

   * 最大/最小プールサイズ
   * 接続テストクエリ（`SELECT 1 FROM DUAL` など）
   * タイムアウト・再接続の設定

👉 現場で一番トラブルになるのは

* プールサイズ不足
* タイムアウト・切断復旧の設定不足
  なので、このへんは DB の特性と負荷を見ながらチューニングします。

---

### 3-4. JMS 設定（キュー、トピック）

管理コンソール → **Services → Messaging → JMS Modules**

* JMS サーバ
* JMS モジュール
* 接続ファクトリ（Connection Factory）
* キュー / トピック（Queue / Topic）

を組み合わせて設定します。

* 一般手順

  1. JMS サーバを作成し、ターゲットサーバに紐づける
  2. JMS モジュール内でキュー/トピックを作成
  3. JNDI 名を決めてアプリから参照

クラスタ構成の場合、**分散キュー／分散トピック**なども使います。

---

### 3-5. セキュリティ（ユーザ・ロール・ポリシー）

管理コンソール → **Security Realms → myrealm**

* Users and Groups

  * 管理コンソールログインユーザ
  * アプリ認証用ユーザ
* Roles and Policies

  * Web アプリや EJB に対するアクセス権限

さらに凝った構成では、LDAP サーバ（Active Directory 等）と連携して、
ユーザ管理を外部に任せることもあります。

---

### 3-6. デプロイメント（アプリの配置）

管理コンソール → **Deployments**

* war / ear / jar をデプロイ
* ターゲット（サーバ／クラスタ）を指定
* デプロイモード

  * stage / nostage / external_stage

**自動デプロイ**を使う方法もあり、
`domains/<domain>/autodeploy` にファイルを置くだけでデプロイされる方式もあります
（開発環境向け）。

---

### 3-7. クラスタ・高可用性関連

管理コンソール → **Environment → Clusters**

* Cluster 名、マルチキャスト/ユニキャスト設定
* ロードバランス方式（ラウンドロビン、負荷ベース etc.）

さらに、

* **Machines**

  * OS ホストを論理的に表したもの
* **Node Manager**

  * リモートのマシン上のサーバ起動/停止制御

を組み合わせて、複数ホスト・複数サーバ構成を組みます。

---

## 4. よくある「設定ファイル周り」の話

### 4-1. 環境変数・起動スクリプト

* `setDomainEnv.sh` / `.cmd`

  * クラスパスや JVM オプション、環境変数がまとまっている
* `startWebLogic.sh` / `.cmd`

  * Admin Server 起動用
* `startManagedWebLogic.sh` / `.cmd`

  * Managed Server 起動用

現場だと、**これらをラップした独自の起動スクリプト**を作って、
ログ出力ディレクトリや JVM パラメータを切り替えることが多いです。

### 4-2. weblogic.xml（Web アプリ固有の設定）

アプリ側の `WEB-INF/weblogic.xml` で

* コンテキストルート
* セッションタイムアウト
* ロードオーダー
* セキュリティロールマッピング

などを細かく制御できます。
Tomcat の `context.xml` + `web.xml` みたいなイメージです。

---

## 5. 性能・運用観点で押さえておきたい設定

ざっくり「チューニングでまず触る」ポイントを挙げておきます。

1. **JVM ヒープサイズ / GC**

   * `-Xms`, `-Xmx`, `-Xlog:gc*` など
2. **スレッドプール**

   * `Work Manager` の設定
   * HTTP スレッド数（サーバのチューニングタブ）
3. **JDBC プール**

   * 最大/最小コネクション数
   * タイムアウト・アイドル切断設定
4. **ログ**

   * ログローテーション（サイズ or 日時）
   * ログレベル
5. **セッション管理**

   * セッションタイムアウト
   * セッションレプリケーション（クラスタ構成時）

---

## 6. ここから先、どう深掘りするか

もしよければ、次のどれかを教えてもらえれば、
**設定例（スクショイメージや値の例付き）でかなり具体的に書けます。**

* 使っている WebLogic のバージョン（例：12c, 14c）
* OS（Windows / Linux）と構成（単体 / クラスタ）
* やりたいこと：

  * 例1：Oracle DB への DataSource 設定を一からやりたい
  * 例2：クラスタを組んでロードバランスしたい
  * 例3：ログと JVM のチューニングをしたい
  * 例4：WLST で自動構成したい

「◯◯の設定をステップバイステップで」と指定してくれれば、
コマンド・画面項目レベルで手順書風にまとめます 👍


まずは「WebLogic のデプロイ」と「Eclipse から動かしているときの裏側」、それから「WebLogic を単体で起動する方法」に分けて整理してみますね。

---

## 1. デプロイ方式の整理（stage / nostage / external_stage / autodeploy）

### 1-1. 通常のデプロイ（コンソールから）

**管理コンソール → Deployments → Install** で war / ear を選ぶときに
「deployment mode」を指定します。

ざっくりいうと：

#### ◆ stage モード

* **アプリのファイルを、各サーバごとの「ステージング領域」にコピーしてから動かす**方式
* 管理サーバ上に置いた war を、Managed Server ごとにコピーする
* 特徴

  * 各サーバが **ローカルにアプリを持つ**
  * サーバ間が別マシンでも OK
* 一般的には **本番向けで無難** なモード

#### ◆ nostage モード

* **コピーせず、指定したパスのアプリをそのまま参照**する方式
* 全サーバが **同じファイルシステム（共有ディスクなど）** にアクセスできる前提
* 特徴

  * アプリを 1 箇所に置けばよい
  * ただし、共有ストレージ前提なので構成をちゃんと組む必要あり
* 単体サーバ／開発環境でもよく使われます（共有じゃなくても、ローカルパスをそのまま参照するイメージ）

#### ◆ external_stage モード

* **ファイルコピーは管理者が手でやる前提** のモード
* WebLogic は「ここに置いてある前提で動かすよ」というだけで、自分ではコピーしない
* 使う場面はかなり限定的（独自の配布スクリプトを組んでいるような環境など）

---

### 1-2. autodeploy ディレクトリ

`domains/<domain>/autodeploy` に war / ear を置くと、WebLogic が **自動でデプロイ** してくれる仕組みです。

* 特徴

  * 監視間隔ごとに autodeploy フォルダをチェック
  * 新しく置かれたファイル → 自動デプロイ
  * 削除したら → 自動アンデプロイ
* 制約

  * **基本的に開発用**（ドキュメントにも「本番では使うな」と書かれていることが多い）
  * 単一サーバ想定（クラスタや複雑な設定には向かない）
* イメージとしては **「簡易ホットデプロイ用フォルダ」** です。

---

## 2. Eclipse から実行しているときの動き

Eclipse（＋ OEPE / WebLogic プラグイン）で
「Run on Server（WebLogic）」しているとき、裏でだいたいこんな動きになっています。

### 2-1. Eclipse がやっていること（ざっくり）

1. **WebLogic 用のドメインをどこかに作成**

   * 例）Eclipse の workspace 配下
     `workspace/.metadata/.plugins/.../wl_domain` みたいなところ
   * または、既存のドメインを参照する設定にしている場合もあります

2. **そのドメインの AdminServer を起動**

   * Eclipse から Java プロセスとして起動（`startWebLogic` 相当のコマンド＋引数）

3. **プロジェクトをビルドして、WebLogic にデプロイ**

   * war を作ることもあれば、「exploded（展開されたフォルダ）」形式でデプロイすることもある
   * WebLogic から見ると、
     「管理コンソール経由でデプロイされたアプリ」とほぼ同じ扱い
     （内部的には WebLogic の管理 API / WLST 相当でやっている）

4. **ソース変更時に自動で再デプロイ / ホットデプロイ**

   * 保存したらクラスだけ差し替え、などの動きを Eclipse がやってくれる

### 2-2. deployment mode はどうなっているの？

Eclipse から見るとあまり意識しませんが、概念的には：

* **Eclipse がビルド結果をドメイン内の特定フォルダに置いて、そこを参照させている**

  * つまり WebLogic 的には **nostage に近い** 挙動です
* カスタマイズすれば stage にもできますが、開発環境では

  * 「ビルドした結果をそのまま参照」
  * 「クラスファイルだけ入れ替え」
    がやりやすい nostage / exploded デプロイが多いです。

※ `autodeploy` フォルダを直接使っているわけではなく、
Eclipse プラグインが **WebLogic の管理APIを叩いてデプロイしている** と思っておくとイメージしやすいです。

---

## 3. WebLogic を「単体で」起動するには？

Eclipse なしで WebLogic だけを起動したい場合は、
**対象ドメインのディレクトリに降りて、付属のスクリプトを叩く** だけです。

### 3-1. 基本パターン（インストール済み WebLogic の場合）

1. **ドメインを作成済みであること**

   * `MW_HOME/wlserver/common/bin/config.sh` などで作ったドメイン
   * 例）`/u01/oracle/user_projects/domains/mydomain`

2. **AdminServer を起動**

**Linux / macOS:**

```bash
cd /u01/oracle/user_projects/domains/mydomain
./startWebLogic.sh
```

**Windows:**

```bat
cd C:\Oracle\user_projects\domains\mydomain
startWebLogic.cmd
```

3. **Managed Server を起動したい場合**

```bash
cd /u01/oracle/user_projects/domains/mydomain/bin
./startManagedWebLogic.sh MyManagedServer http://host:7001
```

* `MyManagedServer`：サーバ名（コンソールに出てくる名前）
* `http://host:7001`：AdminServer のアドレス

---

### 3-2. 「Eclipse が使っているドメイン」を単体起動したい場合

「今 Eclipse で動かしている WebLogic と同じ状態を、コマンドで起動したい」
というケースもありますよね。

その場合は：

1. **Eclipse で WebLogic サーバのプロパティを確認**

   * Servers ビュー → 対象 WebLogic サーバをダブルクリック
   * 「Domain directory」や「Domain home」などの項目にパスが書いてあります

2. そのパス（`DOMAIN_HOME`）に移動して `startWebLogic` 実行

```bash
cd <Eclipse で表示されていた DOMAIN_HOME>
./startWebLogic.sh    # Linux/mac
# or
startWebLogic.cmd     # Windows
```

* これで **Eclipse なしで AdminServer が起動** します
* そのドメインに Eclipse からデプロイしたアプリは、そのまま有効です

  * つまり、ブラウザで `http://host:port/アプリコンテキスト` にアクセスすれば普通に動きます

※ もし「Eclipse 用のドメイン」と「自分で作ったドメイン」が別なら、
　後者で起動してもアプリは入っていないので、改めてコンソールからデプロイが必要です。

---

## 4. まとめ＆次に深掘りできそうなところ

* **stage / nostage / external_stage**

  * ステージングするかどうか、誰がコピーするかの違い
  * 開発では nostage や autodeploy、本番では stage が無難
* **Eclipse 実行時**

  * Eclipse が裏でドメインを作成・起動
  * 管理 API 経由でアプリをデプロイ（概念的には nostage/exploded）
* **単体起動**

  * `DOMAIN_HOME` に行って `startWebLogic(.cmd/.sh)` を叩くだけ
  * Eclipse が作ったドメインも同じ要領で起動可能

---

もし次にやりたいことがあれば：

* 「コンソールから war をデプロイする手順をスクショ風に文字でステップ化して」
* 「Eclipse じゃなく、gradle/maven から WebLogic へデプロイしたい」
* 「単体起動した WebLogic に、今作ってるアプリを手動でデプロイする手順が知りたい」

みたいに言ってくれれば、そのパターンに絞って手順書風に整理します 👍

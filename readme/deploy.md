OK、Gradle 前提で **「WAR を作らず、クラスファイル＋リソースのディレクトリをそのまま WebLogic にデプロイする」** 流れを整理しますね。

---

## 全体像（Gradle でやること）

やることはシンプルに言うとこの 3 ステップです。

1. **exploded 構成のディレクトリを作る**
   （WAR 展開済みと同じ構造を Gradle のタスクで生成）

2. **`weblogic.Deployer` を Gradle の Exec タスクで叩いてデプロイ**

3. 必要なら **undeploy / redeploy 用タスク** も用意

以下、`build.gradle`（Groovy DSL）で書く想定でコード例をまとめます。

---

## 1. 前提ディレクトリ構成

標準的な Java Web アプリ想定：

```text
src/
  main/
    java/          … Java ソース
    resources/     … プロパティなど
    webapp/        … JSP や静的ファイル
      WEB-INF/
        web.xml
build/             … Gradle の出力
```

Gradle でコンパイルするとクラスはここに出ます：

```text
build/classes/java/main/
```

このクラスたちを、最終的にこんな構成にまとめます：

```text
build/exploded/myapp/
  （src/main/webapp の中身） 例: index.jsp, css など
  WEB-INF/
    web.xml
    classes/
      com/example/.../*.class
    lib/
      依存 jar
```

この `build/exploded/myapp` を、そのまま WebLogic にデプロイします。

---

## 2. exploded ディレクトリを作るタスク

`build.gradle` に追加：

```groovy
plugins {
    id 'java'
    id 'war'      // webapp 用（war は作るけど、使わなくてもOK）
}

group = 'com.example'
version = '1.0.0'

repositories {
    mavenCentral()
}

dependencies {
    // 例：必要な依存ライブラリ
    implementation 'org.springframework:spring-webmvc:5.3.39'
    // などなど
}

/**
 * exploded 用ディレクトリ生成タスク
 * build/exploded/myapp に「WAR 展開済み」の構造を作る
 */
task explodedWebapp(type: Sync) {
    // 出力先
    def appName = 'myapp'   // WebLogic 上のアプリ名にも使う
    into "$buildDir/exploded/${appName}"

    // JSP, 静的ファイルなど webapp の中身
    from('src/main/webapp') {
        // 必要なら除外/調整
        // exclude 'WEB-INF/web.xml'  // web.xml を別で扱いたいなら
    }

    // クラスファイル → WEB-INF/classes
    from("$buildDir/classes/java/main") {
        into 'WEB-INF/classes'
    }

    // resources（プロパティ等）もクラスパスに入れるなら
    from("$buildDir/resources/main") {
        into 'WEB-INF/classes'
    }

    // 依存 jar → WEB-INF/lib
    from(configurations.runtimeClasspath) {
        into 'WEB-INF/lib'
    }
}

// コンパイル後に exploded を作るように依存関係を追加
explodedWebapp.dependsOn classes, processResources
```

これで：

```bash
gradle clean explodedWebapp
```

とすると、`build/exploded/myapp` に WebLogic が食べられる形のディレクトリができます。

---

## 3. WebLogic へのデプロイタスク

次に、`weblogic.Deployer` を叩く `Exec` タスクを追加します。

```groovy
// ★ 環境に合わせて書き換えポイント ★
def weblogicHome = '/opt/oracle/middleware/wlserver'      // WebLogic のインストールパス
def wlJar        = "${weblogicHome}/server/lib/weblogic.jar"

def adminUrl     = 't3://localhost:7001'
def wlUser       = 'weblogic'
def wlPassword   = 'weblogic_password'
def wlTargets    = 'AdminServer'   // or クラスタ名
def appName      = 'myapp'         // explodedWebapp で使った名前と合わせる

/**
 * exploded ディレクトリを WebLogic にデプロイ
 */
task deployToWebLogic(type: Exec) {
    dependsOn explodedWebapp

    def sourceDir = file("$buildDir/exploded/${appName}").absolutePath

    commandLine 'java',
        '-cp', wlJar,
        'weblogic.Deployer',
        '-adminurl', adminUrl,
        '-username', wlUser,
        '-password', wlPassword,
        '-deploy',
        '-name', appName,
        '-source', sourceDir,
        '-targets', wlTargets,
        '-nostage'       // ディレクトリをそのまま参照させる
}

/**
 * アプリをアンデプロイするタスク
 */
task undeployFromWebLogic(type: Exec) {
    commandLine 'java',
        '-cp', wlJar,
        'weblogic.Deployer',
        '-adminurl', adminUrl,
        '-username', wlUser,
        '-password', wlPassword,
        '-undeploy',
        '-name', appName
}

/**
 * 既にデプロイ済みなら再デプロイしたい場合用
 */
task redeployToWebLogic(type: Exec) {
    dependsOn explodedWebapp

    def sourceDir = file("$buildDir/exploded/${appName}").absolutePath

    commandLine 'java',
        '-cp', wlJar,
        'weblogic.Deployer',
        '-adminurl', adminUrl,
        '-username', wlUser,
        '-password', wlPassword,
        '-redeploy',
        '-name', appName,
        '-source', sourceDir,
        '-targets', wlTargets,
        '-nostage'
}
```

---

## 4. 実行フロー

### 初回デプロイ

```bash
# クラスコンパイル → exploded ディレクトリ生成 → WebLogic に deploy
gradle deployToWebLogic
```

### コード修正後に反映（テーブル定義変わらない程度）

```bash
gradle redeployToWebLogic
```

※ WebLogic の設定によっては、`redeploy` なしでもクラス差し替えで済むケースもありますが、
とりあえず **コンパイル → exploded 更新 → redeploy** が一番確実です。

### アンデプロイしたい場合

```bash
gradle undeployFromWebLogic
```

---

## 5. ポイントだけおさらい

* **WAR を作らずに動かしたい** →
  実態は「WAR 展開済みディレクトリ」を作ってそれを WebLogic に食わせるイメージ

* Gradle 側では：

  * `Sync` タスクで `build/exploded/myapp` を構成
  * `weblogic.Deployer` を `Exec` タスクから呼び出し

* `-nostage` を指定することで、
  WebLogic は **そのディレクトリを直接参照**（Eclipse の開発スタイルに近づく）

---

もし

* 実際の WebLogic パス（Windows / Linux）
* Gradle のバージョン（7 / 8…）
* Spring MVC / Spring Boot などのフレームワーク

がわかれば、それ前提で **ほぼコピペで動く `build.gradle` 全体版** にして渡すこともできます。
とりあえず上の断片を貼り付けてみて、エラーや詰まるところがあればログ貼ってもらえれば一緒に直しましょう 💪

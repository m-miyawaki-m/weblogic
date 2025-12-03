マルチモジュールのGradleプロジェクト設定をご案内します。

## プロジェクト構造（想定）

```
main-project/
├── settings.gradle
├── build.gradle
├── lib/
│   ├── commons-lang3-3.12.0.jar
│   └── その他のjar...
├── module1/
│   ├── build.gradle
│   └── src/main/java/
├── module2/
│   ├── build.gradle
│   └── src/main/java/
└── module3/
    ├── build.gradle
    └── src/main/java/
```

## 設定ファイル

### 1. **settings.gradle**（ルート）
```gradle
rootProject.name = 'main-project'

include 'module1'
include 'module2'
include 'module3'
```

### 2. **build.gradle**（ルート）
```gradle
// 全モジュール共通の設定
subprojects {
    apply plugin: 'java'
    
    sourceCompatibility = 1.8
    targetCompatibility = 1.8
    
    // 文字エンコーディング設定
    tasks.withType(JavaCompile) {
        options.encoding = 'UTF-8'
    }
    
    repositories {
        mavenCentral()
    }
    
    // libディレクトリのjarファイルを全モジュールで利用
    dependencies {
        implementation fileTree(dir: "${rootProject.projectDir}/lib", include: ['*.jar'])
    }
}
```

### 3. **module1/build.gradle**
```gradle
dependencies {
    // 外部ライブラリ（必要に応じて）
    // implementation 'org.springframework:spring-core:5.3.20'
}
```

### 4. **module2/build.gradle**
```gradle
dependencies {
    // module1に依存する場合
    implementation project(':module1')
}
```

### 5. **module3/build.gradle**
```gradle
dependencies {
    implementation project(':module1')
    implementation project(':module2')
}
```

## Gradleコマンド

### **基本的なコンパイル**
```bash
# Windowsの場合
gradlew build

# すべてクリーンしてからビルド
gradlew clean build

# 特定のモジュールだけビルド
gradlew :module1:build
```

### **その他の便利なコマンド**
```bash
# コンパイルのみ（テストなし）
gradlew compileJava

# 依存関係の確認
gradlew dependencies

# タスク一覧の表示
gradlew tasks

# ビルドの詳細情報を表示
gradlew build --info
```

## VS Codeでの使用方法

1. **Gradle for Java**拡張機能をインストール
2. プロジェクトを開くと自動的にGradleプロジェクトとして認識される
3. サイドバーの「GRADLE PROJECTS」からタスクを実行可能

## 既存のsrc構造がsrc/main/javaでない場合

もし既存のソース構造が`module1/src/`直下にある場合:

```gradle
// module1/build.gradle
sourceSets {
    main {
        java {
            srcDirs = ['src']  // デフォルトのsrc/main/javaの代わりにsrcを使用
        }
    }
}
```

この設定で、既存のEclipseプロジェクト構造をそのまま維持できます。

何か不明点や、特定の要件（WebLogicへのWARファイル作成など）があれば教えてください。


# Gradleのコンパイルを徹底解説

## Gradleのコンパイルの仕組み

### **基本的な流れ**

```
ソースコード → コンパイル → クラスファイル → JAR/WAR
   (src/)      (compileJava)  (build/classes/) (build/libs/)
```

Gradleは以下の順序でコンパイルを実行します:

1. **依存関係の解決** - 必要なライブラリをダウンロード/確認
2. **ソースコードの検出** - `src/main/java`配下のJavaファイルを検出
3. **コンパイル** - javacを使ってクラスファイルに変換
4. **出力** - `build/classes/java/main/`に配置

## コンパイル関連のタスク

### **主要なコンパイルタスク**

```bash
# メインソースのコンパイル
gradlew compileJava

# テストコードのコンパイル
gradlew compileTestJava

# すべてのコンパイル（テスト含む）
gradlew classes

# ビルド全体（コンパイル + テスト + パッケージング）
gradlew build
```

### **タスクの依存関係**

```
build
 └─ assemble
     └─ jar
         └─ classes
             └─ compileJava
                 └─ processResources
```

`gradlew build`を実行すると、自動的に`compileJava`も実行されます。

## コンパイル設定の詳細

### **1. 基本的なコンパイル設定**

```gradle
// build.gradle

// Javaプラグインを適用
plugins {
    id 'java'
}

// Javaバージョンの指定
sourceCompatibility = '1.8'  // ソースコードのJavaバージョン
targetCompatibility = '1.8'  // コンパイル後のクラスファイルのバージョン

// または
java {
    sourceCompatibility = JavaVersion.VERSION_1_8
    targetCompatibility = JavaVersion.VERSION_1_8
}
```

### **2. コンパイルオプションの詳細設定**

```gradle
tasks.withType(JavaCompile) {
    // 文字エンコーディング（必須：日本語対応）
    options.encoding = 'UTF-8'
    
    // コンパイラの警告レベル
    options.compilerArgs << '-Xlint:unchecked'
    options.compilerArgs << '-Xlint:deprecation'
    
    // デバッグ情報を含める
    options.debug = true
    options.debugOptions.debugLevel = 'source,lines,vars'
    
    // 並列コンパイル
    options.fork = true
    options.forkOptions.maxHeapSize = '1g'
    
    // 増分コンパイル（デフォルトで有効）
    options.incremental = true
}
```

### **3. ソースディレクトリのカスタマイズ**

```gradle
// デフォルト: src/main/java

// Eclipseプロジェクトのような構造の場合
sourceSets {
    main {
        java {
            srcDirs = ['src']  // src/main/java の代わりに src を使用
        }
        resources {
            srcDirs = ['resources']
        }
    }
    test {
        java {
            srcDirs = ['test']
        }
    }
}
```

### **4. 複数のソースディレクトリ**

```gradle
sourceSets {
    main {
        java {
            srcDirs = ['src', 'src-generated', 'src-legacy']
        }
    }
}
```

## マルチモジュールでのコンパイル

### **プロジェクト構造**

```
main-project/
├── settings.gradle
├── build.gradle          # ルート設定
├── lib/
│   └── custom-lib.jar
├── module1/
│   ├── build.gradle
│   └── src/main/java/
├── module2/
│   ├── build.gradle
│   └── src/main/java/
└── module3/
    ├── build.gradle
    └── src/main/java/
```

### **ルートのbuild.gradle**

```gradle
// すべてのサブプロジェクト共通設定
subprojects {
    apply plugin: 'java'
    
    sourceCompatibility = '1.8'
    targetCompatibility = '1.8'
    
    // コンパイル設定
    tasks.withType(JavaCompile) {
        options.encoding = 'UTF-8'
        options.compilerArgs += ['-Xlint:unchecked', '-Xlint:deprecation']
    }
    
    repositories {
        mavenCentral()
    }
    
    // libディレクトリの共通JAR
    dependencies {
        implementation fileTree(dir: "${rootProject.projectDir}/lib", include: ['*.jar'])
    }
}
```

### **モジュール間の依存関係とコンパイル順序**

**module2/build.gradle:**
```gradle
dependencies {
    implementation project(':module1')  // module1に依存
}
```

**module3/build.gradle:**
```gradle
dependencies {
    implementation project(':module1')
    implementation project(':module2')
}
```

**コンパイル順序:**
```
1. module1 → コンパイル完了
2. module2 → module1を参照してコンパイル
3. module3 → module1, module2を参照してコンパイル
```

Gradleは自動的に依存関係を解析し、正しい順序でコンパイルします。

### **特定モジュールのみコンパイル**

```bash
# module1のみ
gradlew :module1:compileJava

# module2とその依存モジュール
gradlew :module2:compileJava

# すべてのモジュール
gradlew compileJava
```

## 依存関係の管理とコンパイル

### **1. 依存関係のスコープ**

```gradle
dependencies {
    // コンパイル時と実行時に必要
    implementation 'org.apache.commons:commons-lang3:3.12.0'
    
    // コンパイル時のみ必要（実行時は不要）
    compileOnly 'org.projectlombok:lombok:1.18.24'
    
    // コンパイル時に必要で、かつ依存先にも公開される
    api 'com.google.guava:guava:31.1-jre'
    
    // 実行時のみ必要
    runtimeOnly 'mysql:mysql-connector-java:8.0.30'
    
    // テストコンパイル・実行時のみ
    testImplementation 'junit:junit:4.13.2'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}
```

### **2. ローカルJARファイルの扱い**

```gradle
dependencies {
    // libディレクトリのすべてのJAR
    implementation fileTree(dir: 'lib', include: ['*.jar'])
    
    // 特定のJARファイル
    implementation files('lib/custom-library.jar')
    
    // 複数のJARファイル
    implementation files(
        'lib/library1.jar',
        'lib/library2.jar',
        'lib/library3.jar'
    )
}
```

### **3. モジュール間の依存関係**

```gradle
dependencies {
    // 別モジュールへの依存
    implementation project(':module1')
    
    // 別モジュールの特定の設定への依存
    implementation project(path: ':module1', configuration: 'archives')
}
```

## 増分コンパイル（Incremental Compilation）

### **仕組み**

Gradleはデフォルトで増分コンパイルを使用します:

1. **初回コンパイル**: すべてのソースをコンパイル
2. **2回目以降**: 変更されたファイルとその影響を受けるファイルのみコンパイル

```gradle
tasks.withType(JavaCompile) {
    // 増分コンパイルを有効化（デフォルトで有効）
    options.incremental = true
}
```

### **メリット**

```
初回ビルド: 60秒
2回目（変更なし）: 2秒（UP-TO-DATE）
2回目（1ファイル変更）: 5秒
```

### **キャッシュの確認**

```bash
# キャッシュを使用してビルド
gradlew build

# 出力例
> Task :module1:compileJava UP-TO-DATE
> Task :module2:compileJava
> Task :module3:compileJava UP-TO-DATE
```

`UP-TO-DATE`は再コンパイルがスキップされたことを示します。

## コンパイルエラーのデバッグ

### **1. 詳細なコンパイルログ**

```bash
# 詳細ログを表示
gradlew compileJava --info

# さらに詳細
gradlew compileJava --debug

# スタックトレース表示
gradlew compileJava --stacktrace
```

### **2. 依存関係の確認**

```bash
# すべての依存関係を表示
gradlew dependencies

# コンパイル時の依存関係のみ
gradlew dependencies --configuration compileClasspath

# 特定モジュールの依存関係
gradlew :module2:dependencies
```

### **3. クラスパスの確認**

```gradle
// build.gradleに追加
tasks.register('printClasspath') {
    doLast {
        println sourceSets.main.compileClasspath.asPath
    }
}
```

実行:
```bash
gradlew printClasspath
```

## コンパイルのパフォーマンス最適化

### **1. 並列ビルド**

```bash
# コマンドラインから
gradlew build --parallel

# または gradle.properties に設定
org.gradle.parallel=true
org.gradle.workers.max=4
```

### **2. ビルドキャッシュ**

```bash
# コマンドラインから
gradlew build --build-cache

# または gradle.properties に設定
org.gradle.caching=true
```

**gradle.properties（プロジェクトルート）:**
```properties
# 並列ビルド
org.gradle.parallel=true

# ビルドキャッシュ
org.gradle.caching=true

# デーモンモード
org.gradle.daemon=true

# ヒープサイズ
org.gradle.jvmargs=-Xmx2g -XX:MaxMetaspaceSize=512m

# ワーカー数
org.gradle.workers.max=4
```

### **3. 不要なタスクをスキップ**

```bash
# テストをスキップしてコンパイルのみ
gradlew build -x test

# 特定のモジュールを除外
gradlew build -x :module3:compileJava
```

## 実践的なコンパイル設定例

### **標準的なエンタープライズ設定**

```gradle
plugins {
    id 'java'
}

group = 'com.example'
version = '1.0.0'

java {
    sourceCompatibility = JavaVersion.VERSION_1_8
    targetCompatibility = JavaVersion.VERSION_1_8
}

repositories {
    mavenCentral()
}

dependencies {
    // Spring Framework
    implementation 'org.springframework:spring-context:5.3.20'
    implementation 'org.springframework:spring-jdbc:5.3.20'
    
    // データベース
    implementation 'com.oracle.database.jdbc:ojdbc8:21.5.0.0'
    
    // ユーティリティ
    implementation 'org.apache.commons:commons-lang3:3.12.0'
    
    // ログ
    implementation 'org.slf4j:slf4j-api:1.7.36'
    runtimeOnly 'ch.qos.logback:logback-classic:1.2.11'
    
    // ローカルライブラリ
    implementation fileTree(dir: 'lib', include: ['*.jar'])
    
    // テスト
    testImplementation 'junit:junit:4.13.2'
    testImplementation 'org.mockito:mockito-core:4.6.1'
}

tasks.withType(JavaCompile) {
    options.encoding = 'UTF-8'
    options.compilerArgs += [
        '-Xlint:unchecked',
        '-Xlint:deprecation',
        '-parameters'  // リフレクション用にパラメータ名を保持
    ]
}

// コンパイル結果の確認タスク
tasks.register('showCompileOutput') {
    doLast {
        println "Compiled classes location: ${sourceSets.main.java.outputDir}"
        fileTree(sourceSets.main.java.outputDir).each { file ->
            println file.path
        }
    }
}
```

## よくあるコンパイルエラーと対処法

### **1. エンコーディングエラー**

```
エラー: この文字は、エンコーディングwindows-31jにマップできません
```

**対処法:**
```gradle
tasks.withType(JavaCompile) {
    options.encoding = 'UTF-8'
}
```

### **2. クラスが見つからない**

```
エラー: パッケージcom.example.moduleは存在しません
```

**対処法:**
```gradle
// 依存関係を確認
dependencies {
    implementation project(':module1')  // モジュール依存を追加
}
```

### **3. Javaバージョンの不一致**

```
エラー: 無効なターゲット・リリース: 11
```

**対処法:**
```gradle
java {
    sourceCompatibility = JavaVersion.VERSION_1_8
    targetCompatibility = JavaVersion.VERSION_1_8
}
```

### **4. 重複クラス**

```
エラー: クラスcom.example.Utilityが重複しています
```

**対処法:**
```gradle
dependencies {
    // excludeで重複を除外
    implementation('com.example:library:1.0') {
        exclude group: 'commons-logging', module: 'commons-logging'
    }
}
```

## VS Codeでのコンパイル確認

### **1. 問題パネルで確認**

`Ctrl+Shift+M`で問題パネルを開くと、コンパイルエラーが表示されます。

### **2. タスクの実行状況**

下部のステータスバーに実行中のタスクが表示されます。

### **3. 出力ログ**

`表示` → `出力` → `Gradle for Java`を選択してログを確認。

何か特定のコンパイルの問題やシナリオについて、さらに詳しく知りたいことはありますか？
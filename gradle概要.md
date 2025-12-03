# Gradle概要ガイド（Windows & VS Code環境）

## Gradleとは

**Gradle**は、Javaプロジェクトのビルド自動化ツールです。コンパイル、テスト、パッケージング、デプロイなどを自動化します。

### 主な特徴
- **柔軟性**: Groovy/Kotlinでビルドスクリプトを記述
- **高速**: 差分ビルドとキャッシュで効率的
- **マルチモジュール対応**: 複雑なプロジェクト構成に対応
- **依存関係管理**: 外部ライブラリを自動ダウンロード

## 主な用途

### 1. **コンパイル**
Javaソースコードをクラスファイルに変換

### 2. **依存関係管理**
- 外部ライブラリの自動ダウンロード
- バージョン管理
- モジュール間の依存関係解決

### 3. **テスト実行**
JUnitなどのテストフレームワークと連携

### 4. **パッケージング**
- JARファイル作成
- WARファイル作成（Webアプリケーション）
- 配布用のアーカイブ作成

### 5. **デプロイ**
WebLogicなどのアプリケーションサーバーへのデプロイ

## Windows環境でのセットアップ

### 1. **Gradleのインストール**

プロジェクトに**Gradle Wrapper**（推奨）がある場合は不要です。

```bash
# プロジェクトルートに以下のファイルがあればインストール不要
gradlew.bat       # Windowsコマンド
gradle/wrapper/   # Wrapperファイル
```

手動インストールする場合:
```bash
# Chocolateyを使用（推奨）
choco install gradle

# または公式サイトからダウンロード
# https://gradle.org/releases/
```

### 2. **VS Codeのセットアップ**

必要な拡張機能:
- **Extension Pack for Java**（必須）
- **Gradle for Java**（必須）

インストール後、VS Codeを再起動してください。

## 主要コマンド一覧

### **基本コマンド**

```bash
# プロジェクト全体をビルド
gradlew build

# クリーン（生成ファイルを削除）してビルド
gradlew clean build

# コンパイルのみ（テストなし）
gradlew compileJava

# テスト実行
gradlew test

# テストをスキップしてビルド
gradlew build -x test
```

### **情報確認コマンド**

```bash
# 利用可能なタスク一覧を表示
gradlew tasks

# すべてのタスク（内部タスク含む）を表示
gradlew tasks --all

# プロジェクトの依存関係を表示
gradlew dependencies

# プロジェクト構造を表示
gradlew projects

# Gradleのバージョン確認
gradlew --version
```

### **マルチモジュール用コマンド**

```bash
# 特定のモジュールだけビルド
gradlew :module1:build

# 特定のモジュールのタスク実行
gradlew :module2:compileJava

# すべてのモジュールをクリーンビルド
gradlew clean :module1:build :module2:build :module3:build
```

### **デバッグ・トラブルシューティング**

```bash
# 詳細なログを表示
gradlew build --info

# さらに詳細なデバッグログ
gradlew build --debug

# ビルド時間を計測
gradlew build --profile

# キャッシュをクリア
gradlew clean --refresh-dependencies
```

### **WAR/JARファイル作成**

```bash
# JARファイル作成
gradlew jar

# WARファイル作成（Webアプリの場合）
gradlew war

# 成果物の確認
# build/libs/ ディレクトリに生成されます
```

## VS Codeでの使い方

### **GUIからの実行**

1. サイドバーの**GRADLE PROJECTS**を開く
2. プロジェクトを展開
3. タスクをダブルクリックで実行

よく使うタスク:
- `build` → `build`: プロジェクト全体をビルド
- `build` → `clean`: 生成ファイルを削除
- `application` → `run`: アプリケーション実行（設定済みの場合）

### **ターミナルからの実行**

VS Code内蔵ターミナル（Ctrl + @）で:
```bash
# PowerShellまたはコマンドプロンプト
gradlew build
```

### **タスクの設定**

`.vscode/tasks.json`を作成してショートカット設定:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Gradle Build",
            "type": "shell",
            "command": "./gradlew",
            "args": ["build"],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "problemMatcher": []
        }
    ]
}
```

これで`Ctrl+Shift+B`でビルドできます。

## 実践例: マルチモジュールプロジェクト

### **プロジェクト作成の流れ**

```bash
# 1. プロジェクトディレクトリに移動
cd main-project

# 2. Gradle Wrapperを生成（初回のみ）
gradle wrapper

# 3. ビルド実行
gradlew build

# 4. 生成されたファイルを確認
# module1/build/classes/java/main/
# module1/build/libs/module1.jar
```

### **よくある作業フロー**

```bash
# 1. 変更前にクリーン
gradlew clean

# 2. コンパイルして確認
gradlew compileJava

# 3. テスト実行
gradlew test

# 4. 最終ビルド
gradlew build

# 5. 成果物を確認
dir build\libs
```

## トラブルシューティング

### **エンコーディングエラー**
```gradle
tasks.withType(JavaCompile) {
    options.encoding = 'UTF-8'
}
```

### **Javaバージョン指定**
```gradle
sourceCompatibility = 1.8
targetCompatibility = 1.8
```

### **依存関係が解決できない**
```bash
# キャッシュをクリアして再取得
gradlew clean build --refresh-dependencies
```

### **VS Codeで認識されない**
1. VS Codeを再起動
2. `Ctrl+Shift+P` → "Java: Clean Java Language Server Workspace"
3. プロジェクトを再度開く

## 次のステップ

実際にマルチモジュールプロジェクトで試してみる場合は、先ほどご案内した設定ファイルを使って:

```bash
gradlew build
```

を実行してみてください。何かエラーが出た場合は、そのメッセージを教えていただければ対処方法をお伝えします。
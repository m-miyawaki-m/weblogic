はい、可能です。プロジェクト構造を変えずに、**VS Codeの設定だけで対応**できます。

## VS Code側の設定のみで対応する方法

### 前提条件の確認

まず、Eclipseユーザーライブラリの実体(JARファイル)がどこにあるか確認します:

```
Eclipse > Window > Preferences > Java > Build Path > User Libraries
> Spring5を選択 > 各JARのLocationをメモ
```

例:
```
Spring5:
  /opt/libraries/spring/spring-core-5.3.20.jar
  /opt/libraries/spring/spring-context-5.3.20.jar

MyBatis:
  /opt/libraries/mybatis/mybatis-3.5.10.jar
```

## 解決策: VS Codeのsettings.jsonで対応

### 方法1: java.project.referencedLibraries を使う (推奨)

`.vscode/settings.json` を作成:

```json
{
    "java.project.referencedLibraries": [
        "/opt/libraries/spring/*.jar",
        "/opt/libraries/mybatis/*.jar",
        "/opt/libraries/jackson/*.jar"
    ]
}
```

これにより:
- `.classpath`は変更不要
- Eclipse上では従来通りユーザーライブラリを使用
- VS Code上では`referencedLibraries`で指定したJARを認識

### 方法2: 環境変数を使って柔軟に対応

開発者ごとにライブラリの場所が異なる場合:

**環境変数を設定:**
```bash
# ~/.bashrc または ~/.zshrc
export JAVA_LIB_HOME=/opt/libraries
```

**.vscode/settings.json:**
```json
{
    "java.project.referencedLibraries": [
        "${env:JAVA_LIB_HOME}/spring/*.jar",
        "${env:JAVA_LIB_HOME}/mybatis/*.jar"
    ]
}
```

### 方法3: 相対パスで共有ライブラリを参照

チーム開発で共有サーバーにライブラリがある場合:

```json
{
    "java.project.referencedLibraries": [
        "//shared-server/libraries/spring/*.jar",
        "//shared-server/libraries/mybatis/*.jar"
    ]
}
```

または、シンボリックリンクを使う:
```bash
# プロジェクトルートで実行
ln -s /opt/libraries ./external-libs

# .vscode/settings.json
{
    "java.project.referencedLibraries": [
        "external-libs/spring/*.jar",
        "external-libs/mybatis/*.jar"
    ]
}
```

```bash
# .gitignoreに追加
echo "external-libs" >> .gitignore
```

## 完全な設定例

### .vscode/settings.json (完全版)

```json
{
    // Javaのバージョン設定
    "java.configuration.runtimes": [
        {
            "name": "JavaSE-11",
            "path": "/usr/lib/jvm/java-11-openjdk",
            "default": true
        }
    ],
    
    // ビルド設定の自動更新
    "java.configuration.updateBuildConfiguration": "automatic",
    
    // Eclipseユーザーライブラリの代替
    "java.project.referencedLibraries": [
        // Spring5ユーザーライブラリの代替
        "/opt/libraries/spring/spring-core-*.jar",
        "/opt/libraries/spring/spring-context-*.jar",
        "/opt/libraries/spring/spring-beans-*.jar",
        "/opt/libraries/spring/spring-web-*.jar",
        
        // MyBatisユーザーライブラリの代替
        "/opt/libraries/mybatis/mybatis-*.jar",
        "/opt/libraries/mybatis/mybatis-spring-*.jar",
        
        // Jacksonユーザーライブラリの代替
        "/opt/libraries/jackson/jackson-core-*.jar",
        "/opt/libraries/jackson/jackson-databind-*.jar",
        "/opt/libraries/jackson/jackson-annotations-*.jar",
        
        // その他の共通ライブラリ
        "/opt/libraries/commons/*.jar"
    ],
    
    // Gradle/Mavenインポートを無効化 (Eclipseプロジェクトのみ使用)
    "java.import.gradle.enabled": false,
    "java.import.maven.enabled": false,
    
    // 出力先
    "java.project.outputPath": "bin",
    
    // ソースエンコーディング
    "files.encoding": "utf8",
    
    // 自動保存でビルド
    "java.autobuild.enabled": true
}
```

## マルチモジュールプロジェクトの場合

各モジュールで異なるライブラリを使う場合は、ルートの`.vscode/settings.json`に全て列挙:

```json
{
    "java.project.referencedLibraries": [
        // module-a用
        "/opt/libraries/spring/*.jar",
        
        // module-b用  
        "/opt/libraries/spring/*.jar",
        "/opt/libraries/mybatis/*.jar",
        
        // module-c用
        "/opt/libraries/mybatis/*.jar",
        "/opt/libraries/jackson/*.jar"
    ]
}
```

重複していても問題ありません。VS Codeが自動的に整理します。

## confのプロパティファイルを活用する方法

既に`conf/libraries.properties`がある場合、スクリプトで`.vscode/settings.json`を自動生成:

**conf/libraries.properties:**
```properties
spring.lib.path=/opt/libraries/spring
mybatis.lib.path=/opt/libraries/mybatis
jackson.lib.path=/opt/libraries/jackson
```

**generate_vscode_settings.sh:**
```bash
#!/bin/bash

PROPS_FILE="conf/libraries.properties"
OUTPUT_FILE=".vscode/settings.json"

# .vscodeディレクトリ作成
mkdir -p .vscode

# settings.jsonの生成開始
cat > $OUTPUT_FILE <<'EOF'
{
    "java.configuration.updateBuildConfiguration": "automatic",
    "java.import.gradle.enabled": false,
    "java.import.maven.enabled": false,
    "java.project.referencedLibraries": [
EOF

# プロパティファイルから読み込んでパスを追加
while IFS='=' read -r key value; do
    if [[ $key == *.lib.path ]]; then
        echo "        \"$value/*.jar\"," >> $OUTPUT_FILE
    fi
done < $PROPS_FILE

# 最後のカンマを削除してJSONを閉じる
sed -i '$ s/,$//' $OUTPUT_FILE
cat >> $OUTPUT_FILE <<'EOF'
    ]
}
EOF

echo "Generated $OUTPUT_FILE"
```

使い方:
```bash
chmod +x generate_vscode_settings.sh
./generate_vscode_settings.sh
```

生成される`.vscode/settings.json`:
```json
{
    "java.configuration.updateBuildConfiguration": "automatic",
    "java.import.gradle.enabled": false,
    "java.import.maven.enabled": false,
    "java.project.referencedLibraries": [
        "/opt/libraries/spring/*.jar",
        "/opt/libraries/mybatis/*.jar",
        "/opt/libraries/jackson/*.jar"
    ]
}
```

## .gitignoreの設定

`.vscode/settings.json`をGitで管理するかどうか:

### パターンA: チーム全体で同じパスを使う場合
```bash
# .vscode/settings.jsonをコミット
git add .vscode/settings.json
git commit -m "Add VS Code settings"
```

### パターンB: 開発者ごとにパスが異なる場合
```bash
# .gitignoreに追加
echo ".vscode/settings.json" >> .gitignore

# テンプレートを提供
cp .vscode/settings.json .vscode/settings.json.template
git add .vscode/settings.json.template
```

各開発者が:
```bash
cp .vscode/settings.json.template .vscode/settings.json
# 自分の環境に合わせてパスを修正
```

## 動作確認

### ステップ1: VS Codeを再起動
```bash
# VS Codeを閉じて再度開く
code .
```

### ステップ2: Java Language Serverを再起動
```
Ctrl+Shift+P > "Java: Clean Java Language Server Workspace"
```

### ステップ3: 確認項目
- [ ] Javaファイルを開いてエラーが出ないか
- [ ] 外部ライブラリのクラスにカーソルを合わせて定義にジャンプできるか (F12)
- [ ] コード補完が効くか (Ctrl+Space)
- [ ] モジュール間の参照が正常か

### ステップ4: ビルド確認
```bash
# ファイルを編集して保存
# → bin/にクラスファイルが自動生成されることを確認
```

## トラブルシューティング

### 問題1: ライブラリが認識されない

**確認1: パスが正しいか**
```bash
ls /opt/libraries/spring/*.jar
# JARファイルが表示されるか確認
```

**確認2: settings.jsonの構文エラー**
```
Ctrl+Shift+P > "Preferences: Open Settings (JSON)"
# JSONが正しいか確認
```

**確認3: Java Language Serverのログ確認**
```
Ctrl+Shift+P > "Java: Open Java Language Server Log File"
# エラーメッセージを確認
```

### 問題2: .classpathのUSER_LIBRARYが邪魔をする

VS Codeが`.classpath`のUSER_LIBRARYエントリを認識してエラーを出す場合:

**.vscode/settings.json に追加:**
```json
{
    "java.import.exclusions": [
        "**/org.eclipse.jdt.USER_LIBRARY/**"
    ]
}
```

### 問題3: ワイルドカード(*)が効かない

特定のJARファイルのみを個別に指定:
```json
{
    "java.project.referencedLibraries": [
        "/opt/libraries/spring/spring-core-5.3.20.jar",
        "/opt/libraries/spring/spring-context-5.3.20.jar",
        "/opt/libraries/mybatis/mybatis-3.5.10.jar"
    ]
}
```

## まとめ: プロジェクト構造を変えない対応

**結論:**
- ✅ `.classpath`は変更不要
- ✅ Eclipseユーザーライブラリも残したまま
- ✅ `.vscode/settings.json`だけで対応可能
- ✅ Eclipse/VS Code両環境で開発可能

**必要な作業:**
1. Eclipseでユーザーライブラリの実体のパスを確認
2. `.vscode/settings.json`を作成
3. `java.project.referencedLibraries`に実体のパスを記述
4. VS Codeを再起動して確認

これで、プロジェクト構造を一切変更せず、VS Code側の設定だけで対応できます。

はい、VS CodeからWebLogicへの動的なリモートデバッグは可能です。Eclipseと同様の体験を実現できます。

## 1. WebLogicのデバッグモード起動

### 方法A: setDomainEnv.sh を編集（永続的）

**$DOMAIN_HOME/bin/setDomainEnv.sh を編集:**
```bash
# デバッグ設定を追加（ファイルの末尾近く）

# 既存のJAVA_OPTIONSの後に追加
debugFlag="true"
export debugFlag

if [ "${debugFlag}" = "true" ]; then
    JAVA_OPTIONS="${JAVA_OPTIONS} -Xdebug -Xrunjdwp:transport=dt_socket,address=*:8453,server=y,suspend=n"
    echo "Debug mode enabled on port 8453"
fi

export JAVA_OPTIONS
```

**注意:** 
- `address=*:8453` の `*` は全てのネットワークインターフェースからの接続を許可
- ローカルのみなら `address=localhost:8453` または `address=127.0.0.1:8453`
- `suspend=n` は起動時にデバッガーの接続を待たない（すぐ起動）
- `suspend=y` にするとデバッガー接続まで起動を待機

### 方法B: 起動スクリプトで指定（一時的）

**scripts/start_weblogic_debug.sh:**
```bash
#!/bin/bash

export DOMAIN_HOME="/path/to/weblogic/user_projects/domains/mydomain"

# デバッグオプションを追加
export JAVA_OPTIONS="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=*:8453"

echo "Starting WebLogic in debug mode on port 8453..."
$DOMAIN_HOME/bin/startWebLogic.sh
```

または、Java 9以降の新しい構文:
```bash
export JAVA_OPTIONS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8453"
```

### 方法C: VS Codeタスクで起動

**.vscode/tasks.json:**
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start WebLogic (Debug Mode)",
            "type": "shell",
            "command": "bash",
            "args": [
                "-c",
                "export JAVA_OPTIONS='-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8453' && ${env:DOMAIN_HOME}/bin/startWebLogic.sh"
            ],
            "isBackground": true,
            "problemMatcher": {
                "pattern": {
                    "regexp": "^(.*)$",
                    "file": 1
                },
                "background": {
                    "activeOnStart": true,
                    "beginsPattern": ".*Starting WebLogic Server.*",
                    "endsPattern": ".*Server state changed to RUNNING.*"
                }
            },
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            }
        },
        {
            "label": "Stop WebLogic",
            "type": "shell",
            "command": "${env:DOMAIN_HOME}/bin/stopWebLogic.sh",
            "problemMatcher": []
        }
    ]
}
```

使い方:
```
Terminal > Run Task > "Start WebLogic (Debug Mode)"
```

## 2. VS Codeのデバッグ設定

### 基本的なリモートデバッグ設定

**.vscode/launch.json:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "java",
            "name": "Attach to WebLogic",
            "request": "attach",
            "hostName": "localhost",
            "port": 8453,
            "projectName": "web-module"
        }
    ]
}
```

### 複数サーバー対応

**.vscode/launch.json (拡張版):**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "java",
            "name": "Attach to WebLogic (Local)",
            "request": "attach",
            "hostName": "localhost",
            "port": 8453,
            "projectName": "web-module"
        },
        {
            "type": "java",
            "name": "Attach to WebLogic (Dev Server)",
            "request": "attach",
            "hostName": "dev-server.example.com",
            "port": 8453,
            "projectName": "web-module"
        },
        {
            "type": "java",
            "name": "Attach to WebLogic (Staging)",
            "request": "attach",
            "hostName": "staging-server.example.com",
            "port": 8453,
            "projectName": "web-module"
        }
    ]
}
```

### マルチモジュール対応

マルチモジュールプロジェクトの場合、複数のプロジェクトを指定できます:

```json
{
    "type": "java",
    "name": "Attach to WebLogic (All Modules)",
    "request": "attach",
    "hostName": "localhost",
    "port": 8453,
    "projectName": ["common-lib", "business-logic", "web-module"]
}
```

## 3. デバッグの実行方法

### ステップ1: WebLogicをデバッグモードで起動

```bash
# 方法1: スクリプトで起動
./scripts/start_weblogic_debug.sh

# 方法2: VS Codeタスクで起動
# Terminal > Run Task > "Start WebLogic (Debug Mode)"

# 方法3: 通常起動（setDomainEnv.shを編集済みの場合）
$DOMAIN_HOME/bin/startWebLogic.sh
```

起動ログで確認:
```
Listening for transport dt_socket at address: 8453
```

### ステップ2: VS Codeからアタッチ

```
1. F5キーを押す
   または
   Run > Start Debugging

2. "Attach to WebLogic" を選択

3. ステータスバーに "Debugger attached" と表示される
```

### ステップ3: ブレークポイントの設定

```java
// 例: コントローラークラス
@Controller
public class UserController {
    
    @RequestMapping("/user/list")
    public String listUsers(Model model) {
        // ここにブレークポイントを設定 ← 行番号の左をクリック
        List<User> users = userService.findAll();
        model.addAttribute("users", users);
        return "user/list";
    }
}
```

### ステップ4: デバッグ実行

```
1. ブラウザでアプリケーションにアクセス
   http://localhost:7001/myapp/user/list

2. ブレークポイントで処理が停止

3. VS Codeのデバッグビューで変数の確認、ステップ実行など
```

## 4. 動的なホットスワップ（Hot Swap）

### VS Codeでのホットスワップ設定

**.vscode/settings.json:**
```json
{
    "java.debug.settings.hotCodeReplace": "auto",
    "java.debug.settings.enableHotCodeReplace": true,
    "java.autobuild.enabled": true
}
```

### ホットスワップの動作

```
デバッグ中に:
1. Javaファイルを編集
2. 保存 (Ctrl+S)
3. VS Codeが自動コンパイル
4. デバッガーが自動的にクラスを再ロード（Hot Swap）
5. 処理を継続
```

**制限事項:**
- メソッドの本体の変更: ✅ 可能
- 新しいメソッドの追加: ❌ 不可（サーバー再起動が必要）
- クラス構造の変更: ❌ 不可
- フィールドの追加・削除: ❌ 不可

### より強力なホットスワップ: JRebel（有料）

制限を回避したい場合は JRebel を使用:

```bash
# JRebelエージェントを追加
export JAVA_OPTIONS="-agentpath:/path/to/jrebel/lib/libjrebel64.so -Drebel.remoting_plugin=true -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8453"
```

## 5. 自動デプロイ + 自動アタッチ

### 統合ワークフロー

**.vscode/tasks.json に追加:**
```json
{
    "label": "Build, Deploy, and Debug",
    "dependsOrder": "sequence",
    "dependsOn": [
        "Deploy Exploded to WebLogic",
        "Start WebLogic (Debug Mode)"
    ],
    "problemMatcher": []
}
```

**.vscode/launch.json に追加:**
```json
{
    "type": "java",
    "name": "Deploy and Debug WebLogic",
    "request": "attach",
    "hostName": "localhost",
    "port": 8453,
    "preLaunchTask": "Build, Deploy, and Debug",
    "postDebugTask": "Stop WebLogic"
}
```

使い方:
```
F5 を押すだけで:
1. ビルド
2. デプロイ
3. WebLogic起動
4. デバッガーアタッチ
が自動実行される
```

## 6. ファイル変更の自動検知 + リデプロイ

### Watchモード + 自動リロード

**scripts/watch_deploy_reload.sh:**
```bash
#!/bin/bash

PROJECT_ROOT="/path/to/your/project"
WEBLOGIC_DEPLOY_DIR="/path/to/weblogic/.../autodeploy/myapp"
WEBLOGIC_ADMIN_URL="t3://localhost:7001"
WEBLOGIC_USER="weblogic"
WEBLOGIC_PASSWORD="password"

echo "Watching for file changes and auto-deploying..."

inotifywait -m -r -e modify,create \
    "$PROJECT_ROOT/module-a/bin" \
    "$PROJECT_ROOT/module-b/bin" \
    "$PROJECT_ROOT/web-module/bin" | while read path action file; do
    
    if [[ "$file" == *.class ]]; then
        echo "Detected class change: $file"
        
        # クラスファイルをコピー
        RELATIVE_PATH="${path#$PROJECT_ROOT/*/bin/}"
        TARGET_DIR="$WEBLOGIC_DEPLOY_DIR/WEB-INF/classes/$RELATIVE_PATH"
        mkdir -p "$TARGET_DIR"
        cp "$path/$file" "$TARGET_DIR/"
        
        # WebLogicに再デプロイ通知（オプション）
        echo "Notifying WebLogic to reload..."
        touch "$WEBLOGIC_DEPLOY_DIR/WEB-INF/web.xml"
        
        # または WLST スクリプトで明示的に再デプロイ
        # wlst.sh scripts/redeploy.py
    fi
done
```

**scripts/redeploy.py (WLST スクリプト):**
```python
# WebLogic Scripting Tool (WLST) スクリプト

connect('weblogic', 'password', 't3://localhost:7001')

try:
    print('Redeploying application...')
    redeploy('myapp', upload=false)
    print('Redeploy completed')
except Exception, e:
    print('Redeploy failed: ' + str(e))

disconnect()
```

## 7. デバッグ中の便利な機能

### 条件付きブレークポイント

```java
public String processUser(User user) {
    // ブレークポイントを右クリック > Edit Breakpoint
    // Condition: user.getId() == 123
    // 特定のIDのときだけ停止
    return userService.process(user);
}
```

### ログポイント（ブレークせずにログ出力）

```java
public void updateUser(User user) {
    // ブレークポイントを右クリック > Edit Breakpoint
    // Log Message: User {user.getName()} is being updated
    userRepository.save(user);
}
```

### 式の評価

```
デバッグ中に:
1. Debug Console で任意のJavaコードを実行
   例: user.getName()
   例: userService.findById(123)

2. Watch ビューで式を監視
   例: users.size()
   例: request.getParameter("id")
```

### ステップフィルター

**.vscode/settings.json:**
```json
{
    "java.debug.settings.stepping.skipClasses": [
        "java.lang.ClassLoader",
        "org.springframework.cglib.*",
        "com.sun.*"
    ],
    "java.debug.settings.stepping.skipSynthetics": true,
    "java.debug.settings.stepping.skipStaticInitializers": true,
    "java.debug.settings.stepping.skipConstructors": false
}
```

## 8. リモートサーバーのデバッグ

開発サーバーや他のマシンのWebLogicをデバッグする場合:

### サーバー側の設定

```bash
# リモートサーバーで
export JAVA_OPTIONS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8453"
./startWebLogic.sh
```

**ファイアウォール設定:**
```bash
# ポート8453を開放
sudo firewall-cmd --permanent --add-port=8453/tcp
sudo firewall-cmd --reload
```

### VS Code側の設定

**.vscode/launch.json:**
```json
{
    "type": "java",
    "name": "Attach to Remote WebLogic",
    "request": "attach",
    "hostName": "remote-server.example.com",
    "port": 8453,
    "projectName": "web-module",
    
    // ソースパスのマッピング（必要に応じて）
    "sourcePaths": [
        "${workspaceFolder}/module-a/src",
        "${workspaceFolder}/module-b/src",
        "${workspaceFolder}/web-module/src"
    ]
}
```

### SSHトンネル経由のデバッグ

セキュリティ上、デバッグポートを直接公開したくない場合:

```bash
# ローカルマシンでSSHトンネルを作成
ssh -L 8453:localhost:8453 user@remote-server.example.com

# VS Codeは localhost:8453 に接続
# → SSHトンネル経由でリモートサーバーに転送される
```

**.vscode/launch.json:**
```json
{
    "type": "java",
    "name": "Attach via SSH Tunnel",
    "request": "attach",
    "hostName": "localhost",  // SSHトンネルのローカル側
    "port": 8453,
    "projectName": "web-module"
}
```

## 9. トラブルシューティング

### 問題1: デバッガーがアタッチできない

**確認事項:**
```bash
# WebLogicがデバッグポートで待ち受けているか確認
netstat -an | grep 8453
# または
lsof -i :8453

# ポートが開いていない場合
# → setDomainEnv.sh または起動スクリプトを確認
```

### 問題2: ブレークポイントで停止しない

**原因と対処:**
1. **クラスファイルとソースが不一致**
   ```bash
   # 再ビルド・再デプロイ
   Terminal > Run Task > "Deploy Exploded to WebLogic"
   ```

2. **WebLogicが古いクラスをロードしている**
   ```bash
   # WebLogicを再起動
   $DOMAIN_HOME/bin/stopWebLogic.sh
   ./scripts/start_weblogic_debug.sh
   ```

3. **ブレークポイントが灰色表示**
   - ソースパスが正しいか確認
   - `.vscode/launch.json` の `sourcePaths` を確認

### 問題3: ホットスワップが効かない

**対処:**
```json
// .vscode/settings.json
{
    "java.debug.settings.hotCodeReplace": "manual"
}
```

手動でホットスワップ:
```
デバッグ中に:
Ctrl+Shift+P > "Java: Hot Code Replace"
```

### 問題4: マルチモジュールでソースが見つからない

**.vscode/launch.json:**
```json
{
    "type": "java",
    "name": "Attach to WebLogic",
    "request": "attach",
    "hostName": "localhost",
    "port": 8453,
    "sourcePaths": [
        "${workspaceFolder}/common-lib/src",
        "${workspaceFolder}/business-logic/src",
        "${workspaceFolder}/web-module/src",
        "${workspaceFolder}/common-lib/resources",
        "${workspaceFolder}/business-logic/resources",
        "${workspaceFolder}/web-module/resources"
    ]
}
```

## まとめ: VS CodeでWebLogic動的リモートデバッグ

**手順:**
1. WebLogicをデバッグモードで起動 (JDWP有効化)
2. VS Codeでデバッグ構成を作成 (launch.json)
3. F5でアタッチ
4. ブレークポイント設定してデバッグ

**Eclipseとの比較:**
| 機能 | Eclipse | VS Code |
|------|---------|---------|
| サーバー統合 | ○ 自動 | △ タスクで対応 |
| リモートデバッグ | ○ | ○ 同等 |
| ホットスワップ | ○ | ○ 同等 |
| ブレークポイント | ○ | ○ 同等 |
| 式の評価 | ○ | ○ 同等 |
| 自動再デプロイ | ○ | △ スクリプトで対応 |

**推奨構成:**
- デバッグポート: 8453 (デフォルトの8453を使用)
- 起動: VS Codeタスクまたはスクリプト
- デプロイ: watch + 自動デプロイスクリプト
- デバッグ: リモートアタッチ

この構成で、Eclipseと同等のデバッグ体験をVS Codeで実現できます。
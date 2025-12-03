# Gradle vs Maven 比較ガイド

## 概要比較

| 項目 | Gradle | Maven |
|------|--------|-------|
| **設定ファイル** | build.gradle (Groovy/Kotlin) | pom.xml (XML) |
| **記述量** | 少ない（簡潔） | 多い（冗長） |
| **ビルド速度** | 高速（差分ビルド・キャッシュ） | やや遅い |
| **柔軟性** | 非常に高い（プログラマブル） | 制約が多い（規約重視） |
| **学習曲線** | やや急（自由度が高い分複雑） | 緩やか（規約が明確） |
| **採用企業** | Google, Netflix, LinkedIn | 多くのエンタープライズ企業 |
| **リリース** | 2012年 | 2004年 |

## 設定ファイルの比較

### **同じ依存関係を定義する場合**

**Gradle (build.gradle):**
```gradle
dependencies {
    implementation 'org.springframework:spring-core:5.3.20'
    implementation 'commons-io:commons-io:2.11.0'
    testImplementation 'junit:junit:4.13.2'
}
```

**Maven (pom.xml):**
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>5.3.20</version>
    </dependency>
    <dependency>
        <groupId>commons-io</groupId>
        <artifactId>commons-io</artifactId>
        <version>2.11.0</version>
    </dependency>
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.13.2</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

**記述量**: Gradleの方が約60%少ない

## できることの比較

### 1. **基本的なビルド機能**

| 機能 | Gradle | Maven |
|------|--------|-------|
| コンパイル | ✅ | ✅ |
| テスト実行 | ✅ | ✅ |
| JAR/WAR作成 | ✅ | ✅ |
| 依存関係管理 | ✅ | ✅ |
| マルチモジュール | ✅ | ✅ |

**どちらでも実現可能**

### 2. **ビルドパフォーマンス**

**Gradle:**
```bash
# 差分ビルド（変更部分のみ）
gradlew build
# → 2回目以降は高速（数秒）

# 並列ビルド（デフォルトで有効）
gradlew build --parallel

# ビルドキャッシュ
gradlew build --build-cache
```

**Maven:**
```bash
# 毎回フルビルド（デフォルト）
mvn clean install
# → 毎回時間がかかる

# 並列ビルド（手動設定が必要）
mvn clean install -T 4
```

**結果**: Gradleの方が2〜10倍高速（プロジェクト規模による）

### 3. **マルチモジュールプロジェクト**

**Gradle (settings.gradle):**
```gradle
rootProject.name = 'main-project'
include 'module1', 'module2', 'module3'
```

**Maven (pom.xml):**
```xml
<modules>
    <module>module1</module>
    <module>module2</module>
    <module>module3</module>
</modules>
```

**モジュール間の依存関係:**

**Gradle:**
```gradle
dependencies {
    implementation project(':module1')
}
```

**Maven:**
```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>module1</artifactId>
    <version>${project.version}</version>
</dependency>
```

**結果**: どちらも対応可能だが、Gradleの方が簡潔

### 4. **カスタムタスク（柔軟性）**

**Gradle: 独自タスクを簡単に追加できる**
```gradle
// カスタムタスクの定義
task copyLibs(type: Copy) {
    from 'lib'
    into 'build/output/lib'
}

task deploy {
    doLast {
        exec {
            commandLine 'cmd', '/c', 'deploy.bat'
        }
    }
}

build.dependsOn copyLibs
```

**Maven: プラグインを使うか、独自プラグイン開発が必要**
```xml
<plugin>
    <artifactId>maven-antrun-plugin</artifactId>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>run</goal>
            </goals>
            <configuration>
                <tasks>
                    <copy todir="build/output/lib">
                        <fileset dir="lib"/>
                    </copy>
                </tasks>
            </configuration>
        </execution>
    </executions>
</plugin>
```

**結果**: Gradleの方が圧倒的に柔軟で簡単

### 5. **ローカルJARファイルの管理**

**Gradle:**
```gradle
dependencies {
    implementation fileTree(dir: 'lib', include: ['*.jar'])
    // または
    implementation files('lib/my-library.jar')
}
```

**Maven:**
```xml
<dependency>
    <groupId>local</groupId>
    <artifactId>my-library</artifactId>
    <version>1.0</version>
    <scope>system</scope>
    <systemPath>${project.basedir}/lib/my-library.jar</systemPath>
</dependency>
```

**結果**: Gradleの方がシンプル

### 6. **WebLogicへのデプロイ**

**Gradle:**
```gradle
plugins {
    id 'war'
}

task deployToWebLogic(type: Exec) {
    workingDir 'C:/Oracle/Middleware/wlserver/common/bin'
    commandLine 'cmd', '/c', 'wldeploy.cmd', 
                '-adminurl', 't3://localhost:7001',
                '-username', 'weblogic',
                '-password', 'password',
                '-deploy',
                '-name', 'myapp',
                file('build/libs/myapp.war').absolutePath
}
```

**Maven:**
```xml
<plugin>
    <groupId>com.oracle.weblogic</groupId>
    <artifactId>weblogic-maven-plugin</artifactId>
    <version>12.2.1-4-0</version>
    <configuration>
        <adminurl>t3://localhost:7001</adminurl>
        <user>weblogic</user>
        <password>password</password>
        <source>${project.build.directory}/${project.build.finalName}.war</source>
        <name>myapp</name>
    </configuration>
</plugin>
```

**結果**: どちらも可能だが、Gradleの方が柔軟に設定できる

## コマンド比較

### **基本コマンド**

| 操作 | Gradle | Maven |
|------|--------|-------|
| ビルド | `gradlew build` | `mvn compile` |
| クリーンビルド | `gradlew clean build` | `mvn clean install` |
| テスト | `gradlew test` | `mvn test` |
| パッケージング | `gradlew jar` / `gradlew war` | `mvn package` |
| 依存関係表示 | `gradlew dependencies` | `mvn dependency:tree` |
| タスク一覧 | `gradlew tasks` | `mvn help:describe -Dcmd=compile` |

### **マルチモジュール**

| 操作 | Gradle | Maven |
|------|--------|-------|
| 特定モジュールビルド | `gradlew :module1:build` | `mvn install -pl module1` |
| 依存モジュール含む | `gradlew :module2:build` | `mvn install -pl module2 -am` |

## Windows & VS Code での使いやすさ

### **Gradle**
- ✅ Gradle Wrapperで環境構築不要（`gradlew.bat`）
- ✅ VS Codeの「Gradle for Java」で完全統合
- ✅ Windowsパスの問題が少ない
- ✅ PowerShellでも問題なく動作

### **Maven**
- ✅ VS Codeの「Maven for Java」で統合可能
- ⚠️ 別途Mavenのインストールが必要な場合がある
- ✅ 安定した動作
- ✅ エンタープライズ環境での実績豊富

## どちらを選ぶべきか

### **Gradleを選ぶべき場合**
- ✅ 新規プロジェクト
- ✅ ビルド速度を重視
- ✅ 柔軟なカスタマイズが必要
- ✅ マルチモジュールの複雑な依存関係
- ✅ Android開発（Gradle必須）

### **Mavenを選ぶべき場合**
- ✅ 既存のMavenプロジェクトがある
- ✅ チーム全員がMavenに慣れている
- ✅ 規約重視・標準化重視
- ✅ 社内標準がMaven
- ✅ レガシーなエンタープライズ環境

## m-miyawakiさんの状況での推奨

既存のEclipseマルチモジュールプロジェクトで、VS Codeへの移行を考えている場合:

### **Gradleを推奨する理由:**
1. **VS Codeとの相性が良い**
2. **libディレクトリのJAR管理が簡単**
3. **ビルドが高速**（大規模プロジェクトほど効果大）
4. **WebLogicデプロイのカスタマイズが容易**
5. **Windows環境でのトラブルが少ない**

### **移行の難易度:**
- Eclipseプロジェクト → Gradle: 中程度（1〜2日）
- Eclipseプロジェクト → Maven: 中程度（1〜2日）

結果として、どちらも同程度の工数ですが、**長期的な保守性とビルド速度を考慮するとGradleが有利**です。

具体的な移行手順が必要であれば、現在のプロジェクト構成を教えていただければ詳しくご案内します。


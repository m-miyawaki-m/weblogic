# Rust Windows環境構築手順

## 目次

1. [概要](#1-概要)
2. [システム要件](#2-システム要件)
3. [インストール方法](#3-インストール方法)
4. [環境変数の確認](#4-環境変数の確認)
5. [インストールの確認](#5-インストールの確認)
6. [開発ツールのセットアップ](#6-開発ツールのセットアップ)
7. [トラブルシューティング](#7-トラブルシューティング)
8. [次のステップ](#8-次のステップ)

---

## 1. 概要

Rustは、メモリ安全性とパフォーマンスを両立するシステムプログラミング言語です。Windows環境でも簡単にインストール・使用できます。

**公式サイト**: [https://www.rust-lang.org/](https://www.rust-lang.org/)

**公式ドキュメント**: [https://doc.rust-lang.org/](https://doc.rust-lang.org/)

---

## 2. システム要件

### 2.1 最小要件

- **OS**: Windows 7以降（64ビット推奨）
- **メモリ**: 2GB以上（推奨: 4GB以上）
- **ディスク容量**: 約3GB（ツールチェーンとドキュメント含む）
- **インターネット接続**: インストール時に必要

### 2.2 必要なコンポーネント

- **Visual C++ Build Tools**: WindowsでRustをコンパイルするために必要
- **Git**: 一部のパッケージで必要（オプション）

---

## 3. インストール方法

### 3.1 方法1: rustup（推奨）

`rustup`はRustの公式インストーラーで、最も簡単な方法です。

#### ステップ1: rustup-init.exeをダウンロード

1. [https://rustup.rs/](https://rustup.rs/) にアクセス
2. 「Download rustup-init.exe」をクリック
3. ダウンロードした`rustup-init.exe`を実行

**直接ダウンロードリンク**: 
- 64ビット: [https://win.rustup.rs/x86_64](https://win.rustup.rs/x86_64)
- 32ビット: [https://win.rustup.rs/i686](https://win.rustup.rs/i686)

#### ステップ2: インストーラーを実行

1. ダウンロードした`rustup-init.exe`をダブルクリック
2. セキュリティ警告が表示された場合は「実行」をクリック
3. コマンドプロンプトが開き、インストールオプションが表示されます

```
Welcome to Rust!

This will download and install the official compiler for the Rust
programming language, and its package manager, Cargo.

Current installation options:

   default host triple: x86_64-pc-windows-msvc
     default toolchain: stable
   modify PATH variable: yes

1) Proceed with installation (default)
2) Customize installation
3) Cancel installation
```

4. **デフォルトの場合は「1」を入力してEnter**（推奨）
5. インストールが開始されます（数分かかることがあります）

#### ステップ3: Visual C++ Build Toolsのインストール

初回インストール時、Visual C++ Build Toolsが必要な場合があります：

1. インストーラーが自動的にダウンロードリンクを表示します
2. または、手動で以下からダウンロード:
   - [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
   - 「Build Tools for Visual Studio 2022」をダウンロード
3. インストーラーを実行し、「C++ build tools」ワークロードを選択
4. インストール完了後、再度`rustup-init.exe`を実行

### 3.2 方法2: Chocolateyを使用（オプション）

Chocolateyパッケージマネージャーを使用している場合：

```powershell
# ChocolateyでRustをインストール
choco install rust

# または
choco install rust-ms
```

**Chocolatey公式サイト**: [https://chocolatey.org/](https://chocolatey.org/)

### 3.3 方法3: Scoopを使用（オプション）

Scoopパッケージマネージャーを使用している場合：

```powershell
# ScoopでRustをインストール
scoop install rust
```

**Scoop公式サイト**: [https://scoop.sh/](https://scoop.sh/)

---

## 4. 環境変数の確認

インストール後、新しいコマンドプロンプトまたはPowerShellを開いて環境変数が正しく設定されているか確認します。

### 4.1 PATH環境変数

以下のパスが自動的に追加されます：

```
C:\Users\<ユーザー名>\.cargo\bin
```

### 4.2 手動でPATHを設定する場合

1. 「システムのプロパティ」→「環境変数」を開く
2. 「ユーザー環境変数」の「Path」を選択
3. 「編集」をクリック
4. 以下を追加:
   ```
   C:\Users\<ユーザー名>\.cargo\bin
   ```
5. 「OK」をクリックして保存

**注意**: 変更を反映するには、コマンドプロンプトやPowerShellを再起動する必要があります。

---

## 5. インストールの確認

### 5.1 基本的な確認

新しいコマンドプロンプトまたはPowerShellを開き、以下を実行：

```powershell
# Rustのバージョンを確認
rustc --version

# Cargoのバージョンを確認
cargo --version

# rustupのバージョンを確認
rustup --version
```

**期待される出力例**:
```
rustc 1.75.0 (82e1608df 2023-12-21)
cargo 1.75.0 (1d8b05cdd 2023-11-20)
rustup 1.26.0 (5af9b9484 2023-04-05)
```

### 5.2 ツールチェーンの確認

```powershell
# インストールされているツールチェーンを確認
rustup toolchain list

# デフォルトツールチェーンを確認
rustup default
```

### 5.3 ドキュメントの確認

```powershell
# ローカルのドキュメントを開く
rustup doc
```

ブラウザでRustの公式ドキュメントが開きます。

---

## 6. 開発ツールのセットアップ

### 6.1 Visual Studio Code（推奨）

#### 拡張機能のインストール

1. Visual Studio Codeを開く
2. 拡張機能タブ（Ctrl+Shift+X）を開く
3. 以下を検索してインストール:
   - **rust-analyzer**（推奨）: [https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer)
   - **CodeLLDB**（デバッガー）: [https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb)

#### rust-analyzerの設定

`settings.json`に以下を追加（推奨設定）:

```json
{
  "rust-analyzer.checkOnSave.command": "clippy",
  "rust-analyzer.inlayHints.typeHints.enable": true,
  "rust-analyzer.inlayHints.parameterHints.enable": true
}
```

**Visual Studio Code公式サイト**: [https://code.visualstudio.com/](https://code.visualstudio.com/)

### 6.2 IntelliJ IDEA / CLion

1. IntelliJ IDEAまたはCLionを開く
2. 「File」→「Settings」→「Plugins」
3. 「Rust」プラグインを検索してインストール
4. 再起動後、Rustプロジェクトを開く

**IntelliJ Rustプラグイン**: [https://plugins.jetbrains.com/plugin/8182-rust](https://plugins.jetbrains.com/plugin/8182-rust)

### 6.3 その他のエディタ

- **Sublime Text**: [LSP-rust-analyzer](https://packagecontrol.io/packages/LSP-rust-analyzer)
- **Vim/Neovim**: [rust-analyzer LSP](https://rust-analyzer.github.io/manual.html#vimneovim)
- **Emacs**: [rust-mode](https://github.com/rust-lang/rust-mode)

---

## 7. トラブルシューティング

### 7.1 「rustc が見つかりません」エラー

**原因**: PATH環境変数が正しく設定されていない

**解決方法**:
1. コマンドプロンプト/PowerShellを再起動
2. 環境変数を手動で設定（[4.2節](#42-手動でpathを設定する場合)を参照）
3. システムを再起動

### 7.2 「link.exe が見つかりません」エラー

**原因**: Visual C++ Build Toolsがインストールされていない

**解決方法**:
1. [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)をダウンロード
2. 「C++ build tools」ワークロードをインストール
3. 再起動後、再度試す

### 7.3 インストールが非常に遅い

**原因**: ネットワークの問題、または大量のダウンロード

**解決方法**:
1. インターネット接続を確認
2. プロキシを使用している場合は設定を確認
3. ミラーサイトを使用:
   ```powershell
   # 環境変数でミラーを設定
   $env:RUSTUP_DIST_SERVER="https://mirrors.ustc.edu.cn/rust-static"
   $env:RUSTUP_UPDATE_ROOT="https://mirrors.ustc.edu.cn/rust-static/rustup"
   ```

### 7.4 アンチウイルスソフトが警告を表示

**原因**: rustupがシステムを変更しようとしている

**解決方法**:
1. rustupを例外リストに追加
2. または、一時的にアンチウイルスを無効化してインストール

### 7.5 権限エラー

**原因**: 管理者権限が必要な操作を実行しようとしている

**解決方法**:
1. コマンドプロンプトを管理者として実行
2. または、ユーザー権限でインストール（推奨）

### 7.6 古いバージョンのRustが残っている

**原因**: 以前のインストールが残っている

**解決方法**:
```powershell
# 古いインストールを削除
rustup self uninstall

# 再インストール
rustup-init.exe
```

---

## 8. 次のステップ

### 8.1 最初のRustプログラム

```powershell
# 新しいプロジェクトを作成
cargo new hello_world
cd hello_world

# プログラムを実行
cargo run
```

### 8.2 学習リソース

- **The Rust Programming Language（日本語版）**: [https://doc.rust-jp.rs/book-ja/](https://doc.rust-jp.rs/book-ja/)
- **Rust by Example（日本語版）**: [https://doc.rust-jp.rs/rust-by-example-ja/](https://doc.rust-jp.rs/rust-by-example-ja/)
- **Rust公式ドキュメント**: [https://doc.rust-lang.org/](https://doc.rust-lang.org/)
- **Rustlings（実践的な演習）**: [https://github.com/rust-lang/rustlings](https://github.com/rust-lang/rustlings)

### 8.3 便利なコマンド

```powershell
# 新しいプロジェクトを作成
cargo new <project_name>

# プロジェクトをビルド
cargo build

# プロジェクトを実行
cargo run

# テストを実行
cargo test

# ドキュメントを生成
cargo doc --open

# コードをフォーマット
cargo fmt

# リンターを実行
cargo clippy

# 依存関係を更新
cargo update
```

### 8.4 ツールチェーンの管理

```powershell
# 利用可能なツールチェーンを一覧表示
rustup toolchain list

# 新しいツールチェーンをインストール
rustup toolchain install stable
rustup toolchain install nightly

# デフォルトツールチェーンを変更
rustup default stable
rustup default nightly

# 特定のプロジェクトでツールチェーンを指定
rustup override set nightly
```

### 8.5 コンポーネントの追加

```powershell
# rustfmt（コードフォーマッター）をインストール
rustup component add rustfmt

# clippy（リンター）をインストール
rustup component add clippy

# rust-docs（ドキュメント）をインストール
rustup component add rust-docs
```

---

## 9. 参考リンク

### 公式リソース

- **Rust公式サイト**: [https://www.rust-lang.org/](https://www.rust-lang.org/)
- **Rust公式ドキュメント**: [https://doc.rust-lang.org/](https://doc.rust-lang.org/)
- **rustup公式サイト**: [https://rustup.rs/](https://rustup.rs/)
- **Cargo公式ドキュメント**: [https://doc.rust-lang.org/cargo/](https://doc.rust-lang.org/cargo/)
- **Rust Playground**: [https://play.rust-lang.org/](https://play.rust-lang.org/)

### 日本語リソース

- **Rust日本語ドキュメント**: [https://doc.rust-jp.rs/](https://doc.rust-jp.rs/)
- **The Rust Programming Language（日本語版）**: [https://doc.rust-jp.rs/book-ja/](https://doc.rust-jp.rs/book-ja/)
- **Rust by Example（日本語版）**: [https://doc.rust-jp.rs/rust-by-example-ja/](https://doc.rust-jp.rs/rust-by-example-ja/)

### コミュニティ

- **Rust Users Forum**: [https://users.rust-lang.org/](https://users.rust-lang.org/)
- **Stack Overflow（Rustタグ）**: [https://stackoverflow.com/questions/tagged/rust](https://stackoverflow.com/questions/tagged/rust)
- **Reddit r/rust**: [https://www.reddit.com/r/rust/](https://www.reddit.com/r/rust/)
- **Rust Discord**: [https://discord.gg/rust-lang](https://discord.gg/rust-lang)

### ツールとライブラリ

- **crates.io（パッケージレジストリ）**: [https://crates.io/](https://crates.io/)
- **docs.rs（ドキュメント）**: [https://docs.rs/](https://docs.rs/)
- **rust-analyzer**: [https://rust-analyzer.github.io/](https://rust-analyzer.github.io/)

### Windows固有のリソース

- **Visual Studio Build Tools**: [https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
- **Windows Subsystem for Linux (WSL)**: [https://learn.microsoft.com/ja-jp/windows/wsl/](https://learn.microsoft.com/ja-jp/windows/wsl/)（WSL上でRustを使用する場合）

---

## 10. まとめ

### インストール手順の要約

1. ✅ [rustup.rs](https://rustup.rs/)から`rustup-init.exe`をダウンロード
2. ✅ インストーラーを実行（デフォルト設定でOK）
3. ✅ Visual C++ Build Toolsをインストール（必要に応じて）
4. ✅ 新しいコマンドプロンプト/PowerShellで`rustc --version`を確認
5. ✅ エディタにrust-analyzer拡張機能をインストール

### 確認コマンド

```powershell
# すべて正常に動作することを確認
rustc --version
cargo --version
rustup --version
```

### 次のアクション

- [The Rust Programming Language](https://doc.rust-jp.rs/book-ja/)を読む
- `cargo new hello_world`で最初のプロジェクトを作成
- [Rustlings](https://github.com/rust-lang/rustlings)で実践的な演習を行う

---

## 11. よくある質問（FAQ）

### Q1: Rustは無料ですか？

**A**: はい、Rustは完全に無料でオープンソースです。

### Q2: Windows 10/11で動作しますか？

**A**: はい、Windows 7以降で動作します。Windows 10/11で問題なく動作します。

### Q3: アンインストールする方法は？

**A**: 
```powershell
rustup self uninstall
```

### Q4: 複数のバージョンをインストールできますか？

**A**: はい、rustupで複数のツールチェーン（stable、nightly、beta）を管理できます。

### Q5: オフラインでインストールできますか？

**A**: 基本的にはインターネット接続が必要です。オフラインインストールは複雑なため、オンライン環境でのインストールを推奨します。

---

**最終更新日**: 2024年12月

**参考**: このドキュメントは公式ドキュメントを基に作成されています。最新情報は[公式サイト](https://www.rust-lang.org/)を確認してください。


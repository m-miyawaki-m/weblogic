# Rust関数抽出ツール 概要

## 実装可能性

はい、RustでもJavaScriptやJavaと同様の関数/メソッド抽出ツールを実装できます。Rustの構文特性を考慮した実装が必要です。

---

## Rustの関数/メソッド定義パターン

### 1. 通常の関数（Function）

```rust
fn function_name(param1: Type1, param2: Type2) -> ReturnType {
    // 関数本体
}
```

**例**:
```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn greet(name: &str) {
    println!("Hello, {}!", name);
}
```

---

### 2. パブリック関数（Public Function）

```rust
pub fn public_function() {
    // 関数本体
}
```

---

### 3. メソッド（Method - implブロック内）

```rust
impl StructName {
    fn method_name(&self) {
        // メソッド本体
    }
    
    fn method_with_params(&self, param: Type) -> ReturnType {
        // メソッド本体
    }
}
```

**例**:
```rust
struct User {
    name: String,
    age: u32,
}

impl User {
    fn new(name: String, age: u32) -> User {
        User { name, age }
    }
    
    fn get_name(&self) -> &str {
        &self.name
    }
    
    fn set_age(&mut self, age: u32) {
        self.age = age;
    }
}
```

---

### 4. 関連関数（Associated Function - 静的メソッドに相当）

```rust
impl StructName {
    fn associated_function() -> StructName {
        // 関連関数本体
    }
}
```

**例**:
```rust
impl User {
    fn create_default() -> User {
        User {
            name: String::from("Unknown"),
            age: 0,
        }
    }
}
```

---

### 5. トレイトメソッド（Trait Method）

```rust
trait TraitName {
    fn trait_method(&self);
    
    fn trait_method_with_default(&self) {
        // デフォルト実装
    }
}
```

**例**:
```rust
trait Drawable {
    fn draw(&self);
    
    fn describe(&self) {
        println!("This is a drawable object");
    }
}

impl Drawable for Circle {
    fn draw(&self) {
        println!("Drawing a circle");
    }
}
```

---

### 6. 非同期関数（Async Function）

```rust
async fn async_function() -> Result<Type, Error> {
    // 非同期処理
}
```

**例**:
```rust
async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;
    response.text().await
}
```

---

### 7. 不変関数（Const Function）

```rust
const fn const_function() -> i32 {
    42
}
```

---

### 8. 外部関数（Extern Function）

```rust
extern "C" fn extern_function() {
    // 外部関数本体
}
```

---

### 9. ジェネリック関数（Generic Function）

```rust
fn generic_function<T>(value: T) -> T {
    value
}

fn generic_with_bounds<T: Display>(value: T) {
    println!("{}", value);
}
```

---

### 10. クロージャ（Closure）

```rust
let closure = |x: i32| x + 1;
let closure_with_type = |x: i32| -> i32 { x * 2 };
```

**注意**: クロージャは変数に代入されるため、検出が難しい場合があります。

---

## Rust特有の構文要素

### ライフタイムパラメータ

```rust
fn function_with_lifetime<'a>(s: &'a str) -> &'a str {
    s
}
```

### トレイト境界

```rust
fn function_with_trait_bound<T: Clone + Display>(value: T) {
    // 関数本体
}
```

### where句

```rust
fn complex_generic<T, U>()
where
    T: Clone + Display,
    U: Copy + Debug,
{
    // 関数本体
}
```

---

## 実装時の考慮事項

### 1. 正規表現の複雑さ

Rustの構文は以下の理由で正規表現による抽出が複雑になります：

- **ライフタイムパラメータ**: `<'a>`, `<'a, 'b>`
- **ジェネリクス**: `<T>`, `<T: Trait>`, `<T, U>`
- **トレイト境界**: `T: Clone + Display`
- **where句**: 複雑な型制約
- **パターンマッチング**: 関数シグネチャ内での使用

### 2. 推奨される実装方法

#### 方法1: 正規表現ベース（簡易版）
- Python版と同様のアプローチ
- 基本的なパターンのみ検出
- 実装が簡単だが、複雑な構文には対応困難

#### 方法2: パーサーライブラリ使用（推奨）
- `syn`クレートを使用してRustコードをパース
- AST（抽象構文木）から正確に情報を抽出
- より正確だが、依存関係が増える

#### 方法3: rustcのASTを利用
- 最も正確だが、実装が複雑
- rustcの内部APIに依存

---

## 実装例（正規表現ベース）

### 基本的な関数パターン

```rust
use regex::Regex;

// 通常の関数
let pattern = Regex::new(r"fn\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^{]+))?\s*\{")?;

// パブリック関数
let pub_pattern = Regex::new(r"pub\s+fn\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^{]+))?\s*\{")?;

// implブロック内のメソッド
let impl_pattern = Regex::new(r"impl\s+[\w<>:]+(?:\s+for\s+[\w<>:]+)?\s*\{[^}]*fn\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^{]+))?\s*\{")?;
```

### 実装の課題

1. **ネストされた波括弧**: 正規表現では正確に処理が困難
2. **マクロ**: `#[derive(...)]`などのマクロは検出が困難
3. **属性**: `#[test]`, `#[allow(...)]`などの属性の処理
4. **ドキュメントコメント**: `///`や`//!`の処理

---

## 推奨実装アプローチ

### `syn`クレートを使用した実装

```rust
use syn::{File, Item, ItemFn, ItemImpl, ItemTrait};

fn extract_functions(content: &str) -> Vec<FunctionInfo> {
    let ast: File = syn::parse_file(content).unwrap();
    let mut functions = Vec::new();
    
    for item in ast.items {
        match item {
            Item::Fn(func) => {
                // 関数を抽出
                functions.push(extract_function_info(&func));
            }
            Item::Impl(impl_block) => {
                // implブロック内のメソッドを抽出
                for item in impl_block.items {
                    if let syn::ImplItem::Method(method) = item {
                        functions.push(extract_method_info(&method));
                    }
                }
            }
            Item::Trait(trait_def) => {
                // トレイトメソッドを抽出
                for item in trait_def.items {
                    if let syn::TraitItem::Method(method) = item {
                        functions.push(extract_trait_method_info(&method));
                    }
                }
            }
            _ => {}
        }
    }
    
    functions
}
```

### 利点

- ✅ 正確な構文解析
- ✅ ライフタイム、ジェネリクス、トレイト境界の正確な抽出
- ✅ マクロ展開前の情報も取得可能
- ✅ 属性情報の取得

### 欠点

- ❌ 依存関係の追加（`syn`クレート）
- ❌ コンパイル時間の増加
- ❌ より複雑な実装

---

## 検出可能な情報

### 関数情報

- 関数名
- 引数（型、名前、ライフタイム）
- 戻り値の型
- 可視性（`pub`, `pub(crate)`, `pub(super)`など）
- 属性（`#[test]`, `#[allow(...)]`など）
- ジェネリクス型パラメータ
- トレイト境界
- 行番号

### メソッド情報

- メソッド名
- レシーバー（`&self`, `&mut self`, `self`）
- 引数
- 戻り値の型
- 関連関数かメソッドか
- 実装先の型名

### トレイトメソッド情報

- メソッド名
- デフォルト実装の有無
- トレイト名
- 引数、戻り値の型

---

## 実装の優先順位

### Phase 1: 基本的な実装
1. 通常の関数（`fn`）
2. パブリック関数（`pub fn`）
3. implブロック内のメソッド

### Phase 2: 拡張機能
1. トレイトメソッド
2. 非同期関数
3. ジェネリック関数

### Phase 3: 高度な機能
1. ライフタイムパラメータの抽出
2. トレイト境界の抽出
3. 属性情報の抽出

---

## まとめ

Rustでも同様の関数/メソッド抽出ツールを実装できますが、以下の点に注意が必要です：

1. **構文の複雑さ**: ライフタイム、ジェネリクス、トレイト境界など
2. **実装方法の選択**: 正規表現（簡易） vs パーサーライブラリ（正確）
3. **パフォーマンス**: Rustの実装は高速だが、パーサー使用時はコンパイル時間が増加

**推奨**: `syn`クレートを使用した実装が最も正確で、将来の拡張にも対応しやすいです。



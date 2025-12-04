# PythonとJavaの概念・基本文法の比較

## 目次

1. [基本概念の比較](#1-基本概念の比較)
2. [データ型の比較](#2-データ型の比較)
3. [変数と定数の比較](#3-変数と定数の比較)
4. [制御構文の比較](#4-制御構文の比較)
5. [関数・メソッドの比較](#5-関数メソッドの比較)
6. [クラスとオブジェクトの比較](#6-クラスとオブジェクトの比較)
7. [エラーハンドリングの比較](#7-エラーハンドリングの比較)
8. [モジュール・パッケージの比較](#8-モジュールパッケージの比較)
9. [メモリ管理の比較](#9-メモリ管理の比較)
10. [実行環境の比較](#10-実行環境の比較)

---

## 1. 基本概念の比較

| 項目 | Python | Java |
|------|--------|------|
| **言語タイプ** | 動的型付け、インタプリタ型 | 静的型付け、コンパイル型 |
| **パラダイム** | オブジェクト指向、関数型、手続き型 | オブジェクト指向（純粋） |
| **実行方法** | インタプリタで直接実行 | コンパイルしてJVMで実行 |
| **コードの記述** | インデントでブロックを表現 | 波括弧`{}`でブロックを表現 |
| **セミコロン** | 不要（改行で文の終了） | 必須（文の終了を示す） |
| **コメント** | `#`（単一行）、`"""`（複数行） | `//`（単一行）、`/* */`（複数行） |
| **命名規則** | スネークケース（`snake_case`） | キャメルケース（`camelCase`） |
| **クラス名** | パスカルケース（`PascalCase`） | パスカルケース（`PascalCase`） |
| **定数** | 大文字スネークケース（`CONSTANT_NAME`） | 大文字スネークケース（`CONSTANT_NAME`） |

---

## 2. データ型の比較

| 項目 | Python | Java |
|------|--------|------|
| **型宣言** | 不要（動的型付け） | 必須（静的型付け） |
| **整数型** | `int`（任意精度） | `byte`, `short`, `int`, `long` |
| **浮動小数点型** | `float`, `complex` | `float`, `double` |
| **文字型** | `str`（文字列のみ） | `char`（1文字）、`String`（文字列） |
| **真偽型** | `bool`（`True`/`False`） | `boolean`（`true`/`false`） |
| **配列** | `list`, `tuple` | `[]`（配列）、`ArrayList`など |
| **辞書/マップ** | `dict` | `HashMap`, `TreeMap`など |
| **集合** | `set`, `frozenset` | `HashSet`, `TreeSet`など |
| **None/null** | `None` | `null` |
| **型チェック** | 実行時 | コンパイル時 |

### 型の例

**Python**:
```python
name = "Alice"  # 型宣言不要
age = 30
is_active = True
numbers = [1, 2, 3]
```

**Java**:
```java
String name = "Alice";  // 型宣言必須
int age = 30;
boolean isActive = true;
int[] numbers = {1, 2, 3};
```

---

## 3. 変数と定数の比較

| 項目 | Python | Java |
|------|--------|------|
| **変数宣言** | 代入時に自動宣言 | 明示的な宣言が必要 |
| **変数の型** | 動的（代入時に決定） | 静的（宣言時に決定） |
| **定数** | `CONSTANT_NAME = value`（慣習） | `final`キーワード |
| **可変性** | デフォルトで可変 | `final`で不変 |
| **スコープ** | 関数/クラス/グローバル | ブロック/メソッド/クラス |
| **グローバル変数** | `global`キーワード | `static`キーワード |

### 変数の例

**Python**:
```python
x = 10  # 変数宣言
x = 20  # 再代入可能

CONSTANT = 100  # 慣習的な定数

def func():
    global x  # グローバル変数へのアクセス
    x = 30
```

**Java**:
```java
int x = 10;  // 変数宣言
x = 20;      // 再代入可能

final int CONSTANT = 100;  // 定数（再代入不可）

static int globalVar = 50;  // クラス変数（グローバル相当）
```

---

## 4. 制御構文の比較

### 4.1 条件分岐

| 項目 | Python | Java |
|------|--------|------|
| **if文** | `if`, `elif`, `else` | `if`, `else if`, `else` |
| **三項演算子** | `x if condition else y` | `condition ? x : y` |
| **switch文** | `match`（Python 3.10+） | `switch`（`case`, `break`） |

**Python**:
```python
if x > 10:
    print("large")
elif x > 5:
    print("medium")
else:
    print("small")

result = "positive" if x > 0 else "negative"
```

**Java**:
```java
if (x > 10) {
    System.out.println("large");
} else if (x > 5) {
    System.out.println("medium");
} else {
    System.out.println("small");
}

String result = x > 0 ? "positive" : "negative";
```

### 4.2 ループ

| 項目 | Python | Java |
|------|--------|------|
| **for文** | `for item in iterable:` | `for (init; condition; increment)` |
| **拡張for文** | デフォルト | `for (Type item : collection)` |
| **while文** | `while condition:` | `while (condition)` |
| **do-while文** | なし | `do { } while (condition)` |
| **break/continue** | あり | あり |

**Python**:
```python
# for文
for i in range(10):
    print(i)

for item in [1, 2, 3]:
    print(item)

# while文
while x > 0:
    x -= 1
```

**Java**:
```java
// for文
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

// 拡張for文
for (int item : new int[]{1, 2, 3}) {
    System.out.println(item);
}

// while文
while (x > 0) {
    x--;
}
```

---

## 5. 関数・メソッドの比較

| 項目 | Python | Java |
|------|--------|------|
| **関数定義** | `def function_name():` | `returnType methodName()` |
| **戻り値** | `return`（型指定不要） | `return`（型必須） |
| **引数の型** | 型ヒント（オプション） | 型必須 |
| **デフォルト引数** | サポート | サポート（オーバーロードで代替） |
| **可変長引数** | `*args`, `**kwargs` | `Type... args` |
| **関数オブジェクト** | 第一級オブジェクト | ラムダ式、メソッド参照 |
| **ラムダ式** | `lambda x: x + 1` | `x -> x + 1` |
| **メソッド** | クラス内の関数 | クラス内のみ |

### 関数の例

**Python**:
```python
def add(a, b):
    return a + b

def greet(name="Guest"):
    return f"Hello, {name}"

def sum_all(*args):
    return sum(args)

# ラムダ式
square = lambda x: x * x
```

**Java**:
```java
public int add(int a, int b) {
    return a + b;
}

// デフォルト引数の代替（オーバーロード）
public String greet() {
    return greet("Guest");
}

public String greet(String name) {
    return "Hello, " + name;
}

// 可変長引数
public int sumAll(int... args) {
    int sum = 0;
    for (int arg : args) {
        sum += arg;
    }
    return sum;
}

// ラムダ式
Function<Integer, Integer> square = x -> x * x;
```

---

## 6. クラスとオブジェクトの比較

| 項目 | Python | Java |
|------|--------|------|
| **クラス定義** | `class ClassName:` | `class ClassName { }` |
| **コンストラクタ** | `__init__(self)` | `ClassName()` |
| **self/this** | `self`（明示的） | `this`（暗黙的） |
| **アクセス修飾子** | 慣習（`_`でプライベート） | `public`, `private`, `protected` |
| **継承** | `class Child(Parent):` | `class Child extends Parent` |
| **多重継承** | サポート | サポートしない（インターフェースで代替） |
| **インターフェース** | プロトコル（型ヒント） | `interface`（明示的） |
| **抽象クラス** | `ABC`モジュール | `abstract class` |
| **静的メソッド** | `@staticmethod` | `static` |
| **クラスメソッド** | `@classmethod` | なし（静的メソッドで代替） |
| **プロパティ** | `@property` | ゲッター/セッター |

### クラスの例

**Python**:
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self._age = age  # プライベート（慣習）
    
    def greet(self):
        return f"Hello, I'm {self.name}"
    
    @staticmethod
    def create_default():
        return Person("Unknown", 0)

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
```

**Java**:
```java
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public void greet() {
        System.out.println("Hello, I'm " + name);
    }
    
    public static Person createDefault() {
        return new Person("Unknown", 0);
    }
}

public class Student extends Person {
    private String studentId;
    
    public Student(String name, int age, String studentId) {
        super(name, age);
        this.studentId = studentId;
    }
}
```

---

## 7. エラーハンドリングの比較

| 項目 | Python | Java |
|------|--------|------|
| **例外処理** | `try`, `except`, `finally` | `try`, `catch`, `finally` |
| **例外の型** | 実行時チェック | コンパイル時チェック（チェック例外） |
| **例外の宣言** | 不要 | `throws`キーワード |
| **カスタム例外** | `class CustomError(Exception):` | `class CustomException extends Exception` |
| **例外の発生** | `raise Exception("message")` | `throw new Exception("message")` |
| **複数例外** | `except (Type1, Type2):` | `catch (Type1 | Type2 e)` |

### エラーハンドリングの例

**Python**:
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Division by zero")
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Cleanup")

# 例外の発生
raise ValueError("Invalid value")
```

**Java**:
```java
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Division by zero");
} catch (Exception e) {
    System.out.println("Error: " + e.getMessage());
} finally {
    System.out.println("Cleanup");
}

// 例外の発生
throw new IllegalArgumentException("Invalid value");

// 例外の宣言
public void method() throws IOException {
    // ...
}
```

---

## 8. モジュール・パッケージの比較

| 項目 | Python | Java |
|------|--------|------|
| **モジュール** | `.py`ファイル | `.java`ファイル |
| **パッケージ** | ディレクトリ構造 | `package`キーワード |
| **インポート** | `import module` | `import package.Class` |
| **名前空間** | モジュール名 | パッケージ名 |
| **標準ライブラリ** | 豊富（組み込み） | 豊富（JDK） |
| **依存管理** | `pip`, `requirements.txt` | `Maven`, `Gradle`, `pom.xml` |
| **仮想環境** | `venv`, `virtualenv` | なし（プロジェクト単位） |

### インポートの例

**Python**:
```python
import os
from collections import defaultdict
import numpy as np

# モジュールの実行
if __name__ == "__main__":
    print("Main module")
```

**Java**:
```java
import java.util.ArrayList;
import java.util.HashMap;
import static java.lang.Math.PI;

// パッケージ宣言
package com.example;

// メインメソッド
public static void main(String[] args) {
    System.out.println("Main method");
}
```

---

## 9. メモリ管理の比較

| 項目 | Python | Java |
|------|--------|------|
| **メモリ管理** | ガベージコレクション（参照カウント+循環参照検出） | ガベージコレクション（マーク&スイープ） |
| **メモリリーク** | まれ（循環参照に注意） | まれ（適切に実装すれば） |
| **メモリ効率** | やや低い（オーバーヘッド大） | やや高い（最適化されている） |
| **ポインタ** | なし（参照のみ） | なし（参照のみ） |
| **手動メモリ管理** | 不可能 | 不可能 |

---

## 10. 実行環境の比較

| 項目 | Python | Java |
|------|--------|------|
| **実行環境** | Pythonインタプリタ | JVM（Java Virtual Machine） |
| **コンパイル** | 不要（直接実行） | 必要（`.java` → `.class`） |
| **バイトコード** | `.pyc`（オプション） | `.class`（必須） |
| **プラットフォーム** | クロスプラットフォーム | クロスプラットフォーム（JVM上） |
| **起動速度** | 速い | やや遅い（JVM起動） |
| **実行速度** | やや遅い | 速い（JITコンパイル） |
| **デプロイ** | インタプリタ必要 | JRE必要（または単一JAR） |

---

## 11. その他の重要な違い

### 11.1 文字列処理

| 項目 | Python | Java |
|------|--------|------|
| **文字列の型** | `str`（不変） | `String`（不変） |
| **文字列結合** | `+`、`join()` | `+`、`StringBuilder` |
| **文字列フォーマット** | f-string、`.format()` | `String.format()`、`printf` |
| **生文字列** | `r"string"` | なし |

**Python**:
```python
name = "Alice"
message = f"Hello, {name}"  # f-string
message = "Hello, {}".format(name)  # format
```

**Java**:
```java
String name = "Alice";
String message = String.format("Hello, %s", name);
String message = "Hello, " + name;
```

### 11.2 コレクション

| 項目 | Python | Java |
|------|--------|------|
| **リスト** | `list`（可変） | `ArrayList`, `LinkedList` |
| **タプル** | `tuple`（不変） | なし（配列で代替） |
| **辞書** | `dict` | `HashMap`, `TreeMap` |
| **集合** | `set` | `HashSet`, `TreeSet` |
| **内包表記** | リスト内包、辞書内包 | Stream API（Java 8+） |

**Python**:
```python
# リスト内包
squares = [x**2 for x in range(10)]

# 辞書内包
squares_dict = {x: x**2 for x in range(10)}
```

**Java**:
```java
// Stream API
List<Integer> squares = IntStream.range(0, 10)
    .map(x -> x * x)
    .boxed()
    .collect(Collectors.toList());
```

### 11.3 デコレータ/アノテーション

| 項目 | Python | Java |
|------|--------|------|
| **デコレータ** | `@decorator` | `@Annotation` |
| **用途** | 関数/クラスの拡張 | メタデータ、設定 |
| **例** | `@property`, `@staticmethod` | `@Override`, `@Deprecated` |

---

## 12. まとめ

### Pythonの特徴
- ✅ シンプルで読みやすい構文
- ✅ 動的型付けで柔軟
- ✅ 豊富な標準ライブラリ
- ✅ 迅速な開発が可能
- ❌ 実行速度がやや遅い
- ❌ 型エラーが実行時まで発見されない

### Javaの特徴
- ✅ 静的型付けで安全性が高い
- ✅ コンパイル時にエラー検出
- ✅ 高い実行速度（JITコンパイル）
- ✅ エンタープライズ開発に適している
- ❌ 記述量が多い
- ❌ 学習曲線がやや急

### 使い分けの目安

**Pythonを選ぶ場合**:
- プロトタイピング、スクリプト、データ分析
- 機械学習、Web開発（Django、Flask）
- 小規模から中規模のプロジェクト

**Javaを選ぶ場合**:
- 大規模なエンタープライズアプリケーション
- 高いパフォーマンスが要求されるシステム
- 型安全性が重要なプロジェクト
- Androidアプリ開発


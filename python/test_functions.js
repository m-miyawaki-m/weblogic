// テスト用JavaScriptファイル - 様々な関数パターン

// ============================================
// 1. 通常の関数宣言（コメント付き）
// ============================================

/**
 * 通常の関数宣言のサンプル
 * @param {string} name - 名前
 * @param {number} age - 年齢
 * @returns {string} 挨拶メッセージ
 */
function greet(name, age) {
    return `こんにちは、${name}さん（${age}歳）`;
}

// 単一行コメント付き関数
// 引数なしの関数
function sayHello() {
    console.log("Hello");
}

// ============================================
// 2. 関数式
// ============================================

// 関数式（const）
const multiply = function(a, b) {
    return a * b;
};

// 関数式（let）
let divide = function(x, y) {
    return x / y;
};

// 関数式（var）
var subtract = function(a, b) {
    return a - b;
};

// ============================================
// 3. アロー関数
// ============================================

// アロー関数（const）
const add = (a, b) => {
    return a + b;
};

// アロー関数（let）
let square = (x) => {
    return x * x;
};

// アロー関数（var）
var cube = (x) => x * x * x;

// 引数なしのアロー関数
const getCurrentTime = () => {
    return new Date();
};

// ============================================
// 4. ES6メソッド定義（オブジェクト内）
// ============================================

const calculator = {
    // メソッド定義
    add(a, b) {
        return a + b;
    },
    
    // 通常のプロパティ
    name: "Calculator",
    
    // 別のメソッド
    subtract(x, y) {
        return x - y;
    }
};

// ============================================
// 5. デフォルト引数
// ============================================

/**
 * デフォルト引数を持つ関数
 */
function createUser(name, age = 18, city = "Tokyo") {
    return { name, age, city };
}

// デフォルト引数付きアロー関数
const greetWithDefault = (name, greeting = "Hello") => {
    return `${greeting}, ${name}!`;
};

// ============================================
// 6. 分割代入引数
// ============================================

// オブジェクトの分割代入
function processUser({ name, age, email }) {
    return `${name} (${age}): ${email}`;
}

// 配列の分割代入
function getFirstTwo([first, second]) {
    return { first, second };
}

// 分割代入とデフォルト値
function createProfile({ name = "Unknown", age = 0 } = {}) {
    return { name, age };
}

// ============================================
// 7. レストパラメータ
// ============================================

/**
 * レストパラメータを使用する関数
 * @param {...number} numbers - 数値のリスト
 */
function sum(...numbers) {
    return numbers.reduce((acc, n) => acc + n, 0);
}

// レストパラメータ付きアロー関数
const max = (...values) => {
    return Math.max(...values);
};

// ============================================
// 8. 非同期関数
// ============================================

// 非同期関数宣言
async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}

// 非同期アロー関数
const fetchUser = async (userId) => {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
};

// 非同期関数式
const loadData = async function(path) {
    const data = await import(path);
    return data;
};

// ============================================
// 9. ジェネレータ関数
// ============================================

/**
 * ジェネレータ関数
 * @param {number} start - 開始値
 * @param {number} end - 終了値
 */
function* numberRange(start, end) {
    for (let i = start; i <= end; i++) {
        yield i;
    }
}

// ジェネレータ関数式
const fibonacci = function* (n) {
    let a = 0, b = 1;
    for (let i = 0; i < n; i++) {
        yield a;
        [a, b] = [b, a + b];
    }
};

// ============================================
// 10. クラスメソッド
// ============================================

class User {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    // 通常のメソッド
    getName() {
        return this.name;
    }
    
    // メソッド（引数あり）
    setAge(newAge) {
        this.age = newAge;
    }
    
    // 静的メソッド
    static createAdmin() {
        return new User("Admin", 0);
    }
    
    // プライベートメソッド（ES2022）
    #privateMethod() {
        return "private";
    }
}

// ============================================
// 11. 複雑な引数パターン
// ============================================

// 複数の引数パターンの組み合わせ
function complexFunction(
    regularParam,
    { destructured, withDefault = "default" } = {},
    ...restParams
) {
    return { regularParam, destructured, withDefault, restParams };
}

// アロー関数での複雑な引数
const processData = async (
    id,
    { options = {}, callback = null } = {},
    ...additionalArgs
) => {
    // 処理
    return { id, options, callback, additionalArgs };
};

// ============================================
// 12. 即時実行関数（IIFE）
// ============================================

(function() {
    console.log("IIFE");
})();

(function(name) {
    console.log(`Hello, ${name}`);
})("World");

// ============================================
// 13. コールバック関数
// ============================================

function processArray(arr, callback) {
    return arr.map(callback);
}

// 使用例
processArray([1, 2, 3], function(x) {
    return x * 2;
});

// ============================================
// 14. ネストされた関数
// ============================================

function outerFunction(x) {
    function innerFunction(y) {
        return x + y;
    }
    return innerFunction;
}

// ============================================
// 15. 条件付き関数定義
// ============================================

if (true) {
    function conditionalFunction(param1, param2) {
        return param1 + param2;
    }
}

// ============================================
// 16. エクスポート付き関数（モジュール）
// ============================================

export function exportedFunction(a, b) {
    return a + b;
}

export const exportedArrow = (x) => x * 2;

export default function defaultExport(value) {
    return value;
}

// ============================================
// 17. 複数行コメントのパターン
// ============================================

/*
 * 複数行コメント付き関数
 * この関数は様々な処理を行います
 */
function multiLineCommentFunction(param1, param2, param3) {
    return param1 + param2 + param3;
}

// インラインコメント付き
function inlineCommentFunction(/* 引数1 */ arg1, /* 引数2 */ arg2) {
    return arg1 + arg2;
}

// ============================================
// 18. 特殊なケース
// ============================================

// Unicode文字を含む関数名
function 日本語関数名(引数1, 引数2) {
    return 引数1 + 引数2;
}

// アンダースコア付き関数名
function _private_function() {
    return "private";
}

// ドル記号付き関数名
function $jQueryFunction() {
    return "jQuery";
}


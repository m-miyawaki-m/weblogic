// テスト用Javaファイル - 様々なメソッドパターン

package com.example;

import java.util.List;
import java.util.Map;

/**
 * テスト用のクラス
 */
public class TestClass {
    private String name;
    private int age;
    
    // ============================================
    // 1. コンストラクタ
    // ============================================
    
    /**
     * デフォルトコンストラクタ
     */
    public TestClass() {
        this.name = "";
        this.age = 0;
    }
    
    /**
     * パラメータ付きコンストラクタ
     */
    public TestClass(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // ============================================
    // 2. 通常のメソッド
    // ============================================
    
    /**
     * パブリックメソッド
     */
    public String getName() {
        return name;
    }
    
    /**
     * プライベートメソッド
     */
    private void setName(String name) {
        this.name = name;
    }
    
    /**
     * 静的メソッド
     */
    public static void printMessage(String message) {
        System.out.println(message);
    }
    
    /**
     * 複数の修飾子を持つメソッド
     */
    public static final int calculateSum(int a, int b) {
        return a + b;
    }
    
    /**
     * 保護されたメソッド
     */
    protected void processData(String data) {
        // 処理
    }
    
    // ============================================
    // 3. 戻り値の型のバリエーション
    // ============================================
    
    /**
     * voidメソッド
     */
    public void doSomething() {
        System.out.println("Doing something");
    }
    
    /**
     * プリミティブ型を返すメソッド
     */
    public int getAge() {
        return age;
    }
    
    /**
     * オブジェクト型を返すメソッド
     */
    public String getFullName() {
        return name;
    }
    
    /**
     * 配列を返すメソッド
     */
    public int[] getNumbers() {
        return new int[]{1, 2, 3};
    }
    
    /**
     * ジェネリクス型を返すメソッド
     */
    public List<String> getItems() {
        return null;
    }
    
    /**
     * 複雑なジェネリクス型
     */
    public Map<String, List<Integer>> getComplexData() {
        return null;
    }
    
    // ============================================
    // 4. 引数のバリエーション
    // ============================================
    
    /**
     * 引数なしのメソッド
     */
    public void noParameters() {
        // 処理
    }
    
    /**
     * 単一引数のメソッド
     */
    public void singleParameter(String param) {
        // 処理
    }
    
    /**
     * 複数引数のメソッド
     */
    public void multipleParameters(String name, int age, boolean active) {
        // 処理
    }
    
    /**
     * 可変長引数
     */
    public void varArgs(String... args) {
        for (String arg : args) {
            System.out.println(arg);
        }
    }
    
    /**
     * ジェネリクス型の引数
     */
    public <T> void genericMethod(List<T> items) {
        // 処理
    }
    
    /**
     * 複雑な型の引数
     */
    public void complexParameters(Map<String, List<Integer>> data, String name) {
        // 処理
    }
    
    // ============================================
    // 5. 抽象メソッド（抽象クラス内）
    // ============================================
    
    /**
     * 抽象メソッド
     */
    public abstract void abstractMethod();
    
    // ============================================
    // 6. 同期化メソッド
    // ============================================
    
    /**
     * 同期化メソッド
     */
    public synchronized void synchronizedMethod() {
        // 処理
    }
    
    // ============================================
    // 7. ネイティブメソッド
    // ============================================
    
    /**
     * ネイティブメソッド
     */
    public native void nativeMethod();
    
    // ============================================
    // 8. finalメソッド
    // ============================================
    
    /**
     * finalメソッド
     */
    public final void finalMethod() {
        // 処理
    }
    
    // ============================================
    // 9. strictfpメソッド
    // ============================================
    
    /**
     * strictfpメソッド
     */
    public strictfp double strictfpMethod(double value) {
        return value * 2.0;
    }
    
    // ============================================
    // 10. メソッドチェーン
    // ============================================
    
    /**
     * メソッドチェーン用のメソッド
     */
    public TestClass setNameChain(String name) {
        this.name = name;
        return this;
    }
    
    public TestClass setAgeChain(int age) {
        this.age = age;
        return this;
    }
}


/**
 * インターフェースの例
 */
interface TestInterface {
    /**
     * インターフェースの通常のメソッド（実装なし）
     */
    void interfaceMethod();
    
    /**
     * デフォルトメソッド
     */
    default void defaultMethod() {
        System.out.println("Default implementation");
    }
    
    /**
     * 静的メソッド
     */
    static void staticMethod() {
        System.out.println("Static method");
    }
    
    /**
     * デフォルトメソッド（引数あり）
     */
    default String processString(String input) {
        return input.toUpperCase();
    }
}


/**
 * 抽象クラスの例
 */
abstract class AbstractTestClass {
    /**
     * 抽象メソッド
     */
    public abstract void abstractMethod();
    
    /**
     * 具象メソッド
     */
    public void concreteMethod() {
        System.out.println("Concrete method");
    }
    
    /**
     * 保護された抽象メソッド
     */
    protected abstract int calculate();
}


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Javaファイルからメソッドの名称、引数、ファイル名、行番号を取得するスクリプト
"""

import re
import sys
import csv
from typing import List, Dict
from pathlib import Path


class JavaMethodExtractor:
    """Javaファイルからメソッド情報を抽出するクラス"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = ""
        
    def read_file(self, raise_on_error: bool = True) -> None:
        """ファイルを読み込む"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except FileNotFoundError:
            error_msg = f"エラー: ファイル '{self.file_path}' が見つかりません。"
            if raise_on_error:
                print(error_msg)
                sys.exit(1)
            else:
                raise FileNotFoundError(error_msg)
        except Exception as e:
            error_msg = f"エラー: ファイルの読み込みに失敗しました: {e}"
            if raise_on_error:
                print(error_msg)
                sys.exit(1)
            else:
                raise
    
    def extract_methods(self) -> List[Dict[str, any]]:
        """メソッド定義を抽出"""
        methods = []
        
        # Javaの予約語・キーワード（メソッド名として誤検出しないように）
        java_keywords = {
            'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'default',
            'try', 'catch', 'finally', 'throw', 'return', 'break', 'continue',
            'class', 'interface', 'enum', 'extends', 'implements', 'super',
            'this', 'new', 'instanceof', 'import', 'package', 'static',
            'final', 'abstract', 'public', 'private', 'protected', 'void',
            'int', 'long', 'double', 'float', 'boolean', 'char', 'byte',
            'short', 'String', 'Object', 'null', 'true', 'false'
        }
        
        # クラス名を抽出（メソッドのコンテキストとして使用）
        class_match = re.search(r'class\s+(\w+)', self.content)
        class_name = class_match.group(1) if class_match else None
        
        # メソッド定義パターン
        # パターン1: 通常のメソッド定義
        # [修飾子] 戻り値の型 メソッド名(引数) { ... }
        # 修飾子は0個以上、戻り値の型は必須、メソッド名の後に(引数)が続く
        pattern1 = re.compile(
            r'(?:(?:public|private|protected|static|final|abstract|synchronized|native|strictfp)\s+)*'
            r'(void|[\w<>\[\]\s,\.]+?)\s+'  # 戻り値の型（void、ジェネリクス、配列対応）
            r'(\w+)\s*'  # メソッド名
            r'\(([^)]*)\)\s*\{',  # 引数と開始波括弧
            re.MULTILINE
        )
        
        # パターン2: コンストラクタ
        # [修飾子] クラス名(引数) { ... }
        pattern2 = re.compile(
            r'(?:(?:public|private|protected)\s+)?'
            r'(\w+)\s*'  # クラス名（コンストラクタ名）
            r'\(([^)]*)\)\s*\{',  # 引数と開始波括弧
            re.MULTILINE
        )
        
        # パターン3: インターフェースのメソッド（デフォルトメソッド、staticメソッド）
        # default 戻り値の型 メソッド名(引数) { ... }
        # static 戻り値の型 メソッド名(引数) { ... }
        pattern3 = re.compile(
            r'(?:default|static)\s+'
            r'(void|[\w<>\[\]\s,\.]+?)\s+'  # 戻り値の型
            r'(\w+)\s*'  # メソッド名
            r'\(([^)]*)\)\s*\{',  # 引数と開始波括弧
            re.MULTILINE
        )
        
        # パターンの順序を調整（コンストラクタとインターフェースメソッドを先に検出）
        patterns = [
            (pattern2, 'constructor'),  # コンストラクタを先に
            (pattern3, 'interface_method'),  # インターフェースメソッドを次に
            (pattern1, 'method')  # 通常のメソッドを最後に
        ]
        
        for pattern, method_type in patterns:
            for match in pattern.finditer(self.content):
                if method_type == 'constructor':
                    method_name = match.group(1)
                    params_str = match.group(2).strip()
                    return_type = None
                elif method_type == 'interface_method':
                    return_type_raw = match.group(1).strip()
                    method_name = match.group(2)
                    params_str = match.group(3).strip()
                else:  # method
                    return_type_raw = match.group(1).strip()
                    method_name = match.group(2)
                    params_str = match.group(3).strip()
                
                # 戻り値の型から修飾子を除去
                if method_type != 'constructor':
                    # 修飾子を除去
                    return_type = return_type_raw
                    for modifier in ['public', 'private', 'protected', 'static', 'final', 
                                    'abstract', 'synchronized', 'native', 'strictfp', 'default']:
                        # 単語境界で修飾子を除去
                        return_type = re.sub(r'\b' + modifier + r'\s+', '', return_type)
                    # ジェネリクス型パラメータを除去（<T> void -> void）
                    return_type = re.sub(r'^<[^>]+>\s+', '', return_type)
                    return_type = return_type.strip()
                else:
                    return_type = None
                
                # キーワードチェック
                if method_name in java_keywords:
                    continue
                
                # コンストラクタの場合はクラス名と一致するか確認
                if method_type == 'constructor':
                    if class_name and method_name != class_name:
                        continue
                
                # 前後の文字列を確認して、メソッド定義かどうかを判定
                start_pos = match.start()
                if start_pos > 0:
                    before_text = self.content[max(0, start_pos - 100):start_pos]
                    # メソッド定義の前には修飾子、型、または改行がある
                    # 波括弧の後にメソッド定義が来ることはない（メソッド呼び出しの可能性）
                    if re.search(r'\}\s*$', before_text):
                        continue
                    
                    # メソッド呼び出しの可能性をチェック（前が変数名やオブジェクト参照の場合）
                    if re.search(r'[a-zA-Z_]\w*\.\s*$', before_text):
                        continue
                    
                    # コンストラクタの場合はクラス名と一致する必要がある
                    if method_type == 'constructor':
                        if not class_name or method_name != class_name:
                            continue
                
                # 引数を解析
                params = []
                if params_str:
                    # 引数リストを解析（型 変数名, 型 変数名, ...）
                    # カンマで分割するが、ジェネリクス内のカンマは考慮しない簡易版
                    param_list = []
                    depth = 0
                    current_param = ""
                    
                    for char in params_str:
                        if char == '<':
                            depth += 1
                            current_param += char
                        elif char == '>':
                            depth -= 1
                            current_param += char
                        elif char == ',' and depth == 0:
                            if current_param.strip():
                                param_list.append(current_param.strip())
                            current_param = ""
                        else:
                            current_param += char
                    
                    if current_param.strip():
                        param_list.append(current_param.strip())
                    
                    for param in param_list:
                        if not param:
                            continue
                        # 型と変数名を分離（最後の単語が変数名、それ以前が型）
                        parts = param.strip().split()
                        if len(parts) >= 2:
                            # 型と変数名を結合（例: "String name" -> "String name"）
                            param_str = ' '.join(parts)
                            params.append(param_str)
                        elif len(parts) == 1:
                            # 型のみの場合（例: "String..."）
                            params.append(parts[0])
                
                # メソッド定義の行番号を取得
                line_num = self.content[:match.start()].count('\n') + 1
                
                # 修飾子を抽出
                modifiers = []
                method_start = match.start()
                # メソッド定義の前の部分を取得（最大200文字）
                method_context_start = max(0, method_start - 200)
                method_context = self.content[method_context_start:method_start]
                
                modifier_keywords = ['public', 'private', 'protected', 'static', 'final', 
                                    'abstract', 'synchronized', 'native', 'strictfp', 'default']
                for modifier in modifier_keywords:
                    if re.search(r'\b' + modifier + r'\b', method_context):
                        modifiers.append(modifier)
                
                methods.append({
                    'name': method_name,
                    'type': method_type,
                    'return_type': return_type or '',
                    'parameters': params,
                    'modifiers': ', '.join(modifiers) if modifiers else '',
                    'class_name': class_name or '',
                    'file': str(self.file_path),
                    'line': line_num
                })
        
        # 重複を除去（同じメソッドが複数のパターンでマッチする場合）
        # コンストラクタとインターフェースメソッドを優先
        seen = {}
        unique_methods = []
        # 型の優先順位: constructor > interface_method > method
        type_priority = {'constructor': 0, 'interface_method': 1, 'method': 2}
        
        for method in methods:
            key = (method['name'], method['line'])
            if key not in seen:
                seen[key] = len(unique_methods)
                unique_methods.append(method)
            else:
                # 既に存在する場合、優先度の高い方を保持
                existing_index = seen[key]
                existing = unique_methods[existing_index]
                if type_priority.get(method['type'], 99) < type_priority.get(existing['type'], 99):
                    unique_methods[existing_index] = method
        
        return unique_methods
    
    def extract(self, raise_on_error: bool = True) -> List[Dict[str, any]]:
        """メソッド情報を抽出して返す"""
        self.read_file(raise_on_error=raise_on_error)
        return self.extract_methods()
    
    def print_results(self, methods: List[Dict[str, any]]) -> None:
        """結果を整形して表示"""
        print(f"\n=== {self.file_path.name} ===\n")
        
        if not methods:
            print("メソッドが見つかりませんでした。")
            return
        
        for i, method in enumerate(methods, 1):
            print(f"【メソッド {i}】")
            print(f"  ファイル: {method['file']}")
            if method['class_name']:
                print(f"  クラス: {method['class_name']}")
            print(f"  名称: {method['name']}")
            print(f"  型: {method['type']}")
            if method['return_type']:
                print(f"  戻り値の型: {method['return_type']}")
            if method['modifiers']:
                print(f"  修飾子: {method['modifiers']}")
            print(f"  行番号: {method['line']}")
            
            if method['parameters']:
                print(f"  引数: {', '.join(method['parameters'])}")
            else:
                print(f"  引数: なし")
            
            print()
    
    def export_to_csv(self, methods: List[Dict[str, any]], output_file: str = None) -> None:
        """結果をCSV形式で出力"""
        if output_file is None:
            output_file = str(self.file_path.with_suffix('.csv'))
        
        if not methods:
            print("メソッドが見つかりませんでした。")
            return
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                # ヘッダー行
                writer.writerow(['ファイル', '行番号', 'クラス', '型', '修飾子', '戻り値の型', 'メソッド名', '引数'])
                
                # データ行
                for method in methods:
                    params_str = ', '.join(method['parameters']) if method['parameters'] else ''
                    writer.writerow([
                        method['file'],
                        method['line'],
                        method['class_name'],
                        method['type'],
                        method['modifiers'],
                        method['return_type'],
                        method['name'],
                        params_str
                    ])
            
            print(f"CSVファイルを出力しました: {output_file}")
        except Exception as e:
            print(f"エラー: CSVファイルの出力に失敗しました: {e}")
            sys.exit(1)


def read_file_list(list_csv_path: str) -> List[str]:
    """一覧CSVファイルからファイルパスのリストを読み込む（絶対パス対応）"""
    file_paths = []
    try:
        with open(list_csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            first_row = True
            for row in reader:
                if not row or not row[0].strip():
                    continue
                
                file_path = row[0].strip()
                
                # 最初の行がヘッダー行の可能性をチェック（"ファイル"、"ファイルパス"などのキーワード）
                if first_row:
                    header_keywords = ['ファイル', 'ファイルパス', 'file', 'filepath', 'path', 'ファイル名']
                    if file_path.lower() in [kw.lower() for kw in header_keywords]:
                        first_row = False
                        continue
                    first_row = False
                
                # 絶対パスの場合はそのまま使用
                if Path(file_path).is_absolute():
                    file_paths.append(file_path)
                else:
                    # 相対パスの場合は一覧CSVファイルのディレクトリ基準で解決
                    base_dir = Path(list_csv_path).parent
                    resolved_path = str(base_dir / file_path)
                    file_paths.append(resolved_path)
        
        return file_paths
    except FileNotFoundError:
        print(f"エラー: 一覧CSVファイル '{list_csv_path}' が見つかりません。")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: 一覧CSVファイルの読み込みに失敗しました: {e}")
        sys.exit(1)


def process_multiple_files(list_csv_path: str, output_file: str = None) -> None:
    """一覧CSVファイルに記載された複数ファイルを処理"""
    file_paths = read_file_list(list_csv_path)
    
    if not file_paths:
        print("一覧CSVファイルにファイルパスが記載されていません。")
        return
    
    print(f"処理対象ファイル数: {len(file_paths)}")
    
    all_methods = []
    processed_count = 0
    error_count = 0
    
    for file_path in file_paths:
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            print(f"警告: ファイルが見つかりません: {file_path}")
            error_count += 1
            continue
        
        if not file_path_obj.is_file():
            print(f"警告: ファイルではありません: {file_path}")
            error_count += 1
            continue
        
        try:
            extractor = JavaMethodExtractor(file_path)
            methods = extractor.extract(raise_on_error=False)
            all_methods.extend(methods)
            processed_count += 1
            print(f"処理完了: {file_path} ({len(methods)}個のメソッドを検出)")
        except Exception as e:
            print(f"エラー: {file_path} の処理に失敗しました: {e}")
            error_count += 1
            continue
    
    print(f"\n処理完了: {processed_count}ファイル, エラー: {error_count}ファイル")
    print(f"合計 {len(all_methods)}個のメソッドを検出しました。")
    
    # 結果をCSVに出力
    if output_file is None:
        output_file = str(Path(list_csv_path).with_suffix('')) + '_result.csv'
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            # ヘッダー行
            writer.writerow(['ファイル', '行番号', 'クラス', '型', '修飾子', '戻り値の型', 'メソッド名', '引数'])
            
            # データ行
            for method in all_methods:
                params_str = ', '.join(method['parameters']) if method['parameters'] else ''
                writer.writerow([
                    method['file'],
                    method['line'],
                    method['class_name'],
                    method['type'],
                    method['modifiers'],
                    method['return_type'],
                    method['name'],
                    params_str
                ])
        
        print(f"結果をCSVファイルに出力しました: {output_file}")
    except Exception as e:
        print(f"エラー: CSVファイルの出力に失敗しました: {e}")
        sys.exit(1)


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  単一ファイル: python search_java.py <javaファイルのパス> [--csv [出力ファイル名]] [--json]")
        print("  一覧CSV: python search_java.py --list <一覧CSVファイルのパス> [出力ファイル名]")
        print("")
        print("例:")
        print("  python search_java.py src/App.java")
        print("  python search_java.py src/App.java --csv")
        print("  python search_java.py src/App.java --csv output.csv")
        print("  python search_java.py src/App.java --json")
        print("  python search_java.py --list file_list.csv")
        print("  python search_java.py --list file_list.csv result.csv")
        sys.exit(1)
    
    # 一覧CSVモード
    if sys.argv[1] == '--list':
        if len(sys.argv) < 3:
            print("エラー: 一覧CSVファイルのパスを指定してください。")
            print("使用方法: python search_java.py --list <一覧CSVファイルのパス> [出力ファイル名]")
            sys.exit(1)
        
        list_csv_path = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        process_multiple_files(list_csv_path, output_file)
        return
    
    # 単一ファイルモード
    file_path = sys.argv[1]
    extractor = JavaMethodExtractor(file_path)
    methods = extractor.extract()
    
    # CSV形式で出力する場合
    if len(sys.argv) > 2 and sys.argv[2] == '--csv':
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        extractor.export_to_csv(methods, output_file)
    # JSON形式で出力する場合
    elif len(sys.argv) > 2 and sys.argv[2] == '--json':
        import json
        print("\n=== JSON形式 ===")
        print(json.dumps(methods, ensure_ascii=False, indent=2))
    # 通常の表示
    else:
        extractor.print_results(methods)


if __name__ == '__main__':
    main()


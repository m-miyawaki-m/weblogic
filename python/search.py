#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JavaScriptファイルから関数の名称、引数、ファイル名、行番号を取得するスクリプト
"""

import re
import sys
import csv
from typing import List, Dict
from pathlib import Path


class JavaScriptFunctionExtractor:
    """JavaScriptファイルから関数情報を抽出するクラス"""
    
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
    
    def extract_functions(self) -> List[Dict[str, any]]:
        """関数定義を抽出"""
        functions = []
        
        # JavaScriptの予約語・キーワード（関数名として誤検出しないように）
        js_keywords = {
            'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'default',
            'try', 'catch', 'finally', 'throw', 'return', 'break', 'continue',
            'var', 'let', 'const', 'function', 'class', 'extends', 'super',
            'this', 'new', 'typeof', 'instanceof', 'in', 'of', 'with',
            'import', 'export', 'from', 'as', 'default', 'static', 'async',
            'await', 'yield', 'constructor', 'get', 'set', 'delete', 'void'
        }
        
        # 関数宣言: function name(...) { ... }
        pattern1 = re.compile(
            r'function\s+(\w+)\s*\(([^)]*)\)',
            re.MULTILINE
        )
        
        # 非同期関数宣言: async function name(...) { ... }
        pattern1_async = re.compile(
            r'async\s+function\s+(\w+)\s*\(([^)]*)\)',
            re.MULTILINE
        )
        
        # ジェネレータ関数宣言: function* name(...) { ... }
        pattern1_gen = re.compile(
            r'function\s*\*\s*(\w+)\s*\(([^)]*)\)',
            re.MULTILINE
        )
        
        # 関数式: const/let/var name = function(...) { ... }
        pattern2 = re.compile(
            r'(?:const|let|var)\s+(\w+)\s*=\s*function\s*\(([^)]*)\)',
            re.MULTILINE
        )
        
        # 非同期関数式: const/let/var name = async function(...) { ... }
        pattern2_async = re.compile(
            r'(?:const|let|var)\s+(\w+)\s*=\s*async\s+function\s*\(([^)]*)\)',
            re.MULTILINE
        )
        
        # ジェネレータ関数式: const/let/var name = function*(...) { ... }
        pattern2_gen = re.compile(
            r'(?:const|let|var)\s+(\w+)\s*=\s*function\s*\*\s*\(([^)]*)\)',
            re.MULTILINE
        )
        
        # アロー関数: const/let/var name = (...) => { ... }
        pattern3 = re.compile(
            r'(?:const|let|var)\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>',
            re.MULTILINE
        )
        
        # 非同期アロー関数: const/let/var name = async (...) => { ... }
        pattern3_async = re.compile(
            r'(?:const|let|var)\s+(\w+)\s*=\s*async\s+\(([^)]*)\)\s*=>',
            re.MULTILINE
        )
        
        # メソッド定義: name(...) { ... } (ES6) - キーワードを除外
        # オブジェクトリテラルやクラス内のメソッドを検出
        pattern4 = re.compile(
            r'(\w+)\s*\(([^)]*)\)\s*\{',
            re.MULTILINE
        )
        
        patterns = [
            (pattern1_async, 'async_function'),
            (pattern1_gen, 'generator_function'),
            (pattern1, 'function'),
            (pattern2_async, 'async_function_expression'),
            (pattern2_gen, 'generator_function_expression'),
            (pattern2, 'function_expression'),
            (pattern3_async, 'async_arrow_function'),
            (pattern3, 'arrow_function'),
            (pattern4, 'method')
        ]
        
        for pattern, func_type in patterns:
            for match in pattern.finditer(self.content):
                func_name = match.group(1)
                params_str = match.group(2).strip()
                
                # メソッドパターンの場合、キーワードを除外
                if func_type == 'method':
                    if func_name in js_keywords:
                        continue
                    # 前の文字を確認して、オブジェクトやクラスのメソッドかどうかを判定
                    start_pos = match.start()
                    if start_pos > 0:
                        before_text = self.content[max(0, start_pos - 20):start_pos]
                        # オブジェクトリテラルやクラス内のメソッドのパターンを確認
                        # 前が空白、カンマ、セミコロン、波括弧、コロン、改行など
                        if not re.search(r'[,\s{;:\n]\s*$', before_text):
                            continue
                
                # 引数を解析
                params = []
                if params_str:
                    # デフォルト引数や分割代入を考慮して解析
                    param_list = [p.strip() for p in params_str.split(',')]
                    for param in param_list:
                        if not param:
                            continue
                        # デフォルト引数から変数名を抽出
                        param_name = param.split('=')[0].strip()
                        # 分割代入から変数名を抽出（簡易版）
                        if '{' in param_name or '[' in param_name:
                            # 分割代入の場合はそのまま保持
                            params.append(param_name)
                        else:
                            # 通常の引数
                            params.append(param_name)
                
                # 関数定義の行番号を取得
                line_num = self.content[:match.start()].count('\n') + 1
                
                functions.append({
                    'name': func_name,
                    'type': func_type,
                    'parameters': params,
                    'file': str(self.file_path),
                    'line': line_num
                })
        
        # 重複を除去（同じ関数が複数のパターンでマッチする場合）
        seen = set()
        unique_functions = []
        for func in functions:
            key = (func['name'], func['line'])
            if key not in seen:
                seen.add(key)
                unique_functions.append(func)
        
        return unique_functions
    
    def extract(self, raise_on_error: bool = True) -> List[Dict[str, any]]:
        """関数情報を抽出して返す"""
        self.read_file(raise_on_error=raise_on_error)
        return self.extract_functions()
    
    def print_results(self, functions: List[Dict[str, any]]) -> None:
        """結果を整形して表示"""
        print(f"\n=== {self.file_path.name} ===\n")
        
        if not functions:
            print("関数が見つかりませんでした。")
            return
        
        for i, func in enumerate(functions, 1):
            print(f"【関数 {i}】")
            print(f"  ファイル: {func['file']}")
            print(f"  名称: {func['name']}")
            print(f"  型: {func['type']}")
            print(f"  行番号: {func['line']}")
            
            if func['parameters']:
                print(f"  引数: {', '.join(func['parameters'])}")
            else:
                print(f"  引数: なし")
            
            print()
    
    def export_to_csv(self, functions: List[Dict[str, any]], output_file: str = None) -> None:
        """結果をCSV形式で出力"""
        if output_file is None:
            output_file = str(self.file_path.with_suffix('.csv'))
        
        if not functions:
            print("関数が見つかりませんでした。")
            return
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                # ヘッダー行
                writer.writerow(['ファイル', '行番号', '型', '関数名', '引数'])
                
                # データ行
                for func in functions:
                    params_str = ', '.join(func['parameters']) if func['parameters'] else ''
                    writer.writerow([
                        func['file'],
                        func['line'],
                        func['type'],
                        func['name'],
                        params_str
                    ])
            
            print(f"CSVファイルを出力しました: {output_file}")
        except Exception as e:
            print(f"エラー: CSVファイルの出力に失敗しました: {e}")
            sys.exit(1)


def read_file_list(list_csv_path: str) -> List[str]:
    """一覧CSVファイルからファイルパスのリストを読み込む"""
    file_paths = []
    try:
        with open(list_csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip():  # 1列目が空でない場合
                    file_path = row[0].strip()
                    # 絶対パスに変換
                    if not Path(file_path).is_absolute():
                        # 相対パスの場合は一覧CSVファイルのディレクトリ基準で解決
                        base_dir = Path(list_csv_path).parent
                        file_path = str(base_dir / file_path)
                    file_paths.append(file_path)
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
    
    all_functions = []
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
            extractor = JavaScriptFunctionExtractor(file_path)
            functions = extractor.extract(raise_on_error=False)
            all_functions.extend(functions)
            processed_count += 1
            print(f"処理完了: {file_path} ({len(functions)}個の関数を検出)")
        except Exception as e:
            print(f"エラー: {file_path} の処理に失敗しました: {e}")
            error_count += 1
            continue
    
    print(f"\n処理完了: {processed_count}ファイル, エラー: {error_count}ファイル")
    print(f"合計 {len(all_functions)}個の関数を検出しました。")
    
    # 結果をCSVに出力
    if output_file is None:
        output_file = str(Path(list_csv_path).with_suffix('')) + '_result.csv'
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            # ヘッダー行
            writer.writerow(['ファイル', '行番号', '型', '関数名', '引数'])
            
            # データ行
            for func in all_functions:
                params_str = ', '.join(func['parameters']) if func['parameters'] else ''
                writer.writerow([
                    func['file'],
                    func['line'],
                    func['type'],
                    func['name'],
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
        print("  単一ファイル: python search.py <jsファイルのパス> [--csv [出力ファイル名]] [--json]")
        print("  一覧CSV: python search.py --list <一覧CSVファイルのパス> [出力ファイル名]")
        print("")
        print("例:")
        print("  python search.py src/app.js")
        print("  python search.py src/app.js --csv")
        print("  python search.py src/app.js --csv output.csv")
        print("  python search.py src/app.js --json")
        print("  python search.py --list file_list.csv")
        print("  python search.py --list file_list.csv result.csv")
        sys.exit(1)
    
    # 一覧CSVモード
    if sys.argv[1] == '--list':
        if len(sys.argv) < 3:
            print("エラー: 一覧CSVファイルのパスを指定してください。")
            print("使用方法: python search.py --list <一覧CSVファイルのパス> [出力ファイル名]")
            sys.exit(1)
        
        list_csv_path = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        process_multiple_files(list_csv_path, output_file)
        return
    
    # 単一ファイルモード
    file_path = sys.argv[1]
    extractor = JavaScriptFunctionExtractor(file_path)
    functions = extractor.extract()
    
    # CSV形式で出力する場合
    if len(sys.argv) > 2 and sys.argv[2] == '--csv':
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        extractor.export_to_csv(functions, output_file)
    # JSON形式で出力する場合
    elif len(sys.argv) > 2 and sys.argv[2] == '--json':
        import json
        print("\n=== JSON形式 ===")
        print(json.dumps(functions, ensure_ascii=False, indent=2))
    # 通常の表示
    else:
        extractor.print_results(functions)


if __name__ == '__main__':
    main()


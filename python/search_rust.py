#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rustファイルから関数の名称、引数、ファイル名、行番号を取得するスクリプト
"""

import re
import sys
import csv
from typing import List, Dict
from pathlib import Path


class RustFunctionExtractor:
    """Rustファイルから関数情報を抽出するクラス"""
    
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
        
        # Rustの予約語・キーワード（関数名として誤検出しないように）
        rust_keywords = {
            'if', 'else', 'for', 'while', 'loop', 'match', 'if let', 'while let',
            'let', 'mut', 'const', 'static', 'fn', 'struct', 'enum', 'impl',
            'trait', 'mod', 'use', 'pub', 'self', 'Self', 'super', 'crate',
            'return', 'break', 'continue', 'async', 'await', 'move', 'ref',
            'true', 'false', 'Some', 'None', 'Ok', 'Err', 'Box', 'Vec', 'String'
        }
        
        # 構造体名、トレイト名、impl対象の型名を抽出
        struct_match = re.search(r'struct\s+(\w+)', self.content)
        struct_name = struct_match.group(1) if struct_match else None
        
        trait_match = re.search(r'trait\s+(\w+)', self.content)
        trait_name = trait_match.group(1) if trait_match else None
        
        # implブロックの対象型を抽出（簡易版）
        impl_matches = re.finditer(r'impl\s+(?:([\w<>:]+)\s+for\s+)?([\w<>:]+)', self.content)
        impl_types = []
        for match in impl_matches:
            impl_type = match.group(2) if match.group(2) else match.group(1)
            if impl_type:
                impl_types.append(impl_type.split('<')[0])  # ジェネリクス除去
        
        # パターン1: 通常の関数（pub fn または fn）
        pattern1 = re.compile(
            r'(?:pub\s+(?:\([^)]+\)\s+)?)?fn\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^{]+?))?\s*\{',
            re.MULTILINE
        )
        
        # パターン2: implブロック内のメソッド
        pattern2 = re.compile(
            r'fn\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^{]+?))?\s*\{',
            re.MULTILINE
        )
        
        # パターン3: トレイトメソッド（デフォルト実装あり）
        pattern3 = re.compile(
            r'fn\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^{]+?))?\s*\{',
            re.MULTILINE
        )
        
        # パターン4: 非同期関数
        pattern4 = re.compile(
            r'(?:pub\s+(?:\([^)]+\)\s+)?)?async\s+fn\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^{]+?))?\s*\{',
            re.MULTILINE
        )
        
        # パターン5: 不変関数
        pattern5 = re.compile(
            r'(?:pub\s+(?:\([^)]+\)\s+)?)?const\s+fn\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^{]+?))?\s*\{',
            re.MULTILINE
        )
        
        # パターン6: 外部関数
        pattern6 = re.compile(
            r'extern\s+"[^"]+"\s+fn\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^{]+?))?\s*\{',
            re.MULTILINE
        )
        
        patterns = [
            (pattern4, 'async_function'),
            (pattern5, 'const_function'),
            (pattern6, 'extern_function'),
            (pattern1, 'function'),
            (pattern2, 'method'),
            (pattern3, 'trait_method')
        ]
        
        for pattern, func_type in patterns:
            for match in pattern.finditer(self.content):
                func_name = match.group(1)
                params_str = match.group(2).strip()
                return_type = match.group(3).strip() if match.group(3) else None
                
                # キーワードチェック
                if func_name in rust_keywords:
                    continue
                
                # 前後の文字列を確認して、関数定義かどうかを判定
                start_pos = match.start()
                if start_pos > 0:
                    before_text = self.content[max(0, start_pos - 100):start_pos]
                    
                    # implブロック内かどうかを確認
                    is_in_impl = False
                    is_in_trait = False
                    
                    # implブロック内のメソッドかどうか
                    if func_type == 'method':
                        # 前のimplブロックを探す
                        impl_start = self.content.rfind('impl', 0, start_pos)
                        if impl_start != -1:
                            impl_end = self.content.find('}', impl_start, start_pos)
                            if impl_end == -1 or impl_end > start_pos:
                                is_in_impl = True
                    
                    # トレイト内のメソッドかどうか
                    if func_type == 'trait_method':
                        trait_start = self.content.rfind('trait', 0, start_pos)
                        if trait_start != -1:
                            trait_end = self.content.find('}', trait_start, start_pos)
                            if trait_end == -1 or trait_end > start_pos:
                                is_in_trait = True
                    
                    # 関数呼び出しの可能性をチェック
                    if re.search(r'[a-zA-Z_]\w*\.\s*$', before_text):
                        continue
                    
                    # マクロ呼び出しの可能性をチェック
                    if re.search(r'!\s*$', before_text):
                        continue
                
                # 引数を解析
                params = []
                if params_str:
                    # Rustの引数は "name: Type" の形式
                    # セルフ参照（&self, &mut self, self）を特別に処理
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
                        # 型と変数名を分離（"name: Type" または "&self" など）
                        param = param.strip()
                        if ':' in param:
                            parts = param.split(':', 1)
                            param_str = parts[0].strip() + ': ' + parts[1].strip()
                            params.append(param_str)
                        else:
                            # セルフ参照など
                            params.append(param)
                
                # 関数定義の行番号を取得
                line_num = self.content[:match.start()].count('\n') + 1
                
                # 可視性を抽出
                visibility = ''
                func_start = match.start()
                func_context_start = max(0, func_start - 200)
                func_context = self.content[func_context_start:func_start]
                
                if re.search(r'\bpub\s+(?:\([^)]+\)\s+)?fn\b', func_context):
                    if re.search(r'pub\s*\([^)]+\)', func_context):
                        # pub(crate) などの形式
                        pub_match = re.search(r'pub\s*\(([^)]+)\)', func_context)
                        if pub_match:
                            visibility = f"pub({pub_match.group(1)})"
                        else:
                            visibility = 'pub'
                    else:
                        visibility = 'pub'
                
                # 構造体名またはトレイト名を取得
                struct_or_trait = None
                if is_in_impl:
                    # 最も近いimplブロックの型名を取得
                    impl_start = self.content.rfind('impl', 0, start_pos)
                    if impl_start != -1:
                        impl_text = self.content[impl_start:start_pos]
                        impl_type_match = re.search(r'impl\s+(?:([\w<>:]+)\s+for\s+)?([\w<>:]+)', impl_text)
                        if impl_type_match:
                            struct_or_trait = impl_type_match.group(2) or impl_type_match.group(1)
                            if struct_or_trait:
                                struct_or_trait = struct_or_trait.split('<')[0]
                
                if is_in_trait and trait_name:
                    struct_or_trait = trait_name
                
                functions.append({
                    'name': func_name,
                    'type': func_type,
                    'return_type': return_type or '',
                    'parameters': params,
                    'visibility': visibility,
                    'struct_or_trait': struct_or_trait or '',
                    'file': str(self.file_path),
                    'line': line_num
                })
        
        # 重複を除去（同じ関数が複数のパターンでマッチする場合）
        seen = {}
        unique_functions = []
        type_priority = {
            'async_function': 0,
            'const_function': 1,
            'extern_function': 2,
            'function': 3,
            'method': 4,
            'trait_method': 5
        }
        
        for func in functions:
            key = (func['name'], func['line'])
            if key not in seen:
                seen[key] = len(unique_functions)
                unique_functions.append(func)
            else:
                existing_index = seen[key]
                existing = unique_functions[existing_index]
                if type_priority.get(func['type'], 99) < type_priority.get(existing['type'], 99):
                    unique_functions[existing_index] = func
        
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
            if func['struct_or_trait']:
                print(f"  構造体/トレイト: {func['struct_or_trait']}")
            print(f"  名称: {func['name']}")
            print(f"  型: {func['type']}")
            if func['return_type']:
                print(f"  戻り値の型: {func['return_type']}")
            if func['visibility']:
                print(f"  可視性: {func['visibility']}")
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
                writer.writerow(['ファイル', '行番号', '構造体/トレイト', '型', '可視性', '戻り値の型', '関数名', '引数'])
                
                # データ行
                for func in functions:
                    params_str = ', '.join(func['parameters']) if func['parameters'] else ''
                    writer.writerow([
                        func['file'],
                        func['line'],
                        func['struct_or_trait'],
                        func['type'],
                        func['visibility'],
                        func['return_type'],
                        func['name'],
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
                
                # 最初の行がヘッダー行の可能性をチェック
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
            extractor = RustFunctionExtractor(file_path)
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
            writer.writerow(['ファイル', '行番号', '構造体/トレイト', '型', '可視性', '戻り値の型', '関数名', '引数'])
            
            # データ行
            for func in all_functions:
                params_str = ', '.join(func['parameters']) if func['parameters'] else ''
                writer.writerow([
                    func['file'],
                    func['line'],
                    func['struct_or_trait'],
                    func['type'],
                    func['visibility'],
                    func['return_type'],
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
        print("  単一ファイル: python search_rust.py <rustファイルのパス> [--csv [出力ファイル名]] [--json]")
        print("  一覧CSV: python search_rust.py --list <一覧CSVファイルのパス> [出力ファイル名]")
        print("")
        print("例:")
        print("  python search_rust.py src/main.rs")
        print("  python search_rust.py src/main.rs --csv")
        print("  python search_rust.py src/main.rs --csv output.csv")
        print("  python search_rust.py src/main.rs --json")
        print("  python search_rust.py --list file_list.csv")
        print("  python search_rust.py --list file_list.csv result.csv")
        sys.exit(1)
    
    # 一覧CSVモード
    if sys.argv[1] == '--list':
        if len(sys.argv) < 3:
            print("エラー: 一覧CSVファイルのパスを指定してください。")
            print("使用方法: python search_rust.py --list <一覧CSVファイルのパス> [出力ファイル名]")
            sys.exit(1)
        
        list_csv_path = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        process_multiple_files(list_csv_path, output_file)
        return
    
    # 単一ファイルモード
    file_path = sys.argv[1]
    extractor = RustFunctionExtractor(file_path)
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



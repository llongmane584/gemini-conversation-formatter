#!/usr/bin/env python3
"""
Gemini会話HTMLからMarkdown変換ツール

使用方法:
    python main.py input.html [output.md]
    python main.py examples/*.html --batch
"""

import argparse
import os
import sys
from pathlib import Path
import glob

from gemini_parser import GeminiConversationParser
from markdown_formatter import MarkdownFormatter


def process_single_file(input_path: str, output_path: str = None) -> bool:
    """
    単一のHTMLファイルを処理
    
    Args:
        input_path: 入力HTMLファイルのパス
        output_path: 出力Markdownファイルのパス（省略時は自動生成）
        
    Returns:
        処理が成功したかどうか
    """
    try:
        # パーサーとフォーマッターを初期化
        parser = GeminiConversationParser()
        formatter = MarkdownFormatter()
        
        # HTMLファイルをパース
        print(f"処理中: {input_path}")
        conversations = parser.parse_html_file(input_path)
        
        if not conversations:
            print(f"警告: {input_path} から会話が見つかりませんでした")
            return False
        
        print(f"抽出した会話数: {len(conversations)}")
        
        # 出力ファイル名を決定
        if not output_path:
            input_file = Path(input_path)
            output_path = input_file.parent / f"{input_file.stem}.md"
        
        # ファイル名からタイトルを生成
        title = Path(input_path).stem.replace('-', ' ').replace('_', ' ').title()
        
        # Markdownに変換
        markdown_content = formatter.format_conversations(conversations, title)
        
        # ファイルに保存
        formatter.save_to_file(markdown_content, output_path)
        
        return True
        
    except Exception as e:
        print(f"エラー: {input_path} の処理中にエラーが発生しました: {e}")
        return False


def process_batch(pattern: str, output_dir: str = None) -> None:
    """
    複数のHTMLファイルをバッチ処理
    
    Args:
        pattern: ファイルパターン（例: examples/*.html）
        output_dir: 出力ディレクトリ（省略時は各ファイルと同じディレクトリ）
    """
    files = glob.glob(pattern)
    
    if not files:
        print(f"パターンにマッチするファイルが見つかりません: {pattern}")
        return
    
    print(f"バッチ処理: {len(files)}個のファイルを処理します")
    
    success_count = 0
    
    for file_path in files:
        if output_dir:
            output_path = os.path.join(output_dir, Path(file_path).stem + '.md')
        else:
            output_path = None
            
        if process_single_file(file_path, output_path):
            success_count += 1
    
    print(f"バッチ処理完了: {success_count}/{len(files)}個のファイルが正常に処理されました")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="Gemini会話HTMLファイルをMarkdown形式に変換します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python main.py examples/hair-density.html
  python main.py examples/hair-density.html output.md
  python main.py "examples/*.html" --batch
  python main.py "examples/*.html" --batch --output-dir converted/
        """
    )
    
    parser.add_argument('input', help='入力HTMLファイル（または--batchの場合はパターン）')
    parser.add_argument('output', nargs='?', help='出力Markdownファイル（省略可）')
    parser.add_argument('--batch', action='store_true', help='複数ファイルをバッチ処理')
    parser.add_argument('--output-dir', help='バッチ処理時の出力ディレクトリ')
    
    args = parser.parse_args()
    
    # 入力ファイル/パターンの存在確認
    if not args.batch and not os.path.exists(args.input):
        print(f"エラー: 入力ファイルが見つかりません: {args.input}")
        sys.exit(1)
    
    try:
        if args.batch:
            # バッチ処理
            if args.output_dir and not os.path.exists(args.output_dir):
                os.makedirs(args.output_dir)
                print(f"出力ディレクトリを作成しました: {args.output_dir}")
            
            process_batch(args.input, args.output_dir)
        else:
            # 単一ファイル処理
            success = process_single_file(args.input, args.output)
            if not success:
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n処理が中断されました")
        sys.exit(1)
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

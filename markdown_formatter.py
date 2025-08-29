"""
Markdownフォーマッター

会話データをMarkdown形式に変換する
"""

from typing import List, Dict


class MarkdownFormatter:
    """会話をMarkdown形式にフォーマットするクラス"""
    
    def __init__(self):
        pass

    def _improve_code_blocks(self, text: str) -> str:
        """
        コードブロック（```）前後に改行を追加してMarkdownビューワーでの見やすさを改善
        
        Args:
            text: 処理対象のテキスト
            
        Returns:
            改善されたテキスト
        """
        # 単純で確実なアプローチ：文字列の置換
        result = text
        
        # バッククォート3つを見つけて前後に改行を追加
        import re
        
        # ```の前に文字がある場合（改行以外）、改行を追加
        result = re.sub(r'([^\n])```', r'\1\n```', result)
        
        # ```の後に文字がある場合（改行以外）、改行を追加  
        result = re.sub(r'```([^\n])', r'```\n\1', result)
        
        # 連続する改行を整理（3個以上の連続改行を2個に）
        result = re.sub(r'\n{3,}', r'\n\n', result)
        
        return result
    
    def format_conversations(self, conversations: List[Dict[str, str]], title: str = "Gemini会話") -> str:
        """
        会話リストをMarkdown形式に変換
        
        Args:
            conversations: 会話のリスト
            title: ドキュメントのタイトル
            
        Returns:
            Markdown形式の文字列
        """
        if not conversations:
            return f"# {title}\n\n会話が見つかりませんでした。\n"
        
        markdown_lines = [f"# {title}\n"]
        
        for i, conversation in enumerate(conversations, 1):
            markdown_lines.append(f"## 会話 {i}\n")
            
            # ユーザーの発言
            if 'user' in conversation and conversation['user']:
                markdown_lines.append("### User")
                user_text = self._improve_code_blocks(conversation['user'])
                markdown_lines.append(user_text)
                markdown_lines.append("")
            
            # Geminiの応答
            if 'gemini' in conversation and conversation['gemini']:
                markdown_lines.append("### Gemini")
                gemini_text = self._improve_code_blocks(conversation['gemini'])
                markdown_lines.append(gemini_text)
                markdown_lines.append("")
            
            markdown_lines.append("---\n")
        
        return "\n".join(markdown_lines)
    
    def save_to_file(self, content: str, output_path: str) -> None:
        """
        Markdownコンテンツをファイルに保存
        
        Args:
            content: Markdownコンテンツ
            output_path: 出力ファイルのパス
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Markdownファイルを保存しました: {output_path}")
            
        except Exception as e:
            raise Exception(f"ファイル保存エラー: {e}")
    
    def format_simple(self, conversations: List[Dict[str, str]]) -> str:
        """
        シンプルな会話形式でフォーマット
        
        Args:
            conversations: 会話のリスト
            
        Returns:
            シンプルなMarkdown文字列
        """
        if not conversations:
            return "会話が見つかりませんでした。\n"
        
        markdown_lines = []
        
        for conversation in conversations:
            if 'user' in conversation and conversation['user']:
                markdown_lines.append("**User:**")
                user_text = self._improve_code_blocks(conversation['user'])
                markdown_lines.append(user_text)
                markdown_lines.append("")
            
            if 'gemini' in conversation and conversation['gemini']:
                markdown_lines.append("**Gemini:**")
                gemini_text = self._improve_code_blocks(conversation['gemini'])
                markdown_lines.append(gemini_text)
                markdown_lines.append("")
            
            markdown_lines.append("---\n")
        
        return "\n".join(markdown_lines)
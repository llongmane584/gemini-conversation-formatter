"""
Gemini会話HTMLパーサー

GeminiのHTMLファイルから<user-query>と<model-response>を抽出し、
テキストコンテンツを取得する
"""

from bs4 import BeautifulSoup
from typing import List, Dict
import re


class GeminiConversationParser:
    """Gemini会話HTMLファイルをパースするクラス"""
    
    def __init__(self):
        self.conversations = []
    
    def parse_html_file(self, file_path: str) -> List[Dict[str, str]]:
        """
        HTMLファイルをパースして会話を抽出
        
        Args:
            file_path: HTMLファイルのパス
            
        Returns:
            会話のリスト（userとgeminiのペア）
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            return self.parse_html_content(html_content)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
        except Exception as e:
            raise Exception(f"ファイル読み込みエラー: {e}")
    
    def parse_html_content(self, html_content: str) -> List[Dict[str, str]]:
        """
        HTML文字列から会話を抽出
        
        Args:
            html_content: HTML文字列
            
        Returns:
            会話のリスト
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        conversations = []
        
        # user-queryとmodel-responseを順番に取得
        user_queries = soup.find_all('user-query')
        model_responses = soup.find_all('model-response')
        
        # 会話をペアとして結合
        for i in range(max(len(user_queries), len(model_responses))):
            conversation = {}
            
            if i < len(user_queries):
                user_text = self._extract_text_content(user_queries[i])
                conversation['user'] = user_text
            
            if i < len(model_responses):
                gemini_text = self._extract_text_content(model_responses[i])
                conversation['gemini'] = gemini_text
                
            if conversation:  # 空でない場合のみ追加
                conversations.append(conversation)
        
        return conversations
    
    def _extract_text_content(self, element) -> str:
        """
        HTMLエレメントからテキストコンテンツを抽出
        
        Args:
            element: BeautifulSoupエレメント
            
        Returns:
            クリーンなテキスト
        """
        if not element:
            return ""
        
        # 改行タグを明示的に改行文字に変換
        for br in element.find_all(['br']):
            br.replace_with('\n')
        
        # ブロック要素の後に改行を追加
        for block in element.find_all(['p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if block.string:
                block.string.replace_with(block.string + '\n')
            else:
                block.append('\n')
        
        # <code>タグをインラインコードに変換
        for code_tag in element.find_all("code"):
            code_content = code_tag.get_text()
            code_tag.replace_with(f"`{code_content}`")
        
        # スクリプトやスタイルタグを除去
        for script in element(["script", "style", "svg", "path"]):
            script.decompose()
        
        # テキストを取得（改行を保持）
        text = element.get_text(separator='\n', strip=False)
        
        # 3行以上の連続改行を2行に制限
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 行末の空白を削除（改行は維持）
        text = '\n'.join(line.rstrip() for line in text.split('\n'))
        
        # 全体の先頭末尾の空白行を削除
        text = text.strip()
        
        return text
    
    def get_conversation_count(self) -> int:
        """会話数を取得"""
        return len(self.conversations)
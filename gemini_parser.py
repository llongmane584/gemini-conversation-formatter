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
        
        # スクリプトやスタイルタグを除去
        for script in element(["script", "style", "svg", "path"]):
            script.decompose()
        
        # 改行タグを明示的に改行文字に変換
        for br in element.find_all(['br']):
            br.replace_with('\n')
        
        # 太字タグをMarkdown形式に変換（ブロック要素処理の前に実行）
        for strong_tag in element.find_all(["strong", "b"]):
            strong_text = strong_tag.get_text()
            strong_tag.replace_with(f"**{strong_text}**")
        
        # 斜体タグをMarkdown形式に変換
        for italic_tag in element.find_all(["em", "i"]):
            italic_text = italic_tag.get_text()
            italic_tag.replace_with(f"*{italic_text}*")
        
        # <code>タグをインラインコードに変換
        for code_tag in element.find_all("code"):
            code_content = code_tag.get_text()
            code_tag.replace_with(f"`{code_content}`")
        
        # 見出しタグをMarkdown形式に変換（2レベル格下げして第3レベルから開始）
        for i in range(1, 7):  # h1からh6まで
            for heading in element.find_all(f"h{i}"):
                heading_text = heading.get_text().strip()
                # 2レベル格下げ：h1→###、h2→####、最大######まで
                markdown_level = min(i + 2, 6)
                markdown_heading = "#" * markdown_level + f" {heading_text}"
                heading.replace_with(f"\n{markdown_heading}\n")
        
        # リスト要素をMarkdown形式に変換
        self._convert_lists_to_markdown(element)
        
        # ブロック要素の後に改行を追加
        for block in element.find_all(['p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if block.string:
                block.string.replace_with(block.string + '\n')
            else:
                block.append('\n')
        
        # テキストを取得（改行を維持）
        text = element.get_text(separator='\n', strip=False)
        
        # 3行以上の連続改行を2行に制限
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 行末の空白を削除（改行は維持）
        text = '\n'.join(line.rstrip() for line in text.split('\n'))
        
        # 全体の先頭末尾の空白行を削除
        text = text.strip()
        
        return text
    
    def _convert_lists_to_markdown(self, element) -> None:
        """
        リスト要素をMarkdown形式に変換
        
        Args:
            element: BeautifulSoupエレメント
        """
        # 順序付きリスト（ol）を処理
        for ol in element.find_all("ol"):
            self._convert_ordered_list(ol)
        
        # 順序なしリスト（ul）を処理
        for ul in element.find_all("ul"):
            self._convert_unordered_list(ul)
    
    def _convert_ordered_list(self, ol) -> None:
        """順序付きリストをMarkdown形式に変換"""
        items = ol.find_all("li", recursive=False)  # 直接の子要素のみ
        markdown_items = []
        
        for i, li in enumerate(items, 1):
            item_text = li.get_text().strip()
            if item_text:
                markdown_items.append(f"{i}. {item_text}")
        
        if markdown_items:
            markdown_list = "\n" + "\n".join(markdown_items) + "\n"
            ol.replace_with(markdown_list)
    
    def _convert_unordered_list(self, ul) -> None:
        """順序なしリストをMarkdown形式に変換"""
        items = ul.find_all("li", recursive=False)  # 直接の子要素のみ
        markdown_items = []
        
        for li in items:
            item_text = li.get_text().strip()
            if item_text:
                markdown_items.append(f"- {item_text}")
        
        if markdown_items:
            markdown_list = "\n" + "\n".join(markdown_items) + "\n"
            ul.replace_with(markdown_list)
    
    def get_conversation_count(self) -> int:
        """会話数を取得"""
        return len(self.conversations)
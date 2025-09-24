from typing import List, Optional

import re
from bs4 import BeautifulSoup

from helpers import (
    create_file, 
    add_title_to_file, 
    add_content_to_file,
    get_html_content,
)


class Hjwzw:
    def __init__(
        self, 
        novel_id: int, 
        novel_name: str, 
        after_chapter_id: Optional[str] = None,
        is_continue: bool = False
    ) -> None:
        self.base_url: str = "https://tw.hjwzw.com"
        self.novel_id: int = novel_id
        self.novel_name: str = novel_name
        self.after_chapter_id: Optional[int] = after_chapter_id
        self.is_continue: bool = is_continue
        # 定義章節相關的配置
        self.chapter_config = {
            "number_chars": r"零一二兩三四五六七八九十百千萬\d",  # 可能的數字字符
            "chapter_marker": "章",  # 章節標記字符
        }

    def get_chapter_ids(self) -> List[str]:
        url: str = f"{self.base_url}/Book/Chapter/{self.novel_id}"
        response_text: str = get_html_content(url)

        soup: BeautifulSoup = BeautifulSoup(response_text, "html.parser")
        a_tags: List[BeautifulSoup] = soup.find_all('a', href=True)

        pattern: re.Pattern = re.compile(r'^/Book/Read/\d+,(\d+)$')
        chapter_ids: List[str] = []
        for tag in a_tags:
            href: str = tag['href']
            match: Optional[re.Match] = pattern.match(href)

            if not match: 
                continue
            
            # 如果需要繼續爬取，則只爬取大於等於 after_chapter_id 的章節
            if self.is_continue:
                if int(match.group(1)) >= self.after_chapter_id:
                    chapter_ids.append(match.group(1))
            else:
                chapter_ids.append(match.group(1))

        return chapter_ids

    def get_chapter_title(self, chapter_id: str) -> str:
        url: str = f"{self.base_url}/Book/Read/{self.novel_id},{chapter_id}"
        response_text: str = get_html_content(url)

        soup: BeautifulSoup = BeautifulSoup(response_text, "html.parser")
        title: str = soup.find("h1").get_text().strip()
        title = "".join(title.split())

        # 使用配置構建正則表達式
        pattern = f".*?([{self.chapter_config['number_chars']}]+){self.chapter_config['chapter_marker']}(.*)"
        match = re.match(pattern, title)
        
        if match:
            chapter_number: str = match.group(1)
            chapter_title: str = match.group(2)
            return f"第{chapter_number}章 {chapter_title}"
        else:
            print(f"因無法解析此標題: {title}，故將會直接使用原始標題。")
            return title

    def get_chapter_description(self, chapter_id: str) -> Optional[str]:
        url: str = f"{self.base_url}/Book/Read/{self.novel_id},{chapter_id}"
        response_text: str = get_html_content(url)

        soup: BeautifulSoup = BeautifulSoup(response_text, "html.parser")

        # 尋找 <meta> 標籤，屬性為 property="og:description"
        meta_tag = soup.find("meta", attrs={"property": "og:description"})

        if meta_tag and "content" in meta_tag.attrs:
            description_content: str = meta_tag["content"]
            if len(description_content) > 13:  # 因爲要避開 ...
                return description_content[:10]
            else:
                print("chapter_description 內容太短，無法使用")
                return None
        else:
            print("未找到 chapter_description")
            return None

    def get_chapter_content(self, chapter_id: str) -> str:
        url: str = f"{self.base_url}/Book/Read/{self.novel_id},{chapter_id}"
        response_text: str = get_html_content(url)

        soup: BeautifulSoup = BeautifulSoup(response_text, "html.parser")

        # 先獲取 description_content
        description: Optional[str] = self.get_chapter_description(chapter_id)

        ally_site_div: Optional[BeautifulSoup] = soup.find("div", id="AllySite")
        content_div: Optional[BeautifulSoup] = ally_site_div.find_next(
            "div", style=lambda value: value and "font-size: 20px;" in value
        ) if ally_site_div else None

        if content_div:
            for element in content_div.find_all(["a", "b"]):
                element.extract()  # 移除不要的標籤
        
        content: str = content_div.get_text("\n", strip=True) if content_div else ""
        
        # 如果有找到 description，從 description 開始截取內容
        if description:
            try:
                start_index = content.index(description)
                content = content[start_index:]
            except ValueError:
                print(f"無法在內容中找到 description: {description}，故直接使用原始內容")
        
        return content
    
    def main(self) -> None:
        file_path: str = f"./novels/{self.novel_name}.txt"

        # 如果不是斷點續爬，則創建文件
        if not self.is_continue:
            create_file(file_path=file_path)

        chapter_ids: List[str] = self.get_chapter_ids()
        for chapter_id in chapter_ids:
            print(f"Current chapter id: {chapter_id}")

            title: str = self.get_chapter_title(chapter_id)
            add_title_to_file(file_path=file_path, content=title)
            print(f"Current chapter title: {title}")

            get_chapter_description: Optional[str] = self.get_chapter_description(chapter_id)
            print(f"Current chapter description: {get_chapter_description}")

            content: str = self.get_chapter_content(chapter_id)
            add_content_to_file(file_path=file_path, content=content)

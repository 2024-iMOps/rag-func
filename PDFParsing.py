import os
import json
import requests
import fitz

from tqdm import tqdm
from bs4 import BeautifulSoup
from markdownify import markdownify as markdown

from dotenv import load_dotenv
load_dotenv()

class PDFParsing:
    def __init__(self):
        """
        Upstage Document Parse 활용
        """
        self.api_key = os.environ.get("UPSTAGE_API_KEY")
        self.url = "https://api.upstage.ai/v1/document-ai/document-parse"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def save_json(self, filename, save_path):
        """
        API 반환값을 JSON 형식으로 저장
        
        filename: pdf 이름<br>
        save_path: json 파일을 저장할 경로
        """
        files = {"document": open(filename, "rb")}
        response = requests.post(self.url, headers=self.headers, files=files)
        json_data = response.json()

        json_file_path = os.path.join(save_path, "parse_results.json")
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

        return json_data

    def save_html(self, json_data, save_path):
        """
        JSON에서 HTML 요소 추출
        
        json_data: json 데이터 변수<br>
        save_path: html 파일을 저장할 경로
        """
        html_file_path = os.path.join(save_path, "parse_results.html")
        html_data = ""
        with open(html_file_path, "w", encoding="utf-8") as f:
            for element in json_data["elements"]:
                html_data += element["content"]["html"] + "\n"
                f.write(element["content"]["html"] + "\n")

        return html_data

    def save_md(self, html_data, save_path):
        """
        HTML 형식을 Markdown으로 변환
        
        html_data: html 데이터 변수<br>
        save_path: markdown 파일을 저장할 경로
        """
        md_file_path = os.path.join(save_path, "parse_results.md")
        md_data = markdown(
            html_data,
            convert=[tag for tag in set([tag.name for tag in BeautifulSoup(html_data, "html.parser").find_all()]) if tag not in ["br"]],
        )

        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(md_data)

        return md_data

# def main():
#     category = "card"
#     data_dir = "/workspace/rag-baseline/data"
#     save_base_path = "/workspace/rag-baseline/data-parse"

#     parsing = PDFParsing()

#     pdf_files = [f for f in os.listdir(os.path.join(data_dir, category)) if f.endswith(".pdf")]
#     total_files = len(pdf_files)

#     with tqdm(total=total_files, desc="Parse PDF files") as pbar:
#         for pdf_name in pdf_files:
#             save_path = os.path.join(save_base_path, category, os.path.splitext(pdf_name)[0])
#             if not os.path.exists(save_path):
#                 os.makedirs(save_path)

#             filename = os.path.join(data_dir, category, pdf_name)

#             json_data = parsing.save_json(filename, save_path)
#             html_data = parsing.save_html(json_data, save_path)
#             parsing.save_md(html_data, save_path)

#             pbar.update(1)

# if __name__ == "__main__":
#     main()
import os
import streamlit as st
from PDFParsing import PDFParsing

def main():
    st.set_page_config(page_title="Document Parse")
    st.title("Document Parse")

    # 클래스 불러오기
    parsing = PDFParsing()

    st.subheader("Upload PDF file")
    uploaded_file = st.file_uploader("Choose a file", type="pdf")

    if uploaded_file is not None:

        # 저장 경로: PDFParsing 코드는 해당 경로에 json, html, md 다 저장되게끔 하고있음
        data_dir = "/workspace"
        category = "card"
        save_path = os.path.join(data_dir, category, uploaded_file.name.replace(".pdf", ""))
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        filename = os.path.join(data_dir, category, uploaded_file.name)
        with open(filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 파싱 시작
        st.subheader("Parsing PDF...")
        progress_bar = st.progress(0)
        json_data = parsing.save_json(filename, save_path)
        html_data = parsing.save_html(json_data, save_path)
        md_data = parsing.save_md(html_data, save_path)
        progress_bar.progress(100)

        # 마크다운 파일 다운로드 버튼
        st.download_button(
            label="Download Markdown",
            data=md_data,
            file_name="parse_results.md",
            mime="text/markdown",
        )

if __name__ == "__main__":
    main()